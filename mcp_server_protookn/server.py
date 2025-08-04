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
    
Usage:
    python server.py --endpoint https://frink.apps.renci.org/spoke/sparql
    python server.py --endpoint https://otherendpoint/sparql --description "Custom SPARQL endpoint"
    
    Or via uvx:
    uvx mcp-server-protookn --endpoint https://frink.apps.renci.org/spoke/sparql
    uvx mcp-server-protookn --endpoint https://otherendpoint/sparql --description "Custom description"

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
        # Automatically detect FRINK endpoints and set description
        if endpoint_url.startswith("https://frink.apps.renci.org/"):
            # Extract the KG name from the URL
            path_parts = urlparse(endpoint_url).path.strip('/').split('/')
            kg_name = path_parts[-2]
            self.description = f"https://frink.renci.org/registry/kgs/{kg_name}"
            print(self.description)
        else:
            self.description = description or "SPARQL Query Server"
        self.sparql = SPARQLWrapper(endpoint_url, self.description)
        self.sparql.setReturnFormat(JSON)
    
    def query(self, query_string: str) -> Dict[str, Any]:
        f"""Execute a SPARQL query and return the results or for questions about the underlying KG see {self.description}"""
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
    
    # Initialize the SPARQL server with the endpoint URL
    sparql_server = SPARQLServer(endpoint_url=args.endpoint, description=None)
    
    # Create the MCP server
    mcp = FastMCP("SPARQL Query Server")
    
    query_doc = f"""
Execute a SPARQL query against the endpoint {sparql_server.endpoint_url}.
        
Args:
    query_string: A valid SPARQL query string
    
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
