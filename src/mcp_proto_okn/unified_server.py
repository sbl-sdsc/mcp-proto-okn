"""
Unified MCP Server for Proto-OKN Knowledge Graphs.

Exposes all Proto-OKN knowledge graphs through a single MCP server instance.
Provides graph discovery, natural-language routing, per-graph querying,
and cross-graph result aggregation with identifier mapping.

Transport modes:
  - stdio (default): For local subprocess use via ``uvx mcp-proto-okn-unified``.
  - streamable-http: For remote deployment over HTTP/HTTPS.

Environment variables (HTTP transport):
  MCP_PROTO_OKN_TRANSPORT  - "stdio" (default) or "streamable-http"
  MCP_PROTO_OKN_HOST       - Bind address (default "0.0.0.0")
  MCP_PROTO_OKN_PORT       - Bind port (default 8000)
  MCP_PROTO_OKN_API_KEY    - Optional Bearer-token authentication
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from mcp_proto_okn import __version__

from mcp_proto_okn.identifier_mapping import (
    find_common_identifiers,
    suggest_join_strategy,
    build_gene_lookup_query,
    build_gene_bridge_query,
)
from mcp_proto_okn.registry import GraphRegistry
from mcp_proto_okn.server import SPARQLServer


class UnifiedSPARQLServer:
    """Manages multiple SPARQLServer instances across all Proto-OKN graphs."""

    def __init__(self, registry_path: Optional[str] = None):
        self.registry = GraphRegistry(registry_path)
        self._servers: Dict[str, SPARQLServer] = {}

    def _get_server(self, graph_name: str) -> SPARQLServer:
        """Lazy-create and cache a SPARQLServer for the given graph."""
        canonical = self._validate_graph_name(graph_name)
        if canonical not in self._servers:
            graph_info = self.registry.get(canonical)
            self._servers[canonical] = SPARQLServer(
                endpoint_url=graph_info.endpoint_url
            )
        return self._servers[canonical]

    def _validate_graph_name(self, name: str) -> str:
        """Validate and resolve a graph name. Raises ValueError if not found."""
        canonical = self.registry.resolve_name(name)
        if canonical is None:
            available = ", ".join(self.registry.graph_names)
            raise ValueError(
                f"Unknown graph: '{name}'. Available graphs: {available}"
            )
        return canonical


def parse_args():
    parser = argparse.ArgumentParser(description="Unified MCP SPARQL Server for Proto-OKN")
    parser.add_argument(
        "--registry",
        required=False,
        help="Path to registry.json (default: auto-discover)",
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
    """Wrap a Starlette/ASGI app with Bearer-token authentication."""
    api_key = os.environ.get("MCP_PROTO_OKN_API_KEY")
    if not api_key:
        return app

    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse

    class APIKeyMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
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

    # Initialize unified server
    unified = UnifiedSPARQLServer(registry_path=args.registry)

    # Determine transport early so we can configure security settings
    transport = (args.transport if args.transport is not None
                 else os.environ.get("MCP_PROTO_OKN_TRANSPORT", "stdio")).lower()

    # Disable DNS rebinding protection for HTTP transport (runs behind
    # Kubernetes service/ingress where Host header won't be localhost).
    transport_security = None
    if transport == "streamable-http":
        transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        )

    # Create MCP server
    mcp = FastMCP(
        "Proto-OKN Unified Knowledge Graph Server",
        transport_security=transport_security,
        instructions="""You have access to 27 Proto-OKN knowledge graphs through a single unified server.

WORKFLOW FOR CROSS-GRAPH ANALYSIS:
1. Use list_graphs() or route_query() to discover relevant graphs
2. Use get_schema(graph) to understand each graph's structure before writing SPARQL
3. Use query(graph, sparql) to query individual graphs with graph-specific SPARQL
4. Use get_join_strategy(graph_a, graph_b) to understand how to merge results
5. Use multi_graph_query({graph1: sparql1, graph2: sparql2}) to run queries across graphs

