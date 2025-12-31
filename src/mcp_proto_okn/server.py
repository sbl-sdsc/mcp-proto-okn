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
import re
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

from . import __version__

class QueryAnalyzer:
    """Analyzes SPARQL queries for common issues with LIMIT and ORDER BY."""
    
    def __init__(self, edge_predicates_with_props: Optional[set] = None):
        """Initialize with optional set of predicates that have edge properties."""
        self.edge_predicates_with_props = edge_predicates_with_props or set()
    
    def update_edge_predicates(self, predicates: set):
        """Update the set of predicates known to have edge properties."""
        self.edge_predicates_with_props = predicates
    
    @staticmethod
    def has_limit(query: str) -> Optional[int]:
        """Check if query has LIMIT clause and return the limit value."""
        match = re.search(r'\bLIMIT\s+(\d+)', query, re.IGNORECASE)
        return int(match.group(1)) if match else None
    
    @staticmethod
    def has_order_by(query: str) -> bool:
        """Check if query has ORDER BY clause."""
        return bool(re.search(r'\bORDER\s+BY\b', query, re.IGNORECASE))
    
    @staticmethod
    def extract_select_variables(query: str) -> List[str]:
        """Extract variable names from SELECT clause."""
        # Match SELECT ... WHERE/FROM pattern
        match = re.search(r'\bSELECT\s+(.*?)\s+(?:FROM|WHERE)', query, re.IGNORECASE | re.DOTALL)
        if not match:
            return []
        
        select_clause = match.group(1)
        # Find all ?variable patterns
        variables = re.findall(r'\?(\w+)', select_clause)
        return variables
    
    @staticmethod
    def suggest_order_by(query: str, numeric_vars: Optional[List[str]] = None) -> str:
        """
        Suggest an ORDER BY clause based on query context.
        
        Args:
            query: The SPARQL query string
            numeric_vars: Optional list of variable names that are numeric
        
        Returns:
            Suggested ORDER BY clause or empty string
        """
        variables = QueryAnalyzer.extract_select_variables(query)
        
        if not variables:
            return ""
        
        # Priority for sorting suggestions:
        # 1. Numeric variables (concentration, count, value, etc.)
        # 2. First non-subject variable
        
        numeric_keywords = ['concentration', 'count', 'value', 'amount', 'level', 
                          'score', 'rank', 'number', 'total', 'sum', 'avg', 'max', 'min',
                          'p_value', 'pvalue', 'log2fc', 'fc', 'fold']
        
        # Check for numeric variable names
        for var in variables:
            var_lower = var.lower()
            if any(keyword in var_lower for keyword in numeric_keywords):
                return f"ORDER BY DESC(?{var})"
        
        # Check if numeric_vars hint provided
        if numeric_vars:
            for var in variables:
                if var in numeric_vars:
                    return f"ORDER BY DESC(?{var})"
        
        # Default: sort by first variable that isn't a subject/entity
        if len(variables) > 1:
            return f"ORDER BY DESC(?{variables[1]})"
        
        return ""
    
    def _analyze_edge_property_access(self, query: str) -> str:
        """
        Check if query might be trying to access edge properties incorrectly.
        Returns warning string if issues detected, empty string otherwise.
        """
        if not self.edge_predicates_with_props:
            # No edge property metadata available yet
            return ""
        
        # Check if query uses RDF reification pattern
        has_reification = bool(re.search(
            r'rdf:subject.*rdf:predicate.*rdf:object', 
            query, 
            re.IGNORECASE | re.DOTALL
        ))
        
        # Check if query references any predicates known to have edge properties
        predicates_in_query = []
        for predicate in self.edge_predicates_with_props:
            # Match both URI and label forms
            predicate_pattern = re.escape(str(predicate))
            if re.search(predicate_pattern, query, re.IGNORECASE):
                predicates_in_query.append(predicate)
        
        # If query uses edge predicates but not reification pattern, warn
        if predicates_in_query and not has_reification:
            predicate_names = ', '.join(str(p).split('/')[-1] for p in predicates_in_query[:3])
            if len(predicates_in_query) > 3:
                predicate_names += f", and {len(predicates_in_query) - 3} more"
            
            return (
                f"\n⚠️  Detected relationship(s) with edge properties: {predicate_names}\n"
                "These relationships store data ON the relationship itself (e.g., log2fc, p-values).\n"
                "To access edge properties, use the RDF reification pattern:\n"
                "  ?stmt rdf:subject ?source ;\n"
                "        rdf:predicate schema:RELATIONSHIP_NAME ;\n"
                "        rdf:object ?target ;\n"
                "        schema:property_name ?value .\n"
                "Check the schema's edge_properties section for query templates."
            )
        
        return ""
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze a SPARQL query for potential issues.
        
        Returns a dict with:
            - has_limit: bool
            - limit_value: int or None
            - has_order_by: bool
            - needs_order_by: bool (True if LIMIT without ORDER BY)
            - suggested_order: str (suggested ORDER BY clause)
            - warning: str (warning message if issues found)
            - edge_property_warning: str (warning if edge properties not accessed correctly)
        """
        limit_val = QueryAnalyzer.has_limit(query)
        has_order = QueryAnalyzer.has_order_by(query)
        
        analysis = {
            'has_limit': limit_val is not None,
            'limit_value': limit_val,
            'has_order_by': has_order,
            'needs_order_by': limit_val is not None and not has_order,
            'suggested_order': '',
            'warning': '',
            'edge_property_warning': ''
        }
        
        # Check for LIMIT without ORDER BY
        if analysis['needs_order_by']:
            analysis['suggested_order'] = QueryAnalyzer.suggest_order_by(query)
            analysis['warning'] = (
                f"⚠️  Query uses LIMIT {limit_val} without ORDER BY. "
                "This returns arbitrary results, not the 'top N'. "
                f"Consider adding: {analysis['suggested_order']}"
            )
        
        # Check for edge property access (generic)
        edge_property_analysis = self._analyze_edge_property_access(query)
        if edge_property_analysis:
            analysis['edge_property_warning'] = edge_property_analysis
            if analysis['warning']:
                analysis['warning'] += '\n' + edge_property_analysis
            else:
                analysis['warning'] = edge_property_analysis
        
        return analysis


class SPARQLServer:
    """SPARQL endpoint wrapper with Proto-OKN/registry awareness."""

    def __init__(self, endpoint_url: str, description: Optional[str] = None):
        self.endpoint_url = endpoint_url
        self.description = description  # None means: try to infer
        self.github_base_url = "https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/metadata/entities"
        
        # Track schema state
        self._schema_fetched = False
        self._edge_properties_cache = {}  # Cache edge property metadata
        self._edge_predicates_with_props = set()  # Set of predicate URIs/labels that have edge properties
        
        # Initialize analyzer (will be updated after schema is fetched)
        self.analyzer = QueryAnalyzer(edge_predicates_with_props=set())

        # Extract KG name from endpoint URL during initialization
        self.kg_name, self.registry_url = self._get_registry_url()

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
            return "", ""

        path_parts = urlparse(self.endpoint_url).path.strip("/").split("/")
        kg_name = path_parts[-2] if len(path_parts) >= 2 else "unknown"

        registry_url = (
            "https://raw.githubusercontent.com/frink-okn/okn-registry/"
            "refs/heads/main/docs/registry/kgs/"
            f"{kg_name}.md"
        )
        #self.registry_url = registry_url
        #self.kg_name = kg_name
        return kg_name, registry_url

    def _fetch_registry_content(self) -> Optional[str]:
        """Fetch registry page content in markdown format or None on failure."""
        try:
            if not self.registry_url:
                return None

            with urlopen(self.registry_url, timeout=5) as resp:
                raw = resp.read()
                text = raw.decode("utf-8", errors="replace")
                return text.strip()
        except Exception:
            return None

    def _get_entity_metadata(self) -> Dict[str, Dict[str, str]]:
        """
        Fetch entity metadata from GitHub CSV file.
        Returns a dict mapping URI to {label, description, type, edge_property_of, source_class, target_class}.
        """
        if not self.registry_url:
            return {}
    
        filename = f"{self.kg_name}_entities.csv"
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
                edge_property_of = row.get('EdgePropertyOf', '').strip()
                source_class = row.get('SourceClass', '').strip()
                target_class = row.get('TargetClass', '').strip()
                
                if uri:
                    metadata[uri] = {
                        'label': label,
                        'description': description,
                        'type': entity_type,
                        'edge_property_of': edge_property_of,
                        'source_class': source_class,
                        'target_class': target_class
                    }
            
            return metadata
            
        except Exception as e:
            # If file doesn't exist or any error occurs, return empty dict
            return {}

    def execute(self, query_string: str, format: str = 'compact', analyze: bool = True) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """Execute SPARQL query and return results in requested format.
        
        Args:
            query_string: The SPARQL query to execute
            format: Output format (compact, simplified, full, values, csv)
            analyze: If True, analyze query for common issues (LIMIT without ORDER BY)
        
        Returns:
            Query results in the requested format, with optional query_analysis field
        """
        # Analyze query before execution if requested
        analysis = None
        warnings = []
        
        # Warn if schema hasn't been fetched
        if not self._schema_fetched and analyze:
            warnings.append({
                "type": "schema_not_fetched",
                "message": (
                    "⚠️  RECOMMENDATION: Call get_schema() before querying to understand "
                    "the knowledge graph structure, especially for edge properties."
                )
            })
        
        if analyze:
            analysis = self.analyzer.analyze_query(query_string)
        
        # Get kg_name for FROM clause insertion for federated endpoint
        if self.kg_name != '':
            query_string = self._insert_from_clause(query_string, self.kg_name)
        
        self.sparql.setQuery(query_string)
        
        try:
            raw_result = self.sparql.query().convert()
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            # Add analysis warning to error message if applicable
            if analysis and analysis.get('warning'):
                error_msg += f"\n\n{analysis['warning']}"
            return {
                'error': error_msg,
                'query': query_string
            }
        
        # Apply requested format
        if format == 'full':
            formatted_result = raw_result
        elif format == 'simplified':
            formatted_result = self._simplify_result(raw_result)
        elif format == 'compact':
            formatted_result = self._compact_result(raw_result)
        elif format == 'values':
            formatted_result = self._values_only(raw_result)
        elif format == 'csv':
            formatted_result = self._to_csv(raw_result)
        else:
            formatted_result = self._compact_result(raw_result)
        
        # Add analysis warnings to result if applicable
        if analyze and analysis and analysis.get('warning'):
            if isinstance(formatted_result, dict):
                formatted_result['query_analysis'] = {
                    'warning': analysis['warning'],
                    'suggested_order': analysis['suggested_order'],
                    'limit_value': analysis['limit_value']
                }
            elif isinstance(formatted_result, str):
                # For CSV format, prepend warning as comment
                formatted_result = f"# {analysis['warning']}\n{formatted_result}"
        
        # Add schema warnings if present
        if warnings and isinstance(formatted_result, dict):
            if 'query_analysis' in formatted_result:
                formatted_result['query_analysis']['schema_warnings'] = warnings
            else:
                formatted_result['schema_warnings'] = warnings
        
        return formatted_result

    def _generate_query_template(self, relationship_label: str, source_class: str, target_class: str, properties: List[Dict]) -> str:
        """Generate a SPARQL query template for a reified relationship with edge properties."""
        
        source_var = source_class.lower() if source_class else 'source'
        target_var = target_class.lower() if target_class else 'target'
        
        # Build property selects and patterns
        prop_selects = []
        prop_patterns = []
        
        for prop in properties:
            prop_label = prop['label']
            prop_selects.append(f"?{prop_label}")
            prop_patterns.append(f"         schema:{prop_label} ?{prop_label} ;")
        
        # Remove trailing semicolon from last pattern
        if prop_patterns:
            prop_patterns[-1] = prop_patterns[-1].rstrip(' ;') + ' .'
        
        template = f"""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>

