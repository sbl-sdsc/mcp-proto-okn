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

Transport modes:
  - stdio (default): For local subprocess use via ``uvx mcp-proto-okn``.
  - streamable-http: For remote deployment over HTTP/HTTPS.

Environment variables (HTTP transport):
  MCP_PROTO_OKN_TRANSPORT  - "stdio" (default) or "streamable-http"
  MCP_PROTO_OKN_HOST       - Bind address (default "0.0.0.0")
  MCP_PROTO_OKN_PORT       - Bind port (default 8000)
  MCP_PROTO_OKN_API_KEY    - Optional Bearer-token authentication
"""

import os
import sys
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
    
    # Maximum number of URIs in a VALUES clause before triggering batched execution
    # Large VALUES clauses can cause 403 errors or timeouts
    MAX_VALUES_PER_BATCH = 20

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
        self.sparql.setTimeout(300)
#        self.sparql.setTimeout(120)

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

    def _detect_ontology_uris(self, query_string: str) -> List[str]:
        """
        Detect ontology URIs in a SPARQL query that should be expanded to include descendants.
        
        Detects URIs from all Ubergraph namespace prefixes, including:
        - OBO Foundry ontologies (MONDO, DOID, HP, GO, UBERON, CL, CHEBI, PR, SO, etc.)
        - Additional biological ontologies (ChEBI, Uberon, EMAPA, FBBT, etc.)
        - Gene nomenclature (Bird Gene Nomenclature)
        - Other semantic web vocabularies present in Ubergraph
        
        Args:
            query_string: The SPARQL query string
            
        Returns:
            List of ontology URIs found in the query
        """
        # Define all namespace prefixes present in Ubergraph
        # These prefixes were identified by querying the Ubergraph endpoint
        namespace_prefixes = [
            # All OBO patterns combined:
            # - Base OBO: PREFIX_DIGITS (e.g., MONDO_0005178, GO_0008150)
            # - Hash properties: ontology#property (e.g., chebi#has_functional_parent)
            # - Uberon core: uberon/core#property
            # - ChEBI slash: chebi/property
            r'http://purl\.obolibrary\.org/obo/(?:[A-Z]+_\d+|(?:chebi|emapa|fbbt|fypo|HAO|ma|mondo|nbo|ncbitaxon|pato|pr|so|vbo)#[A-Za-z_]+|uberon/core#[A-Za-z_]+|chebi/[A-Za-z_]+)',
            
            # Gene nomenclature
            r'http://birdgenenames\.org/cgnc/GeneReport\?id=\d+',
            
            # Other semantic web vocabularies (if they contain hierarchical concepts)
            # Note: Not all of these will have rdfs:subClassOf relationships
            # but we include them for completeness
            r'http://www\.w3\.org/2002/07/owl#[A-Za-z]+',
        ]
        
        detected_uris = []
        
        # Extract URIs in angle brackets for each prefix pattern
        for prefix_pattern in namespace_prefixes:
            uri_pattern = f'<({prefix_pattern})>'
            matches = re.findall(uri_pattern, query_string)
            detected_uris.extend(matches)
        
        return list(set(detected_uris))  # Remove duplicates
    
    def _fetch_descendants_for_uri(self, uri: str, max_results: int = 2000, max_depth: int = 5) -> List[str]:
        """
        Fetch descendant URIs for a given ontology URI using the ubergraph,
        with depth limiting to avoid runaway traversals.
        
        Uses a bounded property path (up to max_depth hops) instead of unbounded
        rdfs:subClassOf* to prevent timeouts on large ontologies.
        
        Args:
            uri: The ontology URI to expand
            max_results: Maximum number of descendants to retrieve
            max_depth: Maximum number of subClassOf hops to traverse (default: 5)
            
        Returns:
            List of descendant URIs (including the original URI)
        """
        # Build a depth-limited query using UNION of explicit path lengths.
        # This avoids unbounded rdfs:subClassOf* which can timeout on large ontologies.
        # Each UNION branch adds one more hop: ?d subClassOf ?mid1 . ?mid1 subClassOf <uri> etc.
        depth_patterns = []
        for depth in range(1, max_depth + 1):
            if depth == 1:
                depth_patterns.append(f"{{ ?descendant rdfs:subClassOf <{uri}> }}")
            else:
                # Chain: ?descendant -> ?m1 -> ?m2 -> ... -> <uri>
                chain_parts = []
                prev_var = "?descendant"
                for i in range(1, depth):
                    next_var = f"?_mid{i}"
                    chain_parts.append(f"{prev_var} rdfs:subClassOf {next_var} .")
                    prev_var = next_var
                chain_parts.append(f"{prev_var} rdfs:subClassOf <{uri}> .")
                depth_patterns.append("{ " + " ".join(chain_parts) + " }")
        
        union_block = "\n    UNION\n    ".join(depth_patterns)
        
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?descendant
        FROM <https://purl.org/okn/frink/kg/ubergraph>
        WHERE {{
          {{
            {union_block}
          }}
        }}
        LIMIT {max_results}
        """
        
        try:
            # Execute directly against the federated endpoint to avoid recursion
            self.sparql.setQuery(query)
            raw_result = self.sparql.query().convert()
            
            # Use the existing _extract_values method
            desc_uris = self._extract_values(raw_result, 'descendant')
            # Filter out the original URI and include it at the start
            descendants = [uri] + [d for d in desc_uris if d and d != uri]
            
            return descendants[:max_results]
        except Exception as e:
            # If expansion fails, just return the original URI
            return [uri]
    
    def _expand_query_with_descendants(self, query_string: str, ontology_uris: List[str], max_descendants: int = 100, max_depth: int = 5, bind_variables: Optional[List[str]] = None) -> Tuple[Union[str, List[str]], Dict[str, List[str]]]:
        """
        Rewrite a SPARQL query to include descendants of detected ontology URIs.
        
        Pre-fetches descendants from the ubergraph (with depth limiting) and injects
        them as VALUES clauses into the user's query. This approach works correctly
        across named graphs — the ubergraph is queried separately for the hierarchy,
        then the expanded URI list is used in the KG-specific query.
        
        When the total number of expanded URIs exceeds MAX_VALUES_PER_BATCH, this method
        returns a list of batched queries instead of a single query string.
        
        Args:
            query_string: Original SPARQL query
            ontology_uris: List of ontology URIs detected in the query
            max_descendants: Maximum descendants to fetch per URI
            max_depth: Maximum hierarchy depth to traverse (default: 5)
            bind_variables: Optional list of variable names (with or without '?') that should
                           be constrained to the expanded ontology concepts. For example, if
                           you expand mondo:0005578 and want ?disease to only match those
                           concepts, pass bind_variables=['disease'] or ['?disease'].
                           This is useful for GROUP BY queries where you want to count/aggregate
                           per descendant rather than just filter datasets.
            
        Returns:
            Tuple of (expanded_query_or_queries, uri_to_descendants_mapping)
            where expanded_query_or_queries is either:
            - A single query string (if total URIs <= MAX_VALUES_PER_BATCH)
            - A list of query strings (if batching is required)
        """
        if not ontology_uris:
            return query_string, {}
        
        # Normalize bind_variables (ensure they start with ?)
        bind_vars = []
        if bind_variables:
            bind_vars = [v if v.startswith('?') else f'?{v}' for v in bind_variables]
        
        uri_to_descendants = {}
        var_to_descendants = {}  # Map variable names to their descendant lists
        
        # Fetch all descendants first
        for uri in ontology_uris:
            descendants = self._fetch_descendants_for_uri(uri, max_results=max_descendants, max_depth=max_depth)
            uri_to_descendants[uri] = descendants
            
            if len(descendants) <= 1:
                # No descendants found (or just the original URI), skip expansion
                continue
            
            # Create a unique variable name based on the URI identifier
            uri_id = uri.split('_')[-1] if '_' in uri else uri.split('/')[-1]
            var_name = f"?expanded_uri_{uri_id}"
            var_to_descendants[var_name] = descendants
        
        # Calculate total number of expanded URIs
        total_uris = sum(len(descendants) for descendants in var_to_descendants.values())
        
        # If total URIs is manageable, use the original single-query approach
        if total_uris <= self.MAX_VALUES_PER_BATCH:
            expanded_query = query_string
            values_clauses = []
            
            for uri in ontology_uris:
                descendants = uri_to_descendants.get(uri, [])
                if len(descendants) <= 1:
                    continue
                
                uri_id = uri.split('_')[-1] if '_' in uri else uri.split('/')[-1]
                var_name = f"?expanded_uri_{uri_id}"
                
                # Build the VALUES clause with all descendants
                uri_values = " ".join(f"<{d}>" for d in descendants)
                
                if bind_vars:
                    # When bind_expansion_to is specified, we want the bind variable
                    # (e.g., ?disease) to iterate over the expanded descendants independently.
                    #
                    # Strategy: Replace the original <URI> with the FIRST bind variable,
                    # and add a VALUES clause constraining that bind variable to the
                    # expanded descendants. This merges the URI triple and the bind
                    # variable triple into using the same user-defined variable,
                    # avoiding intersection queries (which would undercount results)
                    # and substring corruption (e.g., ?diseaseLabel -> ?expanded_uri_XLabel).
                    #
                    # Example: Given query:
                    #   ?dataset schema:healthCondition <MONDO_0005578> .
                    #   ?dataset schema:healthCondition ?disease .
                    # With bind_expansion_to=['disease'], this becomes:
                    #   VALUES ?disease { <MONDO_0005578> <MONDO_0008383> ... }
                    #   ?dataset schema:healthCondition ?disease .
                    #   ?dataset schema:healthCondition ?disease .  (redundant but harmless)
                    #
                    # Each descendant is then counted independently — no co-occurrence required.
                    bind_var = bind_vars[0]  # Use first bind variable for this URI
                    expanded_query = expanded_query.replace(f"<{uri}>", bind_var)
                    values_clause = f"VALUES {bind_var} {{ {uri_values} }}"
                    values_clauses.append(values_clause)
                else:
                    # Standard expansion: replace URI with a new expansion variable
                    expanded_query = expanded_query.replace(f"<{uri}>", var_name)
                    values_clause = f"VALUES {var_name} {{ {uri_values} }}"
                    values_clauses.append(values_clause)
            
            # Insert VALUES clauses after WHERE {
            if values_clauses:
                combined_values = "\n  ".join(values_clauses)
                where_match = re.search(r'WHERE\s*\{', expanded_query, re.IGNORECASE)
                if where_match:
                    insert_pos = where_match.end()
                    expanded_query = (
                        expanded_query[:insert_pos] + 
                        f"\n  {combined_values}\n" +
                        expanded_query[insert_pos:]
                    )
            
            return expanded_query, uri_to_descendants
        
        # Otherwise, create batched queries.
        #
        # Strategy: batch ALL expanded variables independently, then emit one query
        # per combination (Cartesian product of per-variable batches).
        #
        # Per-variable batch size: we give each variable an equal share of the budget.
        # With N expanded variables and a budget of MAX_VALUES_PER_BATCH total URIs per
        # query, each variable gets at most MAX_VALUES_PER_BATCH // N slots per batch.
        # This guarantees that the total VALUES-clause size of any single query never
        # exceeds MAX_VALUES_PER_BATCH (modulo rounding up to at least 1).

        num_expanded_vars = len(var_to_descendants)
        per_var_batch_size = max(1, self.MAX_VALUES_PER_BATCH // num_expanded_vars)

        # Build per-variable batch lists: {var_name: [[chunk0], [chunk1], ...]}
        var_batches: Dict[str, List[List[str]]] = {}
        for var_name, desc_list in var_to_descendants.items():
            chunks = [
                desc_list[i:i + per_var_batch_size]
                for i in range(0, len(desc_list), per_var_batch_size)
            ]
            var_batches[var_name] = chunks

        # Build the Cartesian product of per-variable batch indices.
        # For the common case of a single expanded variable this is just a flat loop.
        import itertools
        var_names = list(var_batches.keys())
        chunk_index_ranges = [range(len(var_batches[v])) for v in var_names]

        # Map expansion variable names back to bind/replacement names
        # so that query rewriting stays consistent with the non-batched path.
        var_to_replacement: Dict[str, str] = {}
        if bind_vars:
            # All expanded variables map to the first bind variable (same as non-batched path)
            for v in var_names:
                var_to_replacement[v] = bind_vars[0]
        else:
            for v in var_names:
                var_to_replacement[v] = v  # keep the ?expanded_uri_XXXX name

        batched_queries = []
        for combo in itertools.product(*chunk_index_ranges):
            # combo[i] is the chunk index for var_names[i]

            # Start from the original unmodified query string for each batch
            batch_query = query_string

            # Replace literal URIs in the query with the appropriate variable names
            for uri in ontology_uris:
                descendants = uri_to_descendants.get(uri, [])
                if len(descendants) <= 1:
                    continue
                uri_id = uri.split('_')[-1] if '_' in uri else uri.split('/')[-1]
                var_name = f"?expanded_uri_{uri_id}"
                replacement = var_to_replacement.get(var_name, var_name)
                batch_query = batch_query.replace(f"<{uri}>", replacement)

            # Build one VALUES clause per variable, using this combo's chunk
            values_clauses = []
            for i, v in enumerate(var_names):
                chunk = var_batches[v][combo[i]]
                replacement = var_to_replacement[v]
                uri_values = " ".join(f"<{d}>" for d in chunk)
                values_clauses.append(f"VALUES {replacement} {{ {uri_values} }}")

            # Deduplicate VALUES clauses that target the same replacement variable
            # (happens when bind_expansion_to maps multiple expanded vars to one name).
            seen_replacements = {}
            deduped_clauses = []
            for clause in values_clauses:
                # Extract the variable name from "VALUES ?foo { ... }"
                m = re.match(r'VALUES\s+(\?\w+)', clause)
                rep_var = m.group(1) if m else clause
                if rep_var not in seen_replacements:
                    seen_replacements[rep_var] = True
                    deduped_clauses.append(clause)
            values_clauses = deduped_clauses

            # Insert VALUES clauses right after WHERE {
            combined_values = "\n  ".join(values_clauses)
            where_match = re.search(r'WHERE\s*\{', batch_query, re.IGNORECASE)
            if where_match:
                insert_pos = where_match.end()
                batch_query = (
                    batch_query[:insert_pos] +
                    f"\n  {combined_values}\n" +
                    batch_query[insert_pos:]
                )

            batched_queries.append(batch_query)

        return batched_queries, uri_to_descendants
    
    def _merge_batch_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge results from multiple batched queries into a single result.
        
        Args:
            results: List of query results in compact format
            
        Returns:
            Single merged result in compact format
        """
        if not results:
            return {'columns': [], 'data': [], 'count': 0}
        
        if len(results) == 1:
            return results[0]
        
        # Get columns from first result
        merged = {
            'columns': results[0].get('columns', []),
            'data': [],
            'count': 0
        }
        
        # Collect all data rows, removing duplicates
        seen_rows = set()
        for result in results:
            if 'data' in result:
                for row in result['data']:
                    # Convert row to tuple for hashing
                    row_tuple = tuple(row)
                    if row_tuple not in seen_rows:
                        seen_rows.add(row_tuple)
                        merged['data'].append(row)
        
        merged['count'] = len(merged['data'])
        
        # Merge any warnings or analysis from the first result
        if 'query_analysis' in results[0]:
            merged['query_analysis'] = results[0]['query_analysis']
        if 'schema_warnings' in results[0]:
            merged['schema_warnings'] = results[0]['schema_warnings']
        
        return merged

    
    def _execute_raw(self, query_string: str, analyze: bool = True, auto_expand: bool = True) -> Dict[str, Any]:
        """Internal execute method that handles the actual SPARQL execution.
        
        Note: _fetch_descendants_for_uri now queries the endpoint directly, 
        so there is no risk of infinite recursion even with auto_expand=True.
        """
        return self.execute(query_string, analyze=analyze, auto_expand_descendants=auto_expand)
    
    def execute(self, query_string: str, analyze: bool = True, auto_expand_descendants: bool = True, max_descendants: int = 2000, max_depth: int = 5, bind_expansion_to: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute SPARQL query and return results in compact format.
        
        Args:
            query_string: The SPARQL query to execute
            analyze: If True, analyze query for common issues (LIMIT without ORDER BY)
            auto_expand_descendants: If True (default), automatically expand ontology URIs by
                pre-fetching descendants from ubergraph and injecting VALUES clauses.
                This enables queries like "arthritis" to automatically include all subtypes.
                Set to False when you want only the exact concepts mentioned in your query.
            max_descendants: Maximum descendants to fetch per ontology URI (default: 100).
                Increase for comprehensive coverage of large ontology branches.
            max_depth: Maximum hierarchy depth to traverse when expanding (default: 5 hops).
                Controls how deep to traverse the subClassOf hierarchy:
                - max_depth=1: Direct children only (e.g., osteoarthritis, rheumatoid arthritis)
                - max_depth=2: Children and grandchildren
                - max_depth=5: Up to 5 levels deep in the hierarchy
                Decrease for faster queries on very large/deep ontologies, increase for deeper coverage.
            bind_expansion_to: Optional list of variable names (with or without '?') that should be
                replaced with the expanded ontology variable. This is useful for GROUP BY queries
                where you want to count/aggregate per descendant concept.
                
                How it works: When you specify bind_expansion_to=['disease'], all occurrences of 
                ?disease in your query will be replaced with the expansion variable (e.g., 
                ?expanded_uri_0005578), which is constrained to only the parent + descendant concepts.
                
                Example WITHOUT bind_expansion_to:
                ```sparql
                SELECT ?disease (COUNT(?dataset) as ?count)
                WHERE {
                    ?dataset schema:healthCondition mondo:0005578 .  # Gets expanded
                    ?dataset schema:healthCondition ?disease .       # Matches ALL diseases
                }
                GROUP BY ?disease
                ```
                This returns ALL diseases on datasets that have arthritis, including unrelated ones
                like Cancer, Alzheimer's, etc.
                
                Example WITH bind_expansion_to=['disease']:
                ```sparql
                SELECT ?disease (COUNT(?dataset) as ?count)
                WHERE {
                    ?dataset schema:healthCondition mondo:0005578 .  # Gets expanded
                    ?dataset schema:healthCondition ?disease .       # Now ONLY matches expanded concepts
                }
                GROUP BY ?disease
                ```
                This returns ONLY arthritis-related diseases (parent + descendants) with their counts.

        
        Returns:
            Query results in compact format (columns + data arrays).
            If auto_expand_descendants=True and ontology URIs were expanded, includes 
            'ontology_expansion' field with expansion details.
            If analyze=True and issues detected, includes 'query_analysis' field with warnings.
        
        Examples:
            # Query for arthritis datasets - automatically includes all subtypes
            query('SELECT ?dataset WHERE { ?dataset schema:healthCondition <MONDO_0005578> }')
            
            # Query for direct children only
            query('SELECT ?dataset WHERE { ... }', max_depth=1)
            
            # Query without expansion - only exact matches
            query('SELECT ?dataset WHERE { ... }', auto_expand_descendants=False)
            
            # Count datasets per descendant (GROUP BY use case)
            query('''
                SELECT ?disease ?diseaseLabel (COUNT(DISTINCT ?dataset) as ?count)
                WHERE {
                    ?dataset schema:healthCondition mondo:0005578 .
                    ?dataset schema:healthCondition ?disease .
                    ?disease schema:name ?diseaseLabel .
                }
                GROUP BY ?disease ?diseaseLabel
            ''', max_depth=1, bind_expansion_to=['disease'])
        """
        # Analyze query before execution if requested
        analysis = None
        warnings = []
        expansion_info = None
        
        # Auto-expand ontology URIs to include descendants if requested
        original_query = query_string
        queries_to_execute = [query_string]  # Default: single query
        is_batched = False
        
        if auto_expand_descendants:
            ontology_uris = self._detect_ontology_uris(query_string)
            if ontology_uris:
                # Pre-fetch descendants from ubergraph with depth limiting,
                # then inject them as VALUES clauses into the user's query
                expanded_result, uri_to_descendants = self._expand_query_with_descendants(
                    query_string, ontology_uris, max_descendants, max_depth, bind_expansion_to
                )
                
                # Check if result is a single query or multiple batched queries
                if isinstance(expanded_result, list):
                    queries_to_execute = expanded_result
                    is_batched = True
                else:
                    queries_to_execute = [expanded_result]
                
                expansion_info = {
                    "expanded": True,
                    "original_uris": ontology_uris,
                    "expanded_uris": {
                        uri: len(descendants) for uri, descendants in uri_to_descendants.items()
                    },
                    "total_concepts": sum(len(descendants) for descendants in uri_to_descendants.values()),
                    "batched": is_batched,
                    "num_batches": len(queries_to_execute) if is_batched else 1,
                    "max_values_per_batch": self.MAX_VALUES_PER_BATCH
                }
        
        # Warn if schema hasn't been fetched
        if not self._schema_fetched and analyze:
            warnings.append({
                "type": "schema_not_fetched",
                "message": (
                    "⚠️  RECOMMENDATION: Call get_schema() before querying to understand "
                    "the knowledge graph structure, especially for edge properties."
                )
            })
        
        # Analyze first query (or single query if not batched)
        if analyze:
            analysis = self.analyzer.analyze_query(queries_to_execute[0])
        
        # Execute query/queries
        batch_results = []
        batch_errors = []
        for batch_idx, query_str in enumerate(queries_to_execute):
            # Get kg_name for FROM clause insertion for federated endpoint
            if self.kg_name != '':
                query_str = self._insert_from_clause(query_str, self.kg_name)
            
            self.sparql.setQuery(query_str)
            
            try:
                raw_result = self.sparql.query().convert()
            except Exception as e:
                if is_batched:
                    # For batched execution, record the error and continue with
                    # remaining batches so partial results are not lost.
                    batch_errors.append({
                        'batch': batch_idx,
                        'error': str(e),
                        'query': query_str
                    })
                    continue
                else:
                    # Single-query failure: return the error immediately (original behaviour).
                    error_msg = f"Query execution failed: {str(e)}"
                    # Add analysis warning to error message if applicable
                    if analysis and analysis.get('warning'):
                        error_msg += f"\n\n{analysis['warning']}"
                    return {
                        'error': error_msg,
                        'query': query_str
                    }
            
            # Convert to compact format (columns + data arrays)
            formatted_result = self._compact_result(raw_result)
            batch_results.append(formatted_result)
        
        # If every batch failed, surface the first error
        if is_batched and not batch_results:
            first_err = batch_errors[0]
            error_msg = f"Query execution failed: {first_err['error']}"
            if analysis and analysis.get('warning'):
                error_msg += f"\n\n{analysis['warning']}"
            return {
                'error': error_msg,
                'query': first_err['query']
            }
        
        # Merge results if batched
        if is_batched:
            formatted_result = self._merge_batch_results(batch_results)
            # Surface any per-batch errors as a non-fatal warning in the result
            if batch_errors:
                formatted_result['batch_errors'] = batch_errors
        else:
            formatted_result = batch_results[0]
        
        # Add analysis warnings to result if applicable
        if analyze and analysis and analysis.get('warning'):
            formatted_result['query_analysis'] = {
                'warning': analysis['warning'],
                'suggested_order': analysis['suggested_order'],
                'limit_value': analysis['limit_value']
            }
        
        # Add schema warnings if present
        if warnings:
            if 'query_analysis' in formatted_result:
                formatted_result['query_analysis']['schema_warnings'] = warnings
            else:
                formatted_result['schema_warnings'] = warnings
        
        # Add ontology expansion info if URIs were expanded
        if expansion_info:
            formatted_result['ontology_expansion'] = expansion_info
        
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
}}"""
# LIMIT 10"""
        
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

        # ubergraph has > 200K unique triples.
        if kg_name == "ubergraph":
            return []

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

    def lookup_uri(self, label: str, max_results: int = 2000) -> Dict[str, Any]:
        """Look up ontology term URIs by label in Ubergraph.

        Queries Ubergraph for exact label matches (rdfs:label) and exact
        synonyms (oboInOwl:hasExactSynonym). Case-insensitive.

        Args:
            label: The term to search for (e.g., "muscle organ", "rheumatoid arthritis")
            max_results: Maximum number of matching URIs to return (default: 2000)

        Returns:
            Dictionary with query_label, match_count, and matches list.
        """
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

        SELECT DISTINCT ?uri ?matchedLabel ?matchType
        FROM <https://purl.org/okn/frink/kg/ubergraph>
        WHERE {{
          {{
            ?uri rdfs:label ?matchedLabel .
            FILTER(LCASE(STR(?matchedLabel)) = LCASE("{label}"))
            BIND("exact_label" AS ?matchType)
          }}
          UNION
          {{
            ?uri oboInOwl:hasExactSynonym ?matchedLabel .
            FILTER(LCASE(STR(?matchedLabel)) = LCASE("{label}"))
            BIND("exact_synonym" AS ?matchType)
          }}
        }}
        LIMIT {max_results}
        """

        try:
            self.sparql.setQuery(query)
            raw_result = self.sparql.query().convert()

            matches = []
            if 'results' in raw_result:
                for binding in raw_result['results'].get('bindings', []):
                    matches.append({
                        'uri': binding.get('uri', {}).get('value', ''),
                        'label': binding.get('matchedLabel', {}).get('value', ''),
                        'match_type': binding.get('matchType', {}).get('value', '')
                    })

            return {
                'query_label': label,
                'match_count': len(matches),
                'matches': matches
            }
        except Exception as e:
            return {
                'query_label': label,
                'match_count': 0,
                'matches': [],
                'error': f"Lookup failed: {str(e)}"
            }

    def get_descendants_detailed(
        self,
        uri: str,
        max_results: int = 2000,
        max_depth: int = 5,
        include_distance: bool = True,
    ) -> Dict[str, Any]:
        """Expand a URI to find all its descendant classes in the ontology hierarchy.

        Uses depth-limited traversal via Ubergraph.

        Args:
            uri: The full URI to expand
            max_results: Maximum number of descendants to return (default: 2000)
            max_depth: Maximum number of subClassOf hops (default: 5)
            include_distance: If True, include hierarchy distance from root URI

        Returns:
            Dictionary with uri, label, max_depth, descendant_count, descendants.
        """
        if include_distance:
            depth_branches = []
            for depth in range(1, max_depth + 1):
                if depth == 1:
                    depth_branches.append(
                        f"{{ ?descendant rdfs:subClassOf <{uri}> . BIND({depth} AS ?distance) }}"
                    )
                else:
                    chain_parts = []
                    prev_var = "?descendant"
                    for i in range(1, depth):
                        next_var = f"?_m{i}"
                        chain_parts.append(f"{prev_var} rdfs:subClassOf {next_var} .")
                        prev_var = next_var
                    chain_parts.append(f"{prev_var} rdfs:subClassOf <{uri}> .")
                    chain_str = " ".join(chain_parts)
                    depth_branches.append(
                        f"{{ {chain_str} BIND({depth} AS ?distance) }}"
                    )

            union_block = "\n    UNION\n    ".join(depth_branches)

            query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?descendant ?label (MIN(?distance) AS ?min_distance)
            FROM <https://purl.org/okn/frink/kg/ubergraph>
            WHERE {{
              {{
                {union_block}
              }}
              FILTER(?descendant != <{uri}>)
              OPTIONAL {{ ?descendant rdfs:label ?label }}
            }}
            GROUP BY ?descendant ?label
            ORDER BY ?min_distance ?descendant
            LIMIT {max_results}
            """
        else:
            depth_branches = []
            for depth in range(1, max_depth + 1):
                if depth == 1:
                    depth_branches.append(
                        f"{{ ?descendant rdfs:subClassOf <{uri}> }}"
                    )
                else:
                    chain_parts = []
                    prev_var = "?descendant"
                    for i in range(1, depth):
                        next_var = f"?_m{i}"
                        chain_parts.append(f"{prev_var} rdfs:subClassOf {next_var} .")
                        prev_var = next_var
                    chain_parts.append(f"{prev_var} rdfs:subClassOf <{uri}> .")
                    chain_str = " ".join(chain_parts)
                    depth_branches.append(f"{{ {chain_str} }}")

            union_block = "\n    UNION\n    ".join(depth_branches)

            query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?descendant ?label
            FROM <https://purl.org/okn/frink/kg/ubergraph>
            WHERE {{
              {{
                {union_block}
              }}
              FILTER(?descendant != <{uri}>)
              OPTIONAL {{ ?descendant rdfs:label ?label }}
            }}
            ORDER BY ?descendant
            LIMIT {max_results}
            """

        # Query for the input URI's label
        label_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?label
        FROM <https://purl.org/okn/frink/kg/ubergraph>
        WHERE {{
          <{uri}> rdfs:label ?label .
        }}
        """

        # Get the label of the input URI
        try:
            self.sparql.setQuery(label_query)
            label_result = self.sparql.query().convert()
            uri_label = None
            if 'results' in label_result:
                bindings = label_result['results'].get('bindings', [])
                if bindings and 'label' in bindings[0]:
                    uri_label = bindings[0]['label'].get('value', None)
        except Exception:
            uri_label = None

        # Get descendants
        try:
            self.sparql.setQuery(query)
            raw_result = self.sparql.query().convert()

            descendants = []
            if 'results' in raw_result:
                for binding in raw_result['results'].get('bindings', []):
                    desc = {
                        'uri': binding.get('descendant', {}).get('value', ''),
                        'label': binding.get('label', {}).get('value', None)
                    }
                    if include_distance and 'min_distance' in binding:
                        desc['distance'] = int(binding['min_distance'].get('value', 0))
                    descendants.append(desc)

            return {
                'uri': uri,
                'label': uri_label,
                'max_depth': max_depth,
                'descendant_count': len(descendants),
                'descendants': descendants
            }
        except Exception as e:
            return {
                'uri': uri,
                'label': uri_label,
                'max_depth': max_depth,
                'descendant_count': 0,
                'descendants': [],
                'error': f"Failed to fetch descendants: {str(e)}"
            }


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
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default=None,
        help="Transport mode (default: stdio). Override with MCP_PROTO_OKN_TRANSPORT env var.",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Bind address for HTTP transport (default: 0.0.0.0). Override with MCP_PROTO_OKN_HOST env var.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Bind port for HTTP transport (default: 8000). Override with MCP_PROTO_OKN_PORT env var.",
    )
    return parser.parse_args()


