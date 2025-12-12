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

This class extends the mcp-server-sparql MCP server.
"""

import json
import argparse
from typing import Dict, Any, Optional, Union, List, Tuple
from io import StringIO
import csv
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound

from mcp.server.fastmcp import FastMCP


class SPARQLServer:
    """SPARQL endpoint wrapper with Proto-OKN/registry awareness."""

    def __init__(self, endpoint_url: str, description: Optional[str] = None):
        self.endpoint_url = endpoint_url
        self.description = description  # None means: try to infer
        self.kg_name = ""
        self.registry_url: Optional[str] = None
        self.github_base_url = "https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/metadata/entities"

        # Initialize SPARQLWrapper with only the query endpoint

        # As a workaround, use the federated endpoint
        # self.sparql = SPARQLWrapper(endpoint_url)
        federated_endpoint = "https://frink.apps.renci.org/federation/sparql"
        
        self.sparql = SPARQLWrapper(federated_endpoint)
        self.sparql.setReturnFormat(JSON)

    # ---------------------- Internal helpers ---------------------- #
    def _insert_from_clause(self, query_string, kg_name):
        """
        Inserts a FROM line after the SELECT clause and before WHERE.
        Example insert:
            FROM <https://purl.org/okn/frink/kg/{kg_name}>
        """
        from_line = f"FROM <https://purl.org/okn/frink/kg/{kg_name}>\n"
    
        lines = query_string.split("\n")
        new_lines = []
        select_seen = False
    
        for line in lines:
            new_lines.append(line)
            # Detect SELECT but not WHERE yet
            if line.strip().startswith("SELECT"):
                select_seen = True
                continue
            
            if select_seen and line.strip().startswith("WHERE"):
                # Insert FROM just before WHERE
                new_lines.insert(-1, from_line)
                select_seen = False  # only insert once
    
        return "\n".join(new_lines)

    def _extract_values(self, result: Any, var: str) -> List[str]:
        """Extract variable bindings from a SPARQL JSON result."""
        if isinstance(result, dict) and "results" in result:
            values = []
            for binding in result["results"].get("bindings", []):
                if var in binding:
                    values.append(binding[var].get('value', ''))
            return values
        
        # Fallback for unexpected formats
        if isinstance(result, list):
            return [
                row.get(var, '')
                for row in result
                if isinstance(row, dict)
            ]
        
        return []

    def _simplify_result(self, result: Dict) -> Dict:
        """Remove type/datatype metadata, keep only values"""
        if 'results' not in result:
            return result
            
        simplified_bindings = []
        for binding in result['results']['bindings']:
            row = {}
            for var, data in binding.items():
                row[var] = data.get('value', '')
            simplified_bindings.append(row)
        
        return {
            'variables': result['head']['vars'],
            'rows': simplified_bindings,
            'count': len(simplified_bindings)
        }
    
    def _compact_result(self, result: Dict) -> Dict:
        """Return compact format with headers separate from data arrays"""
        if 'results' not in result:
            return result
        
        variables = result['head']['vars']
        data_rows = []
        
        for binding in result['results']['bindings']:
            # Create row as array in same order as variables
            row = []
            for var in variables:
                row.append(binding.get(var, {}).get('value', ''))
            data_rows.append(row)
        
        return {
            'columns': variables,
            'data': data_rows,
            'count': len(data_rows)
        }

    def _values_only(self, result: Dict) -> List[Dict[str, str]]:
        """Return flat list of value dictionaries"""
        if 'results' not in result:
            return []
        
        values_list = []
        for binding in result['results']['bindings']:
            row = {}
            for var in binding:
                row[var] = binding[var].get('value', '')
            values_list.append(row)
        
        return values_list

    def _to_csv(self, result: Dict) -> str:
        """Convert result to CSV string"""
        if 'results' not in result:
            return ""
        
        output = StringIO()
        vars = result['head']['vars']
        writer = csv.DictWriter(output, fieldnames=vars)
        writer.writeheader()
        
        for binding in result['results']['bindings']:
            row = {}
            for var in vars:
                if var in binding:
                    row[var] = binding[var].get('value', '')
                else:
                    row[var] = ''
            writer.writerow(row)
        
        return output.getvalue()
    
    def _get_registry_url(self) -> Optional[Tuple[str, str]]:
        """Return (kg_name, registry_url) if this looks like a FRINK endpoint, else None."""
        if not self.endpoint_url.startswith("https://frink.apps.renci.org/"):
            return None

        path_parts = urlparse(self.endpoint_url).path.strip("/").split("/")
        kg_name = path_parts[-2] if len(path_parts) >= 2 else "unknown"

        registry_url = (
            "https://raw.githubusercontent.com/frink-okn/okn-registry/"
            "refs/heads/main/docs/registry/kgs/"
            f"{kg_name}.md"
        )
        self.registry_url = registry_url
        self.kg_name = kg_name
        return kg_name, registry_url

    def _fetch_registry_content(self) -> Optional[str]:
        """Fetch registry page content in markdown format or None on failure."""
        try:
            result = self._get_registry_url()
            if not result:
                return None

            kg_name, registry_url = result

            with urlopen(registry_url, timeout=5) as resp:
                raw = resp.read()
                text = raw.decode("utf-8", errors="replace")
                return text.strip()
        except Exception:
            return None

    def _get_entity_metadata(self) -> Dict[str, Dict[str, str]]:
        """
        Fetch entity metadata from GitHub CSV file.
        Returns a dict mapping URI to {label, description}.
        """
        # Construct the GitHub raw file URL
        result = self._get_registry_url()
        if not result:
            return {}
            
        kg_name, _ = result
        filename = f"{kg_name}_entities.csv"
        url = f"{self.github_base_url}/{filename}"
        
        try:
            with urlopen(url, timeout=5) as response:
                # Read and decode the response
                content = response.read().decode('utf-8')
                
                # Parse CSV
                csv_reader = csv.DictReader(StringIO(content))
                
                # Build metadata dict
                metadata = {}
                for row in csv_reader:
                    uri = row.get('URI', '').strip()
                    label = row.get('Label', '').strip()
                    description = row.get('Description', '').strip()
                    rdf_type = row.get('Type', '').strip()
                    
                    if uri:
                        metadata[uri] = {
                            'label': label,
                            'description': description,
                            'rdf_type': rdf_type
                        }
                
                return metadata
                
        except HTTPError as e:
            print(f"HTTP Error fetching entity metadata: {e.code} {e.reason}")
            print(f"URL attempted: {url}")
            return {}
        except URLError as e:
            print(f"URL Error fetching entity metadata: {e.reason}")
            print(f"URL attempted: {url}")
            return {}
        except Exception as e:
            print(f"Error parsing entity metadata: {e}")
            return {}

    # ---------------------- Public API ---------------------- #
    def execute(self, query_string: str, format: str = 'compact') -> Union[Dict[str, Any], str]:
        """Execute SPARQL query with format options: 'full', 'simplified', 'compact', 'values', 'csv'"""
        try:
            # workaround to use federated endpoint (insert a FROM clause to select the KG)
            info = self._get_registry_url()
            if info:
                kg_name, registry_url = info
                query_string = self._insert_from_clause(query_string, kg_name)
            
            self.sparql.setQuery(query_string)
            result = self.sparql.query().convert()
            
            # Format the result based on requested format
            if format == 'simplified':
                formatted_result = self._simplify_result(result)
            elif format == 'compact':
                formatted_result = self._compact_result(result)
            elif format == 'values':
                formatted_result = self._values_only(result)
            elif format == 'csv':
                formatted_result = self._to_csv(result)
            else:
                formatted_result = result
            
            return formatted_result
                
        except Exception as e:
            # Could special-case EndPointNotFound if imported.
            return {"error": f"Query error: {str(e)}"}

    def query_schema(self, compact: bool = False) -> Dict[str, Any]:
        """Return a dict with classes and predicates discovered in the graph."""
        # Try to get entity metadata
        metadata = self._get_entity_metadata()
        kg_name = self.kg_name
        
        # If metadata is available, return it directly without querying
        if len(metadata) > 0:
            # Extract classes and predicates from metadata
            class_data = []
            predicate_data = []
            
            for uri, entity_info in metadata.items():
                rdf_type = entity_info.get('rdf_type', '')
                label = entity_info.get('label', uri.split('/')[-1].split('#')[-1])
                description = entity_info.get('description', '')
                
                # Check if it's a class or predicate
                if rdf_type == 'Class':
                    class_data.append([uri, label, description, rdf_type])
                elif rdf_type == 'Predicate':
                    predicate_data.append([uri, label, description, rdf_type])
            
            return {
                'classes': {
                    'columns': ['uri', 'label', 'description', 'rdf_type'],
                    'data': class_data,
                    'count': len(class_data)
                },
                'predicates': {
                    'columns': ['uri', 'label', 'description', 'rdf_type'],
                    'data': predicate_data,
                    'count': len(predicate_data)
                }
            }
        
        # No metadata available, query for classes and predicates
        class_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?class
WHERE {{
    ?instance rdf:type ?class .
}}
        """
        class_query = self._insert_from_clause(class_query, kg_name)
        classes = self.execute(class_query, format='compact')

        predicate_query = f"""
SELECT DISTINCT ?predicate
WHERE {{
  ?s ?predicate ?o .
}}
        """
        predicate_query = self._insert_from_clause(predicate_query, kg_name)
        predicates = self.execute(predicate_query, format='compact')

        # Extract URIs from compact format
        class_uris = classes.get('data', [])
        class_uris = [row[0] for row in class_uris if row]  # Get first column values
        
        predicate_uris = predicates.get('data', [])
        predicate_uris = [row[0] for row in predicate_uris if row]  # Get first column values
        
        # No metadata available, just return URIs
        class_data = [[uri] for uri in class_uris]
        predicate_data = [[uri] for uri in predicate_uris]
        
        return {
            'classes': {
                'columns': ['uri'],
                'data': class_data,
                'count': len(class_data)
            },
            'predicates': {
                'columns': ['uri'],
                'data': predicate_data,
                'count': len(predicate_data)
            }
        }

    def build_description(self) -> str:
        """Return human-readable metadata about this endpoint."""
        # If caller provided an explicit description, honor it.
        if self.description is not None:
            return self.description.strip()

        # Otherwise, try FRINK registry
        content = self._fetch_registry_content()
        if content and self.registry_url:
            header = f"[registry: {self.registry_url}]\n\n"
            description = header + content
            
            # Try to append additional description from GitHub metadata/descriptions
            additional_desc = self._fetch_additional_description()
            if additional_desc:
                description += "\n\n" + additional_desc
            
            return description

        # Fallback
        return "SPARQL Query Server"
    
    def _fetch_additional_description(self) -> Optional[str]:
        """
        Fetch additional description from GitHub metadata/descriptions directory.
        Returns the description content or None if not found.
        """
        if not self.kg_name:
            return None
            
        # Construct URL to the description file
        description_url = (
            "https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/"
            f"main/metadata/descriptions/{self.kg_name}.txt"
        )
        
        try:
            with urlopen(description_url, timeout=5) as resp:
                raw = resp.read()
                text = raw.decode("utf-8", errors="replace")
                return text.strip()
        except (URLError, HTTPError):
            # File doesn't exist or network error
            return None
        except Exception:
            # Any other error
            return None


