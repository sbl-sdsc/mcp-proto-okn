"""
MCP SPARQL Server for Proto-OKN Knowledge Graphs

This module provides a Model Context Protocol (MCP) server that enables querying
of SPARQL endpoints, particularly those in the Proto-OKN (Prototype Open Knowledge Network)
ecosystem hosted on the FRINK platform.

The server automatically detects FRINK endpoints and provides appropriate documentation
links to the knowledge graph registry. It supports querying various knowledge graphs
including SPOKE, BioBricks ICE, DREAM-KG, SAWGraph, and many others in the Proto-OKN
program.

For FRINK endpoints (https://frink.apps.renci.org/*), the server automatically generates
a description pointing to the knowledge graph registry. For other endpoints, you can
provide a custom description using the --description argument.

This class is an extension of the mcp-server-sparql MCP server.

Classes:
    SPARQLServer: Wrapper around SPARQLWrapper with MCP integration and FRINK endpoint detection
    
Functions:
    parse_args: Parse command line arguments for endpoint URL and optional description
    main: Main entry point that sets up and runs the MCP server

Example MCP Configuration:
    {
        "mcpServers": {
            "mcp-spoke-sparql": {
                "command": "uv",
                "args": ["run", "python", "-m", "mcp_server_protookn.server", "--endpoint", "https://frink.apps.renci.org/spoke/sparql"]
            },
            "mcp-wikidata-sparql": {
                "command": "uv",
                "args": ["run", "python", "-m", "mcp_server_protookn.server", "--endpoint", "https://query.wikidata.org/sparql","--description", "Access to Wikidata's knowledge graph"]
            }
        }
    }

Dependencies:
    - mcp.server.fastmcp: For MCP server functionality
    
See Also:
    - FRINK Registry: https://frink.renci.org/registry/
    - Proto-OKN: https://www.proto-okn.net/
    - MCP Protocol: https://modelcontextprotocol.io/
    - SPARQL Server: https://github.com/ekzhu/mcp-server-sparql/
"""

import json
import argparse
from typing import Dict, Any, Optional, Union, List, Tuple
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from mcp.server.fastmcp import FastMCP


class SPARQLServer:
    """SPARQL endpoint wrapper with Proto-OKN/registry awareness."""

    def __init__(self, endpoint_url: str, description: Optional[str] = None):
        self.endpoint_url = endpoint_url
        self.description = description  # Keep the original value, None means no explicit description
        self.kg_name = ""
        self.registry_url = None
        # Initialize SPARQLWrapper with only the query endpoint
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    # ---------------------- Internal helpers ---------------------- #   
    def _get_registry_url(self) -> Optional[Tuple[str, str]]:
        """Get the FRINK registry URL for the SPARQL endpoint in markdown format."""
        if not self.endpoint_url.startswith("https://frink.apps.renci.org/"):
            return None
        path_parts = urlparse(self.endpoint_url).path.strip('/').split('/')
        kg_name = path_parts[-2] if len(path_parts) >= 2 else "unknown"
        registry_url = f"https://raw.githubusercontent.com/frink-okn/okn-registry/refs/heads/main/docs/registry/kgs/{kg_name}.md"
        self.registry_url = registry_url
        return kg_name, registry_url
    
    def _fetch_registry_content(self) -> Optional[str]:
        """Fetch registry page content in markdown format or None on failure."""
        try:
            result = self._get_registry_url()
            if not result:
                return None
                
            kg_name, registry_url = result
            self.kg_name = kg_name
 
            with urlopen(registry_url, timeout=5) as resp:
                raw = resp.read()
                text = raw.decode("utf-8", errors="replace")
                print(text)
                return text.strip()
        except Exception:
            return None

    # ---------------------- Public API ---------------------- #
    def execute(self, query_string: str) -> Dict[str, Any]:
        try:
            self.sparql.setQuery(query_string)
            return self.sparql.query().convert()
        except SPARQLExceptions.EndPointNotFound:
            return {"error": f"SPARQL endpoint not found: {self.endpoint_url}"}
        except Exception as e:
            return {"error": f"Query error: {str(e)}"}

    def build_description(self) -> str:
        # If a static description was provided explicitly by the user, prefer it.
        if self.description is not None:
            return self.description.strip()

        # Try to fetch registry content for FRINK endpoints
        content = self._fetch_registry_content()
        if content and self.registry_url:
            header = f"[registry: {self.registry_url}]\n\n"
            return header + content
            
        # Fallback to default description
        return "SPARQL Query Server"


def parse_args():
    parser = argparse.ArgumentParser(description="MCP SPARQL Query Server")
    parser.add_argument(
        "--endpoint",
        required=True,
        help="SPARQL endpoint URL (e.g., https://frink.apps.renci.org/spoke/sparql)"
    )
    parser.add_argument(
        "--description",
        required=False,
        help="Description of the SPARQL endpoint (For FRINK endpoints the description is automatically generated)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    # Initialize server (auto-derives kg metadata & dynamic description if applicable)
    sparql_server = SPARQLServer(endpoint_url=args.endpoint, description=args.description)

    # Create MCP server
    mcp = FastMCP("SPARQL Query Server")

    query_doc = f"""
Execute a SPARQL query against the {sparql_server.kg_name or ''} knowledge graph endpoint: {sparql_server.endpoint_url}.

Args:
    query_string: A valid SPARQL query string

Returns:
    The query results in JSON format
"""

    @mcp.tool(description=query_doc)
    def query(query_string: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return sparql_server.execute(query_string)

    description_doc = """
Get a description and other metadata about the endpoint, including the PI, funding information, and more.

Returns:
    A string containing either:
      - Registry page content prefixed with a header line identifying the registry source, OR
      - The static/server-provided description when no registry URL applies.
"""

    @mcp.tool(description=description_doc)
    def get_description() -> str:
        return sparql_server.build_description()

    # Run MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