SELECT ?{source_var} ?{target_var} {' '.join(prop_selects)}
WHERE {{
  ?stmt rdf:subject ?{source_var} ;
        rdf:predicate schema:{relationship_label} ;
        rdf:object ?{target_var} ;
{chr(10).join(prop_patterns)}
}}
LIMIT 10"""
        
        return template

    def query_schema(self, compact: bool = True) -> Dict[str, Any]:
        """
        Query the knowledge graph schema to discover classes and predicates.
        
        Args:
            compact: If True, returns just URIs. If False, enriches with labels and descriptions.
        
        Returns:
            A dictionary with 'classes', 'predicates', 'edge_properties', and 'node_properties' keys.
        """
        if not self.registry_url:
            return {
                'error': 'Cannot determine KG name for schema query',
                'classes': {'columns': ['uri'], 'data': [], 'count': 0},
                'predicates': {'columns': ['uri'], 'data': [], 'count': 0},
                'edge_properties': {},
                'node_properties': {'columns': ['uri'], 'data': [], 'count': 0}
            }
        
        kg_name = self.kg_name

        # Try to get metadata from GitHub CSV first
        entity_metadata = self._get_entity_metadata()
        
        # If we have metadata, use it to build the schema
        if entity_metadata:
            # Separate entities by type
            classes = []
            predicates = []
            edge_properties_dict = {}
            node_properties = []
            
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
                    # Extract the short name from the URI (last part after the final slash)
                    short_name = uri.split('/')[-1] if '/' in uri else uri
                    predicates.append({
                        'uri': uri,
                        'short_name': short_name,  # Add short name for matching
                        'label': metadata.get('label', ''),
                        'description': metadata.get('description', ''),
                        'type': metadata.get('type', ''),
                        'source_class': metadata.get('source_class', ''),
                        'target_class': metadata.get('target_class', ''),
                        'has_edge_properties': False  # Will be updated below
                    })
                elif entity_type == 'edgeproperty':
                    parent_relationships = metadata.get('edge_property_of', '')
                    
                    # BUGFIX: Edge properties can belong to multiple relationships (semicolon-separated)
                    # Split on semicolon and process each relationship separately
                    if parent_relationships:
                        # Split on semicolon and strip whitespace from each relationship name
                        relationship_list = [rel.strip() for rel in parent_relationships.split(';') if rel.strip()]
                        
                        for parent_relationship in relationship_list:
                            if parent_relationship not in edge_properties_dict:
                                edge_properties_dict[parent_relationship] = []
                            
                            edge_properties_dict[parent_relationship].append({
                                'uri': uri,
                                'label': metadata.get('label', ''),
                                'description': metadata.get('description', ''),
                                'type': metadata.get('type', '')
                            })
                elif entity_type == 'nodeproperty':
                    node_properties.append({
                        'uri': uri,
                        'label': metadata.get('label', ''),
                        'description': metadata.get('description', ''),
                        'type': metadata.get('type', ''),
                        'class': metadata.get('source_class', '')
                    })
            
            # Mark predicates that have edge properties
            # BUGFIX: Match using short_name (e.g., "TREATS_CtD") not label (e.g., "Treats (Compound treats Disease)")
            for pred in predicates:
                pred_short_name = pred['short_name']
                if pred_short_name in edge_properties_dict:
                    pred['has_edge_properties'] = True
            
            # Build edge properties output with relationship metadata
            edge_properties_output = {}
            for relationship_label, properties in edge_properties_dict.items():
                # Find the full relationship metadata using short_name
                rel_metadata = next((p for p in predicates if p['short_name'] == relationship_label), None)
                
                if rel_metadata:
                    edge_properties_output[relationship_label] = {
                        'uri': rel_metadata['uri'],
                        'label': relationship_label,
                        'description': rel_metadata['description'],
                        'source_class': rel_metadata['source_class'],
                        'target_class': rel_metadata['target_class'],
                        'properties': properties,
                        'query_template': self._generate_query_template(
                            relationship_label, 
                            rel_metadata['source_class'],
                            rel_metadata['target_class'],
                            properties
                        )
                    }
            
            # Cache edge property information and update analyzer
            self._edge_properties_cache = edge_properties_output
            predicates_with_props = set()
            for relationship_label, edge_info in edge_properties_output.items():
                # Add both URI and label
                predicates_with_props.add(edge_info['uri'])
                predicates_with_props.add(relationship_label)
            
            self._edge_predicates_with_props = predicates_with_props
            self.analyzer.update_edge_predicates(predicates_with_props)
            self._schema_fetched = True
            
            # Add edge property summary if not compact
            if not compact:
                edge_prop_summary = {
                    "CRITICAL_NOTE": (
                        "Some relationships have edge properties (data stored on the relationship itself). "
                        "To query these, use the RDF reification pattern shown in each edge's query_template."
                    ),
                    "edges_with_properties": []
                }
                
                for relationship_label, edge_info in edge_properties_output.items():
                    edge_prop_summary["edges_with_properties"].append({
                        "relationship": relationship_label,
                        "uri": edge_info['uri'],
                        "properties": [
                            {
                                "name": p.get("label", ""),
                                "type": p.get("description", "").split("(")[-1].rstrip(")")
                            } 
                            for p in edge_info.get("properties", [])
                        ],
                        "example_query": edge_info.get("query_template", "")
                    })
            
            # Build response with full metadata
            class_data = [[c['uri'], c['label'], c['description'], c['type']] for c in classes]
            predicate_data = [[p['uri'], p['label'], p['description'], p['type'], p['source_class'], p['target_class'], p['has_edge_properties']] for p in predicates]
            node_property_data = [[n['uri'], n['label'], n['description'], n['type'], n['class']] for n in node_properties]
            
            result = {
                'classes': {
                    'columns': ['uri', 'label', 'description', 'type'],
                    'data': class_data,
                    'count': len(class_data)
                },
                'predicates': {
                    'columns': ['uri', 'label', 'description', 'type', 'source_class', 'target_class', 'has_edge_properties'],
                    'data': predicate_data,
                    'count': len(predicate_data)
                },
                'edge_properties': edge_properties_output,
                'node_properties': {
                    'columns': ['uri', 'label', 'description', 'type', 'class'],
                    'data': node_property_data,
                    'count': len(node_property_data)
                }
            }
            
            # Prepend summary to result if not compact
            if not compact and edge_properties_output:
                result = {
                    "edge_property_summary": edge_prop_summary,
                    **result
                }
            
            return result
        
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
        
        class_query = self._insert_from_clause(class_query, self.kg_name)
        classes = self.execute(class_query, format='compact')
        
        # Query for predicates
        predicate_query = textwrap.dedent("""
            SELECT DISTINCT ?predicate
            WHERE {
              ?s ?predicate ?o .
            }
            ORDER BY ?predicate
        """).strip()
        
        predicate_query = self._insert_from_clause(predicate_query, self.kg_name)
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
            },
            'edge_properties': {},
            'node_properties': {
                'columns': ['uri'],
                'data': [],
                'count': 0
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
    
    def get_edge_property_info(self, predicate_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about edge properties for a specific predicate.
        
        Args:
            predicate_name: Name or URI of the predicate
        
        Returns:
            Dict with edge property information or None if not found
        """
        # Search by exact match first (by label)
        if predicate_name in self._edge_properties_cache:
            return self._edge_properties_cache[predicate_name]
        
        # Search by URI
        for label, info in self._edge_properties_cache.items():
            if info.get("uri") == predicate_name:
                return info
        
        # Search by partial match
        predicate_lower = predicate_name.lower()
        for label, info in self._edge_properties_cache.items():
            uri = info.get("uri", "")
            if predicate_lower in uri.lower() or predicate_lower in label.lower():
                return info
        
        return None

    def get_relationship_template(self, relationship_name: str) -> str:
        """
        Get a query template for a specific relationship.
        
        Args:
            relationship_name: Name of the relationship
        
        Returns:
            A ready-to-use SPARQL query template, or error message if not found
        """
        edge_info = self.get_edge_property_info(relationship_name)
        
        if not edge_info:
            return f"Relationship '{relationship_name}' not found in schema or has no edge properties."
        
        if "query_template" in edge_info:
            return edge_info["query_template"]
        
        # Generate a basic template if none exists
        properties = edge_info.get("properties", [])
        prop_vars = "\n         ".join(f"schema:{p['label']} ?{p['label']} ;" for p in properties)
        label = edge_info.get("label", relationship_name)
        source_class = edge_info.get("source_class", "source")
        target_class = edge_info.get("target_class", "target")
        
        return f"""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <https://purl.org/okn/frink/kg/{self.kg_name}/schema/>

SELECT ?{source_class.lower()} ?{target_class.lower()} {' '.join('?' + p['label'] for p in properties)}
WHERE {{
  ?stmt rdf:subject ?{source_class.lower()} ;
        rdf:predicate schema:{label} ;
        rdf:object ?{target_class.lower()} ;
        {prop_vars.rstrip(' ;')} .
}}
LIMIT 10"""
    
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
Execute a SPARQL query against the {sparql_server.kg_name} knowledge graph endpoint: {sparql_server.endpoint_url}.