IMPORTANT: Each graph has its own schema. Always call get_schema() before writing SPARQL for a graph.
IMPORTANT: For gene queries across graphs, different graphs use different gene identifiers
(Ensembl, NCBI Gene ID, gene symbol). Use get_join_strategy() to understand conversions.""",
    )

    # ── Tool 1: list_graphs ──────────────────────────────────────────────

    @mcp.tool()
    def list_graphs(
        domain: Optional[str] = None,
        entity_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List all available Proto-OKN knowledge graphs with their metadata.

        Call this first to understand what data is available. Returns graph names,
        descriptions, domain tags, entity types, and identifier namespaces.

        Args:
            domain: Optional filter by domain tag (e.g., "biology", "health",
                    "toxicology", "environment", "geospatial")
            entity_type: Optional filter by entity class name (e.g., "Gene",
                        "Disease", "ChemicalEntity")

        Returns:
            Dictionary with graph_count and graphs list.
        """
        if domain:
            graphs = unified.registry.filter_by_domain(domain)
        elif entity_type:
            graphs = unified.registry.filter_by_entity_type(entity_type)
        else:
            graphs = unified.registry.list_all()

        return {
            "graph_count": len(graphs),
            "graphs": graphs,
        }

    # ── Tool 2: route_query ──────────────────────────────────────────────

    @mcp.tool()
    def route_query(question: str) -> Dict[str, Any]:
        """
        Route a natural language question to the most relevant knowledge graphs.

        Takes a natural language question and performs keyword matching against
        all graph metadata (descriptions, domain tags, entity types, example queries).
        Returns ALL graphs sorted by relevance score.

        Args:
            question: Natural language question (e.g., "What drugs treat diabetes?",
                     "Where are PFAS contamination sites?")

        Returns:
            Dictionary with question, candidate_count, and candidates list
            sorted by relevance_score (highest first).
        """
        results = unified.registry.search(question)
        return {
            "question": question,
            "candidate_count": len(results),
            "candidates": results,
        }

    # ── Tool 3: get_schema ───────────────────────────────────────────────

    @mcp.tool()
    def get_schema(
        graph_name: str,
        compact: bool = True,
    ) -> Dict[str, Any]:
        """
        Get the schema (classes, predicates, edge properties) for a knowledge graph.

        MUST be called before writing SPARQL queries for a graph to understand its
        specific entity types, predicates, and property names.

        Args:
            graph_name: Name of the graph (e.g., "spoke-okn", "biobricks-tox21")
            compact: If True, return compact format (default)

        Returns:
            Schema dictionary with classes, predicates, edge_properties, node_properties.
        """
        try:
            server = unified._get_server(graph_name)
            schema = server.query_schema(compact=compact)
            return {"graph_name": graph_name, "schema": schema}
        except ValueError as e:
            return {"error": str(e)}

    # ── Tool 4: get_description ──────────────────────────────────────────

    @mcp.tool()
    def get_description(graph_name: str) -> Dict[str, Any]:
        """
        Get the full description and metadata for a knowledge graph.

        Returns the graph's registry content plus additional metadata including
        domain tags, identifier namespaces, and example queries.

        Args:
            graph_name: Name of the graph (e.g., "spoke-okn")

        Returns:
            Dictionary with description, domain_tags, identifier_namespaces, etc.
        """
        try:
            canonical = unified._validate_graph_name(graph_name)
            graph_info = unified.registry.get(canonical)
            server = unified._get_server(canonical)
            description = server.build_description()
            return {
                "graph_name": canonical,
                "description": description,
                "domain_tags": graph_info.domain_tags,
                "identifier_namespaces": graph_info.identifier_namespaces,
                "example_queries": graph_info.example_queries,
                "entity_types": graph_info.entity_types,
            }
        except ValueError as e:
            return {"error": str(e)}

    # ── Tool 5: query ────────────────────────────────────────────────────

    @mcp.tool()
    def query(
        graph_name: str,
        query_string: str,
        analyze: bool = True,
        auto_expand_descendants: bool = True,
        max_descendants: int = 2000,
        max_depth: int = 5,
        bind_expansion_to: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a SPARQL query against a specific knowledge graph.

        Supports automatic ontology expansion (MONDO, UBERON, etc.), query analysis
        with warnings, and FROM clause injection. The FROM clause is automatically
        added to scope the query to the correct named graph.

        IMPORTANT: Call get_schema() first to understand the graph's entity types
        and predicates before writing your SPARQL query.

        Args:
            graph_name: Name of the graph to query (e.g., "spoke-okn")
            query_string: SPARQL query string
            analyze: If True, analyze query for potential issues (default: True)
            auto_expand_descendants: If True, automatically expand ontology URIs
                to include descendants (default: True)
            max_descendants: Maximum descendants per URI expansion (default: 2000)
            max_depth: Maximum depth for ontology expansion (default: 5)
            bind_expansion_to: Optional list of variable names to bind expanded URIs to

        Returns:
            Dictionary with columns, data, count, and optional analysis/expansion info.
        """
        try:
            server = unified._get_server(graph_name)
            result = server.execute(
                query_string,
                analyze=analyze,
                auto_expand_descendants=auto_expand_descendants,
                max_descendants=max_descendants,
                max_depth=max_depth,
                bind_expansion_to=bind_expansion_to,
            )
            return {"graph_name": graph_name, **result}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Query failed on {graph_name}: {str(e)}"}

    # ── Tool 6: multi_graph_query ────────────────────────────────────────

    @mcp.tool()
    def multi_graph_query(
        queries: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Execute different SPARQL queries against multiple knowledge graphs in one call.

        Each graph gets its own tailored SPARQL query designed for that graph's
        specific schema. Results are returned with a source_graph column prepended.

        WORKFLOW:
        1. Call get_schema() for each graph first to understand its schema
        2. Write graph-specific SPARQL for each graph
        3. Submit all queries here in one call
        4. Use get_join_strategy() to understand how to merge results on shared identifiers

        Args:
            queries: Dictionary mapping graph names to SPARQL query strings.
                     Example: {"spoke-okn": "SELECT ...", "biobricks-ice": "SELECT ..."}

        Returns:
            Dictionary with combined results, per-graph counts, and any errors.
        """
        all_rows = []
        all_columns = None
        per_graph = {}
        errors = {}

        for graph_name, query_string in queries.items():
            try:
                server = unified._get_server(graph_name)
                result = server.execute(query_string)

                columns = result.get("columns", [])
                data = result.get("data", [])
                count = result.get("count", 0)

                # Prepend source_graph column
                if all_columns is None:
                    all_columns = ["source_graph"] + columns

                for row in data:
                    all_rows.append([graph_name] + row)

                per_graph[graph_name] = {"count": count, "status": "success"}

            except ValueError as e:
                errors[graph_name] = str(e)
                per_graph[graph_name] = {"count": 0, "status": "error", "error": str(e)}
            except Exception as e:
                errors[graph_name] = f"Query failed: {str(e)}"
                per_graph[graph_name] = {"count": 0, "status": "error", "error": str(e)}

        return {
            "columns": all_columns or ["source_graph"],
            "data": all_rows,
            "count": len(all_rows),
            "per_graph": per_graph,
            "errors": errors if errors else None,
        }

    # ── Tool 7: get_join_strategy ────────────────────────────────────────

    @mcp.tool()
    def get_join_strategy(graph_a: str, graph_b: str) -> Dict[str, Any]:
        """
        Get the recommended strategy for joining results from two knowledge graphs.

        Returns shared identifier namespaces and a description of how to merge
        results. Especially important for gene identifiers, which vary across graphs
        (Ensembl in spoke-okn, NCBI Gene in spoke-genelab, both in gene-expression-atlas-okn).

        Args:
            graph_a: First graph name
            graph_b: Second graph name

        Returns:
            Dictionary with can_join, common_identifiers, strategy description,
            and optionally bridge graph info for gene identifier conversion.
        """
        try:
            canonical_a = unified._validate_graph_name(graph_a)
            canonical_b = unified._validate_graph_name(graph_b)
            strategy = suggest_join_strategy(canonical_a, canonical_b)
            strategy["graph_a"] = canonical_a
            strategy["graph_b"] = canonical_b
            return strategy
        except ValueError as e:
            return {"error": str(e)}

    # ── Tool 8: lookup_uri ───────────────────────────────────────────────

    @mcp.tool()
    def lookup_uri(
        label: str,
        max_results: int = 2000,
    ) -> Dict[str, Any]:
        """
        Look up the URI for an ontology term by its label (name) in Ubergraph.

        Graph-independent ontology lookup. Use when you have a human-readable term
        like "muscle organ" or "rheumatoid arthritis" and need the corresponding
        ontology URI for use in SPARQL queries.

        Args:
            label: The term to search for (case-insensitive)
            max_results: Maximum number of matching URIs to return (default: 2000)

        Returns:
            Dictionary with query_label, match_count, and matches list.
        """
        # Use any cached server, or create one for spoke-okn (arbitrary choice;
        # lookup_uri queries ubergraph, not the KG endpoint)
        if unified._servers:
            server = next(iter(unified._servers.values()))
        else:
            server = unified._get_server("spoke-okn")
        return server.lookup_uri(label, max_results)

    # ── Tool 9: get_descendants ──────────────────────────────────────────

    @mcp.tool()
    def get_descendants(
        uri: str,
        max_results: int = 2000,
        max_depth: int = 5,
        include_distance: bool = True,
    ) -> Dict[str, Any]:
        """
        Expand a URI to find all its descendant classes in the ontology hierarchy.

        Graph-independent ontology hierarchy expansion via Ubergraph.
        Use to explore ontology structure (e.g., "what types of arthritis exist?").

        For querying datasets with ontology expansion, use the query() tool with
        auto_expand_descendants=True instead.

        Args:
            uri: The full URI to expand (e.g., 'http://purl.obolibrary.org/obo/MONDO_0005178')
            max_results: Maximum number of descendants to return (default: 2000)
            max_depth: Maximum subClassOf hops to traverse (default: 5)
            include_distance: If True, include hierarchy distance from root URI

        Returns:
            Dictionary with uri, label, max_depth, descendant_count, descendants.
        """
        if unified._servers:
            server = next(iter(unified._servers.values()))
        else:
            server = unified._get_server("spoke-okn")
        return server.get_descendants_detailed(uri, max_results, max_depth, include_distance)

    # ── Tool 10: get_query_template ────────────────────────────────────

    @mcp.tool()
    def get_query_template(
        graph_name: str,
        relationship_name: str,
    ) -> Dict[str, Any]:
        """
        Get a query template for a specific relationship, especially useful for edges with properties.

        This tool retrieves the appropriate query template based on the schema,
        showing the RDF reification pattern for querying relationships that have
        edge properties (like MEASURED_DIFFERENTIAL_EXPRESSION,
        MEASURED_DIFFERENTIAL_METHYLATION, etc.).

        Args:
            graph_name: Name of the graph (e.g., "spoke-genelab")
            relationship_name: Name of the relationship (e.g., 'MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG')

        Returns:
            A ready-to-use SPARQL query template showing the RDF reification pattern
            for this relationship.
        """
        try:
            server = unified._get_server(graph_name)
            template = server.get_relationship_template(relationship_name)
            return {"graph_name": graph_name, "relationship_name": relationship_name, "template": template}
        except ValueError as e:
            return {"error": str(e)}

    # ── Tool 11: clean_mermaid_diagram ───────────────────────────────

    @mcp.tool()
    def clean_mermaid_diagram(mermaid_content: str) -> str:
        """
        Clean a Mermaid class diagram by removing unwanted elements.

        This tool removes:
        - All note statements that would render as unreadable yellow boxes
        - Empty curly braces from class definitions (handles both single-line and multi-line)
        - Strings after newline characters (e.g., truncates "ClassName\\nextra" to "ClassName")
        - Vertical bars | (invalid in class diagrams)

        Args:
            mermaid_content: The raw Mermaid class diagram content

        Returns:
            Cleaned Mermaid content with note statements, empty braces, and
            post-newline strings removed.
        """
        import re

        # First, truncate any strings after \n characters in the entire content
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
            if re.match(r'^\s*class\s+\w+\s*\{\s*\}\s*$', line):
                line = re.sub(r'^(\s*class\s+\w+)\s*\{\s*\}\s*$', r'\1', line)
                cleaned_lines.append(line)
                i += 1
                continue

            # Check for empty class definitions (multi-line format)
            if re.match(r'^\s*class\s+\w+\s*\{\s*$', line):
                j = i + 1
                found_closing = False
                has_content = False

                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line:
                        j += 1
                        continue
                    if next_line == '}':
                        found_closing = True
                        break
                    else:
                        has_content = True
                        break

                if found_closing and not has_content:
                    class_match = re.match(r'^(\s*class\s+\w+)\s*\{\s*$', line)
                    if class_match:
                        cleaned_lines.append(class_match.group(1))
                    i = j + 1
                    continue

            cleaned_lines.append(line)
            i += 1

        return '\n'.join(cleaned_lines)

    # ── Tool 12: create_chat_transcript ──────────────────────────────

    @mcp.tool()
    def create_chat_transcript(graph_name: Optional[str] = None) -> str:
        """
        Generate a prompt template for creating a markdown chat transcript.

        Returns formatting guidelines and a template for documenting knowledge
        graph analysis sessions as reproducible markdown transcripts.

        Args:
            graph_name: Optional graph name for the filename. If not provided,
                        uses "proto-okn" as a default prefix.

        Returns:
            A string containing the transcript template with formatting instructions.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        prefix = graph_name or "proto-okn"

        return f"""Create a chat transcript in .md format following the outline below.
1. Include prompts, text responses, and visualizations preferably inline, and when not possible as a link to a document.
2. Include mermaid diagrams inline. Do not link to the mermaid file.
3. Do not include the prompt to create this transcript.
4. Save the transcript to ~/Downloads/<descriptive-filename>.md

## Chat Transcript
<Title>

\U0001f464 **User**
<prompt>

---

\U0001f9e0 **Assistant**
<entire text response goes here>


*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) {__version__} on {today}*

