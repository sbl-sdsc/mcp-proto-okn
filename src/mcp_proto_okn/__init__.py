"""MCP server for querying SPARQL endpoints."""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mcp_proto-okn")
except PackageNotFoundError:
    __version__ = "0.0.0"