⚠️ CRITICAL WORKFLOW - ALWAYS FOLLOW THIS ORDER:
1. If you haven't already, call get_schema() FIRST to understand the data structure
2. Check the schema's edge_properties section for relationships with properties
3. Construct your query using the appropriate pattern

CRITICAL: Before using this tool or discussing the knowledge graph:
1. You MUST call get_description() FIRST to get the correct knowledge graph name and details
2. Until get_description() is called, refer to this knowledge graph ONLY as "{sparql_server.kg_name}" (the short label)
3. DO NOT invent or guess a full name - you will likely hallucinate incorrect information
4. After get_description() is called, you can use the proper name from the description

EDGE PROPERTIES - CRITICAL:
Many relationships in this knowledge graph have properties stored as edge attributes (data ON the relationship itself).
Examples include: log2fc, adj_p_value, methylation_diff, q_value, etc.

To query edge properties, you MUST use the RDF reification pattern:
```sparql
?stmt rdf:subject ?source ;
      rdf:predicate schema:RELATIONSHIP_NAME ;
      rdf:object ?target ;
      schema:property_name ?value .
```

The schema provides query_template for all edges with properties. USE THEM as examples!
Check the edge_properties section in the schema output to see which relationships have properties.

⚠️ CRITICAL QUERY CONSTRUCTION RULES FOR TOP N QUERIES:

