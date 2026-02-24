#!/usr/bin/env python3
"""
Standalone test for mcp-proto-okn HTTP (streamable-http) transport.

Tests:
  1. Server starts in streamable-http mode and responds to MCP initialize.
  2. API-key authentication rejects unauthenticated requests and accepts valid tokens.

Run:
  python tests/test_http_transport.py

Requires no external test framework -- uses only stdlib (unittest, subprocess, urllib).
"""

import json
import os
import signal
import socket
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _free_port():
    """Return an available TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_port(port, host="127.0.0.1", timeout=30):
    """Block until *host:port* accepts a TCP connection or *timeout* expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def _start_server(port, env_extra=None):
    """Start the MCP server as a subprocess in streamable-http mode."""
    env = os.environ.copy()
    env["MCP_PROTO_OKN_TRANSPORT"] = "streamable-http"
    env["MCP_PROTO_OKN_PORT"] = str(port)
    env["MCP_PROTO_OKN_HOST"] = "127.0.0.1"
    if env_extra:
        env.update(env_extra)

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "mcp_proto_okn.server",
            "--endpoint", "https://frink.apps.renci.org/spoke/sparql",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc


def _mcp_initialize(port, headers=None):
    """Send an MCP ``initialize`` request via HTTP POST and return the parsed JSON response."""
    url = f"http://127.0.0.1:{port}/mcp"
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "0.1.0"},
        },
    }).encode()

    req = Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    with urlopen(req, timeout=30) as resp:
        content_type = resp.headers.get("Content-Type", "")
        raw = resp.read().decode()

        # Server may respond with SSE (text/event-stream) or plain JSON
        if "text/event-stream" in content_type:
            # Parse SSE: look for lines starting with "data: "
            for line in raw.splitlines():
                if line.startswith("data: "):
                    return json.loads(line[len("data: "):])
            raise ValueError(f"No data lines found in SSE response: {raw!r}")
        else:
            return json.loads(raw)


class TestHTTPTransport(unittest.TestCase):
    """Test that the MCP server works over streamable-http transport."""

    def test_initialize(self):
        """Server responds to MCP initialize with server info and capabilities."""
        port = _free_port()
        proc = _start_server(port)
        try:
            self.assertTrue(
                _wait_for_port(port),
                f"Server did not start on port {port} within timeout",
            )
            resp = _mcp_initialize(port)

            # The response should be a valid JSON-RPC result with serverInfo
            self.assertIn("result", resp, f"Expected 'result' in response: {resp}")
            result = resp["result"]
            self.assertIn("serverInfo", result)
            self.assertIn("capabilities", result)
            print(f"  Server info: {result['serverInfo']}")
            print(f"  Capabilities: {list(result['capabilities'].keys())}")
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    def test_api_key_reject(self):
        """Server rejects requests without a valid API key when MCP_PROTO_OKN_API_KEY is set."""
        port = _free_port()
        api_key = "test-secret-key-12345"
        proc = _start_server(port, env_extra={"MCP_PROTO_OKN_API_KEY": api_key})
        try:
            self.assertTrue(
                _wait_for_port(port),
                f"Server did not start on port {port} within timeout",
            )

            # Request without auth header should get 401
            with self.assertRaises(HTTPError) as ctx:
                _mcp_initialize(port)
            self.assertEqual(ctx.exception.code, 401)
            print("  Correctly rejected unauthenticated request (401)")
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    def test_api_key_accept(self):
        """Server accepts requests with the correct Bearer token."""
        port = _free_port()
        api_key = "test-secret-key-12345"
        proc = _start_server(port, env_extra={"MCP_PROTO_OKN_API_KEY": api_key})
        try:
            self.assertTrue(
                _wait_for_port(port),
                f"Server did not start on port {port} within timeout",
            )

            # Request with correct Bearer token should succeed
            resp = _mcp_initialize(port, headers={"Authorization": f"Bearer {api_key}"})
            self.assertIn("result", resp, f"Expected 'result' in response: {resp}")
            self.assertIn("serverInfo", resp["result"])
            print("  Correctly accepted authenticated request")
        finally:
            proc.terminate()
            proc.wait(timeout=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