def parse_args():
    parser = argparse.ArgumentParser(description="MCP SPARQL Query Server")
    parser.add_argument(
        "--endpoint",
        required=True,
        help="SPARQL endpoint URL (e.g., https://frink.apps.renci.org/spoke/sparql)",
    )
    parser.add_argument(
        "--description",
        required=False,
        help=(
            "Description of the SPARQL endpoint "
            "(For FRINK endpoints this is automatically generated)"
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize server (auto-derives kg metadata & dynamic description if applicable)
    sparql_server = SPARQLServer(
        endpoint_url=args.endpoint,
        description=args.description,
    )

    # Create MCP server
    mcp = FastMCP("SPARQL Query Server")

    query_doc = f"""
Execute a SPARQL query against the {sparql_server.kg_name or ''} knowledge graph endpoint: {sparql_server.endpoint_url}.

IMPORTANT: You MUST call get_schema() first before using this query tool to understand the available classes and predicates in the knowledge graph.

Args:
    query_string: A valid SPARQL query string
    format: Output format - 'simplified' (default, JSON with dict rows), 'compact' (columns + data arrays, no repeated keys), 'full' (complete SPARQL JSON), 'values' (list of dicts), or 'csv' (CSV string)

Returns:
    The query results in the specified format
"""

    @mcp.tool(description=query_doc)
    def query(query_string: str, format: str = 'compact') -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        return sparql_server.execute(query_string, format=format)

    schema_doc = f"""
Return the schema (classes, relationships, properties) of the {sparql_server.kg_name or ''} knowledge graph endpoint: {sparql_server.endpoint_url}.

IMPORTANT: Always call this tool FIRST before making any queries to understand what data is available in the knowledge graph.

Args:
    compact: If True (default), returns compact URI:label mappings. If False, returns full metadata with descriptions.

Returns:
    The schema in the specified format
"""

    @mcp.tool(description=schema_doc)
    def get_schema(compact: bool = True) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return sparql_server.query_schema(compact=compact)

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

    # Add tool to clean Mermaid diagrams
    @mcp.tool()
    def clean_mermaid_diagram(mermaid_content: str) -> str:
        """Clean a Mermaid class diagram by removing unwanted elements.
        
        This tool removes:
        - All note statements that would render as unreadable yellow boxes
        - Empty curly braces from class definitions
        
        Args:
            mermaid_content: The raw Mermaid class diagram content
            
        Returns:
            Cleaned Mermaid content with note statements and empty braces removed
        """
        import re
        
        lines = mermaid_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip any line containing note syntax
            if (stripped.startswith('note ') or 
                'note for' in stripped or 
                'note left' in stripped or 
                'note right' in stripped):
                continue
            
            # Remove empty curly braces from class definitions
            # Match patterns like: "class ClassName {     }" or "class ClassName { }"
            if re.match(r'^\s*class\s+\w+\s*\{\s*\}\s*$', line):
                # Replace the line with just the class name without braces
                line = re.sub(r'^(\s*class\s+\w+)\s*\{\s*\}\s*$', r'\1', line)
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    # Run MCP server over stdio
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()