When the user asks for "top N", "highest", "lowest", "maximum", "minimum", or ranked results:
1. ALWAYS use ORDER BY before LIMIT
2. Use DESC for highest/maximum values: ORDER BY DESC(?variable) LIMIT N
3. Use ASC for lowest/minimum values: ORDER BY ASC(?variable) LIMIT N

Examples:
- "Top 3 highest concentrations":
  SELECT ?location ?concentration WHERE {{ ... }} ORDER BY DESC(?concentration) LIMIT 3
  
- "5 lowest poverty rates":
  SELECT ?county ?rate WHERE {{ ... }} ORDER BY ASC(?rate) LIMIT 5

WITHOUT ORDER BY, LIMIT RETURNS ARBITRARY RESULTS, NOT THE TOP/BOTTOM N!

Args:
    query_string: A valid SPARQL query string
    format: Output format - 'simplified' (default, JSON with dict rows), 'compact' (columns + data arrays, no repeated keys), 'full' (complete SPARQL JSON), 'values' (list of dicts), or 'csv' (CSV string)
    analyze: If True (default), analyzes query and warns if LIMIT is used without ORDER BY, and checks for edge property issues

Returns:
    The query results in the specified format. If analyze=True and issues are detected, includes a 'query_analysis' field with warnings and suggestions.
