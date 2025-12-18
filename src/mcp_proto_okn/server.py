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

import os
import json
import argparse
import textwrap
from typing import Dict, Any, Optional, Union, List, Tuple
from io import StringIO
import csv
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import certifi

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

        # Work around certificate issue
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
        os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
        
        # Initialize SPARQLWrapper with only the query endpoint

        # As a workaround, use the federated endpoint
        # self.sparql = SPARQLWrapper(endpoint_url)
        federated_endpoint = "https://frink.apps.renci.org/federation/sparql"
        
        self.sparql = SPARQLWrapper(federated_endpoint)
        self.sparql.setReturnFormat(JSON)

        self.sparql.setMethod("GET")
        self.sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")
        self.sparql.setTimeout(120)

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
        Returns a dict mapping URI to {label, description, type}.
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
                content = response.read().decode('utf-8')
                
            # Parse CSV
            reader = csv.DictReader(StringIO(content))
            metadata = {}
            
            for row in reader:
                uri = row.get('URI', '').strip()
                label = row.get('Label', '').strip()
                description = row.get('Description', '').strip()
                entity_type = row.get('Type', '').strip()
                
                if uri:
                    metadata[uri] = {
                        'label': label,
                        'description': description,
                        'type': entity_type
                    }
            
            return metadata
            
        except Exception as e:
            # If file doesn't exist or any error occurs, return empty dict
            return {}

    def execute(self, query_string: str, format: str = 'compact') -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """Execute SPARQL query and return results in requested format."""
        # Get kg_name for FROM clause insertion
        result = self._get_registry_url()
        if result:
            kg_name, _ = result
            query_string = self._insert_from_clause(query_string, kg_name)
        
        self.sparql.setQuery(query_string)
        
        try:
            raw_result = self.sparql.query().convert()
        except Exception as e:
            return {
                'error': str(e),
                'query': query_string
            }
        
        # Apply requested format
        if format == 'full':
            return raw_result
        elif format == 'simplified':
            return self._simplify_result(raw_result)
        elif format == 'compact':
            return self._compact_result(raw_result)
        elif format == 'values':
            return self._values_only(raw_result)
        elif format == 'csv':
            return self._to_csv(raw_result)
        else:
            return self._compact_result(raw_result)

    def query_schema(self, compact: bool = True) -> Dict[str, Any]:
        """
        Query the knowledge graph schema to discover classes and predicates.
        
        Args:
            compact: If True, returns just URIs. If False, enriches with labels and descriptions.
        
        Returns:
            A dictionary with 'classes' and 'predicates' keys, each containing schema info.
        """
        result = self._get_registry_url()
        if not result:
            return {
                'error': 'Cannot determine KG name for schema query',
                'classes': {'columns': ['uri'], 'data': [], 'count': 0},
                'predicates': {'columns': ['uri'], 'data': [], 'count': 0}
            }
        
        kg_name, _ = result

        # Try to get metadata from GitHub CSV first
        entity_metadata = self._get_entity_metadata()
        
        # If we have metadata, use it to build the schema
        if entity_metadata:
            # Separate entities by type
            classes = []
            predicates = []
            
            for uri, metadata in entity_metadata.items():
                entity_type = metadata.get('type', '').lower()
                
                if entity_type == 'class':
                    classes.append({
                        'uri': uri,
                        'label': metadata.get('label', ''),
                        'description': metadata.get('description', ''),
                        'type': metadata.get('type', '')
                    })
                elif entity_type == 'predicate':
                    predicates.append({
                        'uri': uri,
                        'label': metadata.get('label', ''),
                        'description': metadata.get('description', ''),
                        'type': metadata.get('type', '')
                    })
            
            # Build response with full metadata
            class_data = [[c['uri'], c['label'], c['description'], c['type']] for c in classes]
            predicate_data = [[p['uri'], p['label'], p['description'], p['type']] for p in predicates]
            
            return {
                'classes': {
                    'columns': ['uri', 'label', 'description', 'type'],
                    'data': class_data,
                    'count': len(class_data)
                },
                'predicates': {
                    'columns': ['uri', 'label', 'description', 'type'],
                    'data': predicate_data,
                    'count': len(predicate_data)
                }
            }
        
        # Otherwise, fall back to SPARQL queries
        # FIXED: Query for classes using both 'a' and explicit rdf:type
        # Also query for objects that are used as types (in case instances aren't available)
        class_query = textwrap.dedent("""
            SELECT DISTINCT ?class
            WHERE {
              {
                # Method 1: Find classes through instances using 'a' shorthand
                ?s a ?class .
              } UNION {
                # Method 2: Find classes through instances using explicit rdf:type
                ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?class .
              } UNION {
                # Method 3: Find classes that are explicitly declared as rdfs:Class or owl:Class
                ?class a <http://www.w3.org/2000/01/rdf-schema#Class> .
              } UNION {
                ?class a <http://www.w3.org/2002/07/owl#Class> .
              }
            }
            ORDER BY ?class
        """).strip()
        
        class_query = self._insert_from_clause(class_query, kg_name)
        classes = self.execute(class_query, format='compact')
        
        # Query for predicates
        predicate_query = textwrap.dedent("""
            SELECT DISTINCT ?predicate
            WHERE {
              ?s ?predicate ?o .
            }
            ORDER BY ?predicate
        """).strip()
        
        predicate_query = self._insert_from_clause(predicate_query, kg_name)
        predicates = self.execute(predicate_query, format='compact')

        # Extract URIs from compact format
        class_uris = classes.get('data', [])
        class_uris = [row[0] for row in class_uris if row]  # Get first column values
        
        predicate_uris = predicates.get('data', [])
        predicate_uris = [row[0] for row in predicate_uris if row]  # Get first column values
        
        # Filter out unwanted URIs from the schema
        # Exclude: RDF syntax namespace URIs (especially container properties like rdf:_1, rdf:_2, rdf:_5700, etc.)
        def should_exclude_uri(uri: str) -> bool:
            """
            Check if URI should be excluded from schema results.
            Returns True if the URI should be filtered out.
            """
            # Check if URI is from RDF syntax namespace
            rdf_namespace_prefixes = (
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'https://www.w3.org/1999/02/22-rdf-syntax-ns#'
            )
            
            for prefix in rdf_namespace_prefixes:
                if uri.startswith(prefix):
                    return True
            
            return False  # Don't exclude URIs from other namespaces
        
        class_data = [[uri] for uri in class_uris if not should_exclude_uri(uri)]
        predicate_data = [[uri] for uri in predicate_uris if not should_exclude_uri(uri)]
        
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

    # Extract just the KG short name from endpoint
    kg_short_name = sparql_server.kg_name if sparql_server.kg_name else "the"
    
    query_doc = f"""
Execute a SPARQL query against the {kg_short_name} knowledge graph endpoint: {sparql_server.endpoint_url}.

CRITICAL: Before using this tool or discussing the knowledge graph:
1. You MUST call get_description() FIRST to get the correct knowledge graph name and details
2. Until get_description() is called, refer to this knowledge graph ONLY as "{kg_short_name}" (the short label)
3. DO NOT invent or guess a full name - you will likely hallucinate incorrect information
4. After get_description() is called, you can use the proper name from the description

IMPORTANT: You MUST call get_schema() before making queries to understand available classes and predicates.

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
Return the schema (classes, relationships, properties) of the {kg_short_name} knowledge graph endpoint: {sparql_server.endpoint_url}.

CRITICAL: Before discussing the knowledge graph:
1. Call get_description() FIRST to get the correct knowledge graph name
2. Until then, refer to it ONLY as "{kg_short_name}" (the short label)
3. DO NOT invent or guess a full name

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
        - Strings after newline characters (e.g., truncates "ClassName\nextra" to "ClassName")
        
        Args:
            mermaid_content: The raw Mermaid class diagram content
            
        Returns:
            Cleaned Mermaid content with note statements, empty braces, and post-newline strings removed
        """
        import re
        
        # First, truncate any strings after \n characters in the entire content
        # This handles cases like "MEASURED_DIFFERENTIAL_METHYLATION_ASmMR\nmethylation_diff, q_value"
        mermaid_content = re.sub(r'(\S+)\\n[^\s\n]*', r'\1', mermaid_content)
        
        lines = mermaid_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Remove vertical bars, they are not allowed in class diagrams
            stripped = stripped.replace('|', ' ')
            
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

    # Add prompt to create chat transcripts
    @mcp.tool()
    def create_chat_transcript() -> str:
        """Prompt for creating a chat transcript in markdown format with user prompts and Claude responses."""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        return f"""Create a chat transcript in .md format following the outline below. Include prompts, text responses, and visualizations preferably inline, and when not possible as a link to a document.

## Chat Transcript
<Title>

👤 **User**  
<prompt>

---

🧠 **Assistant**  
<entire text response goes here>

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on {today}*
"""

    @mcp.tool()
    def visualize_schema() -> str:
        """Prompt for visualizing the knowledge graph schema using a Mermaid class diagram."""
        return """Visualize the knowledge graph schema using a Mermaid class diagram. 

CRITICAL WORKFLOW - Follow these steps exactly:
1. First call get_schema() if it has not been called to retrieve the classes and predicates
2. Generate the raw Mermaid class diagram showing:
   - Classes as nodes with their properties
   - Predicates/relationships as connections between classes
   - Include relationship labels
3. Do not append newline characters
4. MANDATORY: Pass your generated diagram through the clean_mermaid_diagram tool
5. MANDATORY: Use ONLY the cleaned output from step 3 in your response - do NOT use your original draft
6. Present the cleaned diagram inline in a mermaid code block

Common mistakes to avoid:
- DO NOT render the diagram before cleaning it
- DO NOT use your original draft after calling clean_mermaid_diagram
- DO NOT add note statements or empty curly braces {} for classes without properties
- ALWAYS copy the exact output from clean_mermaid_diagram tool
"""

    # Run MCP server over stdio
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()