IMPORTANT:
- After the footer above, add a line with the model string you are using).
- Save the complete transcript to ~/Downloads/ with a descriptive filename (e.g., ~/Downloads/{prefix}-chat-transcript-{today}.md)
- Use the present_files tool to share the transcript file with the user.
"""

    # ── Tool 13: visualize_schema ────────────────────────────────────

    @mcp.tool()
    def visualize_schema(graph_name: str) -> str:
        """
        Generate a comprehensive prompt for creating a Mermaid class diagram
        of a knowledge graph schema.

        Returns step-by-step instructions for generating, cleaning, and saving
        a publication-quality schema diagram. Includes handling of edges with
        properties as intermediary classes.

        Args:
            graph_name: Name of the graph to visualize (e.g., "spoke-genelab")

        Returns:
            A string containing the step-by-step visualization workflow.
        """
        try:
            canonical = unified._validate_graph_name(graph_name)
        except ValueError as e:
            return str(e)

        return f"""Visualize the knowledge graph schema for '{canonical}' using a Mermaid class diagram.

CRITICAL WORKFLOW - Follow these steps EXACTLY IN ORDER:

STEP 1-5: Generate Draft Diagram
1. First call get_schema('{canonical}') if it has not been called to retrieve the classes and predicates
2. Analyze the schema to identify:
   - Node classes (entities like Gene, Study, Assay, etc.)
   - Edge predicates (relationships between nodes)
   - Edge properties (predicates that describe data types like float, int, string, boolean, date, etc.)