"""

    @mcp.tool(description=query_doc)
    def query(query_string: str, format: str = 'compact', analyze: bool = True) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        return sparql_server.execute(query_string, format=format, analyze=analyze)

    schema_doc = f"""
Return the schema (classes, relationships, properties) of the {sparql_server.kg_name} knowledge graph endpoint: {sparql_server.endpoint_url}.

CRITICAL: Before discussing the knowledge graph:
1. Call get_description() FIRST to get the correct knowledge graph name
2. Until then, refer to it ONLY as "{sparql_server.kg_name}" (the short label)
3. DO NOT invent or guess a full name

IMPORTANT: Always call this tool FIRST before making any queries to understand what data is available in the knowledge graph.

WHAT THIS RETURNS:
- classes: Node types in the knowledge graph (entities like Gene, Study, Assay, etc.)
- predicates: Relationships between nodes
- edge_properties: Relationships that have data stored ON the relationship itself
  (these require special RDF reification pattern - see query templates in the output)
- node_properties: Attributes stored directly on nodes

⚠️ CRITICAL: Many queries fail because users don't check edge_properties!
Relationships with edge properties store quantitative data ON the relationship itself.
Examples: log2fc, adj_p_value, methylation_diff, q_value

Each edge property entry includes:
- A list of properties with their data types
- A query_template showing the exact RDF reification pattern to use
- USE THESE TEMPLATES as examples for your queries!