def _wrap_with_api_key_auth(app):
    """Wrap a Starlette/ASGI app with Bearer-token authentication.

    Only active when the ``MCP_PROTO_OKN_API_KEY`` environment variable is set.
    CORS preflight (OPTIONS) requests are passed through without auth.
    """
    api_key = os.environ.get("MCP_PROTO_OKN_API_KEY")
    if not api_key:
        return app

    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse

    class APIKeyMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # Allow CORS preflight through
            if request.method == "OPTIONS":
                return await call_next(request)
            auth_header = request.headers.get("Authorization", "")
            if auth_header != f"Bearer {api_key}":
                return JSONResponse(
                    {"error": "Invalid or missing API key"},
                    status_code=401,
                )
            return await call_next(request)

    app.add_middleware(APIKeyMiddleware)
    return app


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

AUTOMATIC ONTOLOGY EXPANSION:
By default, this tool automatically detects ontology URIs (MONDO, DOID, HP, GO, UBERON, CL, CHEBI, etc.) 
in your query and expands them to include all descendant concepts. The expansion works by:
1. Pre-fetching descendants from the ubergraph (with depth-limited traversal, default max 5 hops)
2. Injecting the expanded URI list as a VALUES clause into your query

For example:
- A query for MONDO_0005578 (arthritic joint disease) will automatically include osteoarthritis, rheumatoid arthritis, etc.
- A query for GO_0008150 (biological process) will include all child processes
- A query for CL_0000000 (cell) will include all cell types