3. Generate the raw Mermaid class diagram showing:
   - All node classes with their properties
   - For edges WITHOUT properties: show as labeled arrows between classes (e.g., `Mission --> Study : CONDUCTED_MIcS`)
   - For edges WITH properties: represent the edge as an intermediary class containing the properties, with unlabeled arrows connecting source -> edge class -> target
4. Make the diagram taller / less wide:
   - Set the diagram direction to TB (top->bottom): `direction TB`
5. Do not append newline characters

STEP 6-9: MANDATORY CLEANING - CANNOT BE SKIPPED
6. STOP HERE! You now have a draft diagram. DO NOT use it yet.
7. Call clean_mermaid_diagram and pass your draft diagram as the parameter
8. Wait for the tool to return the cleaned diagram
9. Your draft is now OBSOLETE. Delete it from your mind. You will use ONLY the cleaned output.

STEP 10-13: Present ONLY the Cleaned Diagram
10. Copy the EXACT text returned by clean_mermaid_diagram (not your draft)
11. Present this CLEANED diagram inline in a mermaid code block
12. Create a .mermaid file with ONLY the CLEANED diagram code (no markdown fences)
13. Save to ~/Downloads/{canonical}-schema.mermaid and call present_files

STOP AND CHECK - Before you respond to the user:
- Did I call clean_mermaid_diagram? If NO -> Go back and call it now
- Am I using the cleaned output? If NO -> Replace with cleaned output
- Does my diagram contain empty {{}} braces? If YES -> You're using your draft, use cleaned output
- Did I call present_files? If NO -> Call it now

EDGES WITH PROPERTIES - CRITICAL GUIDELINES:
- When an edge predicate has associated properties (e.g., log2fc, adj_p_value), DO NOT use a separate namespace
- Instead, represent the edge as an intermediary class with the original predicate name
- Connect the source class to the edge class, then the edge class to the target class
- Example: Instead of `Assay --> Gene : MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG` with a separate EdgeProperties namespace,
  create:
    class MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG {{
        float log2fc
        float adj_p_value
    }}
    Assay --> MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG
    MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG --> Gene
- This approach clearly shows that the properties belong to the relationship itself

RENDERING REQUIREMENTS:
- The .mermaid file MUST contain ONLY the Mermaid diagram code
- DO NOT include markdown code fences (```mermaid) in the .mermaid file
- DO NOT include any explanatory text in the .mermaid file
- The file should start with "classDiagram" and contain only the diagram definition
- ALWAYS use present_files to share the .mermaid file after creating it
"""

    # ── Transport ────────────────────────────────────────────────────────

    # `transport` was already resolved at the top of main()
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
        print(f"mcp-proto-okn-unified listening on http://{host}:{port}", file=sys.stderr)
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        print(f"Unknown transport: {transport!r}. Use 'stdio' or 'streamable-http'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