Args:
    compact: If True (default), returns compact URI:label mappings. If False, returns full metadata with descriptions and edge_property_summary.

Returns:
    The schema in the specified format, including critical edge_properties section
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

    # Add tool to get query templates for relationships with edge properties
    @mcp.tool()
    def get_query_template(relationship_name: str) -> str:
        """Get a query template for a specific relationship, especially useful for edges with properties.
        
        This is a generic tool that works with any knowledge graph. It retrieves the
        appropriate query template based on the schema, not hardcoded relationships.
        
        Use this when you need an example of how to query a relationship that has edge properties
        (like MEASURED_DIFFERENTIAL_EXPRESSION, MEASURED_DIFFERENTIAL_METHYLATION, etc.).
        
        Args:
            relationship_name: Name of the relationship (e.g., 'MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG')
        
        Returns:
            A ready-to-use SPARQL query template showing the RDF reification pattern for this relationship
        """
        return sparql_server.get_relationship_template(relationship_name)

    # Add tool to clean Mermaid diagrams
    @mcp.tool()
    def clean_mermaid_diagram(mermaid_content: str) -> str:
        """Clean a Mermaid class diagram by removing unwanted elements.
        
        This tool removes:
        - All note statements that would render as unreadable yellow boxes
        - Empty curly braces from class definitions (handles both single-line and multi-line)
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
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Remove vertical bars, they are not allowed in class diagrams
            stripped = stripped.replace('|', ' ')
            
            # Skip any line containing note syntax
            if (stripped.startswith('note ') or 
                'note for' in stripped or 
                'note left' in stripped or 
                'note right' in stripped):
                i += 1
                continue
            
            # Check for empty class definitions (single-line format)
            # Match patterns like: "class ClassName {     }" or "class ClassName { }"
            if re.match(r'^\s*class\s+\w+\s*\{\s*\}\s*$', line):
                # Replace the line with just the class name without braces
                line = re.sub(r'^(\s*class\s+\w+)\s*\{\s*\}\s*$', r'\1', line)
                cleaned_lines.append(line)
                i += 1
                continue
            
            # Check for empty class definitions (multi-line format)
            # Match: "class ClassName {" followed by "}" on next line(s)
            if re.match(r'^\s*class\s+\w+\s*\{\s*$', line):
                # Look ahead to check if next non-empty line is just "}"
                j = i + 1
                found_closing = False
                has_content = False
                
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line:  # Empty line, skip
                        j += 1
                        continue
                    if next_line == '}':  # Found closing brace
                        found_closing = True
                        break
                    else:  # Found content between braces
                        has_content = True
                        break
                
                if found_closing and not has_content:
                    # This is an empty class definition - remove the braces
                    class_match = re.match(r'^(\s*class\s+\w+)\s*\{\s*$', line)
                    if class_match:
                        cleaned_lines.append(class_match.group(1))
                    # Skip ahead past the closing brace
                    i = j + 1
                    continue
            
            cleaned_lines.append(line)
            i += 1
        
        return '\n'.join(cleaned_lines)

    # Add prompt to create chat transcripts
    @mcp.tool()
    def create_chat_transcript() -> str:
        """Prompt for creating a chat transcript in markdown format with user prompts and Claude responses."""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
    
        return f"""Create a chat transcript in .md format following the outline below. 
