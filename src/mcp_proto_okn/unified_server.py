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
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

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

    # Create MCP server
    mcp = FastMCP(
        "Proto-OKN Unified Knowledge Graph Server",
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

    # ── Transport ────────────────────────────────────────────────────────

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
        print(f"mcp-proto-okn-unified listening on http://{host}:{port}", file=sys.stderr)
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        print(f"Unknown transport: {transport!r}. Use 'stdio' or 'streamable-http'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
