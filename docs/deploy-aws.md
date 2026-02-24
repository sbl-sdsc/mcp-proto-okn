# Deploying the Proto-OKN Unified MCP Server on AWS

## What It Is

A lightweight Python server that exposes 27 Proto-OKN knowledge graphs through a single MCP endpoint. It proxies SPARQL queries to the FRINK platform (`frink.apps.renci.org`) — it doesn't host any data, so resource requirements are minimal (a `t3.small` or equivalent is fine).

## Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/sbl-sdsc/mcp-proto-okn.git
cd mcp-proto-okn
uv sync
```

Optional: set `MCP_PROTO_OKN_API_KEY=<token>` for Bearer-token authentication.

## Starting the Server

Three equivalent ways to start the server:

```bash
# Option 1: uv run (manages venv automatically, no install needed)
uv run mcp-proto-okn-unified --transport streamable-http --port 8000

# Option 2: Installed console script (after uv sync or pip install -e .)
mcp-proto-okn-unified --transport streamable-http --port 8000

# Option 3: Direct Python module invocation
python -m mcp_proto_okn.unified_server --transport streamable-http --port 8000
```

## HTTPS

Claude Desktop requires HTTPS with a valid domain. Put a reverse proxy (Caddy, nginx, etc.) in front of the server with a TLS certificate, and point a DNS record at the instance. Claude Code can use plain HTTP for dev/testing.

## Client Configuration

```json
{
  "mcpServers": {
    "proto-okn": {
      "type": "url",
      "url": "https://your-domain.example.com/mcp"
    }
  }
}
```

## For Production

Use systemd (or equivalent) to keep the process running across reboots. Alternatively, containerize it and run on a managed service like ECS Fargate or Cloud Run with a load balancer handling TLS.