1. Include prompts, text responses, and visualizations preferably inline, and when not possible as a link to a document. 
2. Include mermaid diagrams inline. Do not link to the mermaid file.
3. Do not include the prompt to create this transcript.
4. Save the transcript to ~/Downloads/<descriptive-filename>.md

## Chat Transcript
<Title>

👤 **User**  
<prompt>

---

🧠 **Assistant**  
<entire text response goes here>


*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) {__version__} on {today}*

IMPORTANT: 
- After the footer above, add a line with the model string you are using).
- Save the complete transcript to ~/Downloads/ with a descriptive filename (e.g., ~/Downloads/{sparql_server.kg_name}-chat-transcript-{today}.md)
- Use the present_files tool to share the transcript file with the user.
"""

    @mcp.tool()
    def visualize_schema() -> str:
        """Prompt for visualizing the knowledge graph schema using a Mermaid class diagram."""
        return """Visualize the knowledge graph schema using a Mermaid class diagram. 

CRITICAL WORKFLOW - Follow these steps EXACTLY IN ORDER:

STEP 1-5: Generate Draft Diagram
1. First call get_schema() if it has not been called to retrieve the classes and predicates
2. Analyze the schema to identify:
   - Node classes (entities like Gene, Study, Assay, etc.)
   - Edge predicates (relationships between nodes)
   - Edge properties (predicates that describe data types like float, int, string, boolean, date, etc.)