This means you don't need to manually fetch descendants - just query with the parent concept and
all subconcepts are automatically included. You can disable this with auto_expand_descendants=False.

The results will include an 'ontology_expansion' field showing which URIs were expanded and how many
descendants were found.

CONTROLLING EXPANSION DEPTH:
- max_descendants: Maximum number of descendants to fetch per ontology URI (default: 2000)
- max_depth: Maximum hierarchy depth to traverse (default: 5 hops)
  - max_depth=1: DIRECT CHILDREN ONLY (one level down). Use when the user asks for "direct descendants"
  - max_depth=2: Children and grandchildren
  - max_depth=5: Up to 5 levels deep (default, good balance)
  - Increase for deeper ontologies, decrease to 1-3 for faster queries on very large hierarchies

WHEN TO USE get_descendants() vs max_depth:
- Use max_depth parameter: When you want to query datasets/data with controlled hierarchy depth
- Use get_descendants() tool: When you want to EXPLORE the ontology structure itself (see what diseases 
  exist, understand the hierarchy, get distance information). This is useful for answering questions like
  "what are the types of arthritis?" or "show me the disease hierarchy"

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
    analyze: If True (default), analyzes query and warns if LIMIT is used without ORDER BY, and checks for edge property issues
    auto_expand_descendants: If True (default), automatically expands ontology URIs by pre-fetching descendants from ubergraph (depth-limited) and injecting as VALUES clauses. Set to False to query only the exact URIs mentioned.
    max_descendants: Maximum number of descendants to fetch per ontology URI (default: 100). Increase for comprehensive coverage.
    max_depth: Controls hierarchy depth (default: 5 hops). Set to 1 for direct children only, 2-3 for faster queries, 5+ for deep coverage.
    bind_expansion_to: Optional list of variable names (with or without '?') that should be replaced 
        with the expanded ontology variable. This is useful for GROUP BY queries where you want to 
        count/aggregate per descendant concept rather than per dataset.
        
        **HOW IT WORKS**: When you specify bind_expansion_to=['disease'], all occurrences of ?disease 
        in your query will be replaced with the expansion variable (e.g., ?expanded_uri_0005578), which 
        is constrained to only the parent + descendant concepts.
        
        **WITHOUT bind_expansion_to** - Returns datasets with arthritis (but ?disease matches ALL diseases):
        ```
        ?dataset schema:healthCondition mondo:0005578 .  # Gets expanded to include descendants
        ?dataset schema:healthCondition ?disease .       # ?disease binds to ALL diseases on those datasets!
        ```
        Result: Cancer (17 datasets), Alzheimer's (12 datasets), etc. - diseases unrelated to arthritis!
        
        **WITH bind_expansion_to=['disease']** - Returns only arthritis-related diseases:
        ```python
        query('''
            SELECT ?disease ?label (COUNT(?dataset) as ?count)
            WHERE {{
                ?dataset schema:healthCondition mondo:0005578 .
                ?dataset schema:healthCondition ?disease .
                ?disease schema:name ?label .
            }}
            GROUP BY ?disease ?label
        ''', max_depth=1, bind_expansion_to=['disease'])
        ```
        Result: Only rheumatoid arthritis (2006 datasets), osteoarthritis (424 datasets), etc.
        
        The ?disease variable now ONLY matches the parent concept and its descendants.

