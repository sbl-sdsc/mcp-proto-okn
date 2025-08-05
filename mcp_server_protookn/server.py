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
                "command": "uvx",
                "args": ["mcp-server-protookn", "--endpoint", "https://frink.apps.renci.org/spoke/sparql"]
            },
            "mcp-custom-sparql": {
                "command": "uvx", 
                "args": ["mcp-server-protookn", "--endpoint", "https://otherendpoint/sparql", "--description", "Custom SPARQL endpoint"]
            }
        }
    }

Dependencies:
    - SPARQLWrapper: For SPARQL endpoint communication
    - mcp.server.fastmcp: For MCP server functionality
    
See Also:
    - FRINK Registry: https://frink.renci.org/registry/
    - Proto-OKN: https://www.proto-okn.net/
    - MCP Protocol: https://modelcontextprotocol.io/
    - SPARQL Server: https://github.com/ekzhu/mcp-server-sparql/
"""

import json
import argparse
from typing import Dict, Any, Optional, Union, List
from urllib.parse import urlparse

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from mcp.server.fastmcp import FastMCP


class SPARQLServer:
    def __init__(self, endpoint_url: str, description: Optional[str] = None):
        self.endpoint_url = endpoint_url
        self.description = description or "SPARQL Query Server"
        self.sparql = SPARQLWrapper(endpoint_url, self.description)
        self.sparql.setReturnFormat(JSON)
    
    def query(self, query_string: str) -> Dict[str, Any]:
        f"""Execute a SPARQL query or general qauery about the KG. {self.description}"""
        try:
            self.sparql.setQuery(query_string)
            results = self.sparql.query().convert()
            return results
        except SPARQLExceptions.EndPointNotFound:
            return {"error": f"SPARQL endpoint not found: {self.endpoint_url}"}
        except Exception as e:
            return {"error": f"Query error: {str(e)}"}


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
        help="Description of the SPARQL endpoint (see: https://frink.renci.org/registry/)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    kg_name = ""

    # Customize the description based on the Proto-OKN endpoint
    if args.endpoint.startswith("https://frink.apps.renci.org/"):
        path_parts = urlparse(args.endpoint).path.strip('/').split('/')
        kg_name = path_parts[-2] if len(path_parts) >= 2 else "unknown"
        # Fix naming inconsistency
        if kg_name == "climatepub4kg":
            kg_name = "climatemodelskg"
        registry_url = f"https://frink.renci.org/registry/kgs/{kg_name}"
        description = f"""
        If the query is about the scientific data within {kg_name}, use SPARQL. 
        If the query is about SPOKE as a project (funding, contacts, awards, description), 
        fetch information from the registry at https://frink.renci.org/registry/kgs/{kg_name} instead.
        """
    else:
        description = args.description

    # Initialize the SPARQL server with the endpoint URL
    sparql_server = SPARQLServer(endpoint_url=args.endpoint, description=description)

    # Create the MCP server
    mcp = FastMCP("SPARQL Query Server")
    
    query_doc = f"""
Execute a SPARQL query against the {kg_name} knowledge graph endpoint: {sparql_server.endpoint_url}. 
{description}
        
Args:
    query_string: A valid SPARQL query string or a question about the knowledge graph
    
Returns:
    The query results in JSON format
"""

    @mcp.tool(description=query_doc)
    def query(query_string: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return sparql_server.query(query_string)
    
    # Run the MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