3. Generate the raw Mermaid class diagram showing:
   - All node classes with their properties
   - For edges WITHOUT properties: show as labeled arrows between classes (e.g., `Mission --> Study : CONDUCTED_MIcS`)
   - For edges WITH properties: represent the edge as an intermediary class containing the properties, with unlabeled arrows connecting source → edge class → target
4. Make the diagram taller / less wide:
   - Set the diagram direction to TB (top→bottom): `direction TB`
5. Do not append newline characters

⚠️  STEP 6-9: MANDATORY CLEANING - CANNOT BE SKIPPED ⚠️
6. STOP HERE! You now have a draft diagram. DO NOT use it yet.
7. Call clean_mermaid_diagram and pass your draft diagram as the parameter
8. Wait for the tool to return the cleaned diagram
9. Your draft is now OBSOLETE. Delete it from your mind. You will use ONLY the cleaned output.

STEP 10-13: Present ONLY the Cleaned Diagram
10. Copy the EXACT text returned by clean_mermaid_diagram (not your draft)
11. Present this CLEANED diagram inline in a mermaid code block
12. Create a .mermaid file with ONLY the CLEANED diagram code (no markdown fences)
13. Save to /mnt/user-data/outputs/<kg_name>-schema.mermaid and call present_files

⛔ STOP AND CHECK - Before you respond to the user:
□ Did I call clean_mermaid_diagram? If NO → Go back and call it now
□ Am I using the cleaned output? If NO → Replace with cleaned output
□ Does my diagram contain empty {} braces? If YES → You're using your draft, use cleaned output
□ Did I call present_files? If NO → Call it now

EDGES WITH PROPERTIES - CRITICAL GUIDELINES:
- When an edge predicate has associated properties (e.g., log2fc, adj_p_value), DO NOT use a separate namespace
- Instead, represent the edge as an intermediary class with the original predicate name
- Connect the source class to the edge class, then the edge class to the target class
- Example: Instead of `Assay --> Gene : MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG` with a separate EdgeProperties namespace,
  create:
    class MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG {
        float log2fc
        float adj_p_value
    }
    Assay --> MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG
    MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG --> Gene
- This approach clearly shows that the properties belong to the relationship itself

RENDERING REQUIREMENTS:
- The .mermaid file MUST contain ONLY the Mermaid diagram code
- DO NOT include markdown code fences (```mermaid) in the .mermaid file
- DO NOT include any explanatory text in the .mermaid file
- The file should start with "classDiagram" and contain only the diagram definition
- ALWAYS use present_files to share the .mermaid file after creating it

❌ COMMON MISTAKES - These will cause errors:
- Using your draft diagram instead of the cleaned output from clean_mermaid_diagram
- Not calling clean_mermaid_diagram at all
- Calling clean_mermaid_diagram but then using your original draft anyway
- Including empty curly braces {} for classes without properties (the cleaner removes these)
- Not calling present_files to share the final .mermaid file
- Using a separate EdgeProperties namespace instead of intermediary classes
"""

    # Run MCP server over stdio
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()