Returns:
    The query results in compact format (columns + data arrays). If analyze=True and issues are detected, includes a 'query_analysis' field with warnings and suggestions.
    If auto_expand_descendants=True and ontology URIs are expanded, includes an 'ontology_expansion' field with expansion details.
"""

    @mcp.tool(description=query_doc)
    def query(
        query_string: str, 
        analyze: bool = True,
        auto_expand_descendants: bool = True,
        max_descendants: int = 2000,
        max_depth: int = 5,
        bind_expansion_to: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        return sparql_server.execute(
            query_string, 
            analyze=analyze,
            auto_expand_descendants=auto_expand_descendants,
            max_descendants=max_descendants,
            max_depth=max_depth,
            bind_expansion_to=bind_expansion_to
        )

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

    @mcp.tool()
    def lookup_uri(
        label: str,
        max_results: int = 2000
    ) -> Dict[str, Any]:
        """
        Look up the URI for an ontology term by its label (name) in Ubergraph.

        USE THIS TOOL WHEN:
        - You have a human-readable term like "muscle organ", "arthritis", "heart"
          and need the corresponding ontology URI
        - You need to find the URI before calling get_descendants() or query()
        - The user refers to a concept by name rather than by URI

        DO NOT use web search to find ontology URIs — this tool queries Ubergraph directly.

        The search is case-insensitive and matches both exact labels (rdfs:label) and
        exact synonyms (oboInOwl:hasExactSynonym).

        Args:
            label: The term to search for (e.g., "muscle organ", "rheumatoid arthritis",
                   "heart", "glucose"). Case-insensitive.
            max_results: Maximum number of matching URIs to return (default: 2000)

        Returns:
            Dictionary containing:
            - query_label: The search term used
            - match_count: Number of matches found
            - matches: List of matches, each with uri, label, and match_type
                       (exact_label or exact_synonym)

        Examples:
            # Find the URI for "muscle organ"
            lookup_uri("muscle organ")
            # → UBERON:0001630 http://purl.obolibrary.org/obo/UBERON_0001630

            # Find URI for "rheumatoid arthritis"
            lookup_uri("rheumatoid arthritis")
            # → MONDO:0005578 http://purl.obolibrary.org/obo/MONDO_0008383

            # Then use the URI with get_descendants
            get_descendants("http://purl.obolibrary.org/obo/UBERON_0001630")
        """
        return sparql_server.lookup_uri(label, max_results)

    @mcp.tool()
    def get_descendants(
        uri: str,
        max_results: int = 2000,
        max_depth: int = 5,
        include_distance: bool = True
    ) -> Dict[str, Any]:
        """
        Expand a URI to find all its descendant classes in the ontology hierarchy.

        USE THIS TOOL WHEN:
        - You want to EXPLORE the ontology structure itself (not query datasets)
        - You need to see what diseases/concepts exist under a parent term
        - You want to understand the hierarchy and see distance information
        - The user asks questions like "what types of arthritis are there?" or "show me the disease hierarchy"

        DON'T USE THIS TOOL WHEN:
        - You want to query datasets with ontology expansion - use the query() tool with max_depth parameter instead
        - The user wants data/datasets - use query() which has built-in expansion

        Descendants are classes that are subclasses (direct or transitive) of the given URI.
        This uses the rdfs:subClassOf relationship to traverse the ontology hierarchy.

        Uses depth-limited traversal (up to 5 hops) to avoid timeouts on large ontologies.

        Args:
            uri: The full URI to expand (e.g., 'http://purl.obolibrary.org/obo/MONDO_0005178')
            max_results: Maximum number of descendants to return (default: 2000)
            max_depth: Maximum number of subClassOf hops to traverse (default: 5)
            include_distance: If True (default), include the hierarchy distance from the root URI.
                Distance=1 means direct children, distance=2 means grandchildren, etc.

        Returns:
            Dictionary containing:
            - uri: The input URI
            - label: The label of the input URI (if available)
            - max_depth: Maximum depth traversed (always 5)
            - descendant_count: Total number of descendants found
            - descendants: List of descendant objects with uri, label, and optionally distance

        Examples:
            # Explore arthritis hierarchy with distance info
            get_descendants('http://purl.obolibrary.org/obo/MONDO_0005578', include_distance=True)

            # Get comprehensive list without distance
            get_descendants('http://purl.obolibrary.org/obo/MONDO_0005578', max_results=2000, include_distance=False)
        """
        return sparql_server.get_descendants_detailed(uri, max_results, max_depth, include_distance)

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
13. Save to ~/Downloads/<kg_name>-schema.mermaid and call present_files

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

    # Resolve transport settings: CLI args > env vars > defaults
    transport = (args.transport if args.transport is not None
                 else os.environ.get("MCP_PROTO_OKN_TRANSPORT", "stdio")).lower()
    host = (args.host if args.host is not None
            else os.environ.get("MCP_PROTO_OKN_HOST", "0.0.0.0"))
    port = (args.port if args.port is not None
            else int(os.environ.get("MCP_PROTO_OKN_PORT", "8000")))

    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "streamable-http":
        mcp.settings.host = host
        mcp.settings.port = port
        app = mcp.streamable_http_app()
        app = _wrap_with_api_key_auth(app)
        import uvicorn
        print(f"mcp-proto-okn ({sparql_server.kg_name}) listening on http://{host}:{port}", file=sys.stderr)
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        print(f"Unknown transport: {transport!r}. Use 'stdio' or 'streamable-http'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()