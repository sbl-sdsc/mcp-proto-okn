# Unified MCP Server for Proto-OKN Knowledge Graphs

A single [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes **27 Proto-OKN knowledge graphs** through one unified interface. The server enables AI assistants to discover graphs, understand their schemas, query them with SPARQL, bridge identifiers across graphs, and combine results from multiple sources -- all through natural language conversation.

## The Problem

The [Proto-OKN](https://www.proto-okn.net/) program has produced 27 knowledge graphs spanning biology, health, toxicology, environment, justice, and manufacturing. These graphs are hosted on the [FRINK](https://frink.renci.org/) federated SPARQL platform and contain rich, interconnected data. But each graph has its own schema, its own identifier systems, and its own query patterns.

Previously, each graph required its own MCP server instance -- 27 separate processes, 27 separate `@mentions` in Claude Desktop, and no programmatic way to discover or navigate across them. Cross-graph analysis required the user to manually coordinate between servers, know which identifiers each graph uses, and figure out how to bridge results.

## The Solution

The unified server replaces all 27 separate processes with a **single server** that provides:

- **Graph Discovery** -- list, filter, and search all 27 graphs by domain, entity type, or natural language
- **Schema Inspection** -- understand each graph's classes, predicates, and properties before writing queries
- **Per-Graph Querying** -- execute SPARQL with automatic ontology expansion and FROM clause injection
- **Cross-Graph Bridging** -- understand shared identifiers and join strategies between any two graphs
- **Multi-Graph Queries** -- run different SPARQL queries across multiple graphs in a single call
- **Ontology Services** -- look up URIs and explore ontology hierarchies via Ubergraph
- **Visualization & Documentation** -- generate schema diagrams, query templates, and chat transcripts

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI Assistant (Claude)                           │
│                                                                       │
│  "What genes are affected by spaceflight and what diseases             │
│   are they associated with?"                                          │
└───────────────────────────────┬───────────────────────────────────────┘
                                │  MCP Protocol (stdio or HTTP)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Unified MCP Server                                  │
│                    (mcp-proto-okn-unified)                             │
│                                                                       │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────────────┐│
│  │  13 MCP Tools  │  │Graph Registry│  │ Identifier Mapping           ││
│  │               │  │              │  │                              ││
│  │ list_graphs   │  │ 27 graphs    │  │ Gene: Ensembl ↔ NCBI ↔      ││
│  │ route_query   │  │ domain tags  │  │       Symbol (via bridge)    ││
│  │ get_schema    │  │ entity types │  │ Chemical: CAS, InChIKey,     ││
│  │ get_descript. │  │ identifiers  │  │          DTXSID              ││
│  │ query         │  │ examples     │  │ Disease: MONDO               ││
│  │ multi_graph   │  │ aliases      │  │ Location: FIPS, S2Cell       ││
│  │ join_strategy │  │              │  │ Industry: NAICS              ││
│  │ lookup_uri    │  │              │  │                              ││
│  │ get_descend.  │  │              │  │                              ││
│  │ query_template│  │              │  │                              ││
│  │ clean_mermaid │  │              │  │                              ││
│  │ chat_transcr. │  │              │  │                              ││
│  │ viz_schema    │  │              │  │                              ││
│  └──────┬────────┘  └──────────────┘  └──────────────────────────────┘│
│         │                                                             │
│  ┌──────▼──────────────────────────────────────────────────────────┐  │
│  │              SPARQLServer instances (lazy-cached)                │  │
│  │                                                                  │  │
│  │  spoke-okn ──┐                                                  │  │
│  │  spoke-genelab ──┐    Each server handles:                      │  │
│  │  biobricks-ice ──┤    • FROM clause injection (named graph)     │  │
│  │  biobricks-tox21 ┤    • Ontology expansion (MONDO, UBERON, ..)  │  │
│  │  gene-expr-atlas ┤    • Query analysis and warnings             │  │
│  │  ... (27 total) ─┘    • Result formatting                      │  │
│  └──────┬──────────────────────────────────────────────────────────┘  │
└─────────┼────────────────────────────────────────────────────────────┘
          │  SPARQL over HTTPS
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRINK Federation Platform                           │
│                    frink.apps.renci.org                                │
│                                                                       │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │spoke-okn│ │spoke-    │ │biobricks-│ │biobricks-│ │gene-expr-│    │
│  │         │ │genelab   │ │ice       │ │tox21     │ │atlas-okn │    │
│  └─────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │sawgraph │ │dreamkg   │ │scales    │ │ruralkg   │ │securechn │    │
│  └─────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│                     ... 27 named graphs total ...                     │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  Ubergraph (ontology services: MONDO, UBERON, HP, GO, etc.)   │   │
│  └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Graph Registry (`registry.py` + `registry.json`)

A structured catalog of all 27 knowledge graphs. Each entry contains:

| Field | Description |
|---|---|
| `name` | Canonical graph name (e.g., `spoke-okn`) |
| `display_name` | Human-readable name |
| `endpoint_url` | SPARQL endpoint URL |
| `domain_tags` | Categorization (biology, health, toxicology, environment, etc.) |
| `description_summary` | What the graph contains, how large it is, who it's for |
| `entity_types` | Classes, predicates, edge properties in the graph |
| `identifier_namespaces` | What ID systems the graph uses (Ensembl, CAS, MONDO, etc.) |
| `example_queries` | Natural language questions this graph can answer |
| `aliases` | Alternate names that resolve to this graph |

The registry enables **discovery without querying**. An AI assistant can search by keyword, filter by domain or entity type, and understand what each graph contains before ever sending a SPARQL query.

### Identifier Mapping (`identifier_mapping.py`)

A static bridge table that maps identifier types to graphs and their URI patterns. This solves the critical cross-graph problem: different graphs use different identifiers for the same real-world entities.

**Identifier bridge categories:**

| Category | Identifier Types | Graphs |
|---|---|---|
| **Genes** | Ensembl, NCBI Gene, Gene Symbol | spoke-okn, spoke-genelab, gene-expression-atlas-okn, biobricks-ice |
| **Chemicals** | CAS, DTXSID, InChIKey | biobricks-tox21, biobricks-ice, biobricks-toxcast, sawgraph, spoke-okn |
| **Diseases** | MONDO | spoke-okn, biohealth |
| **Locations** | FIPS, S2Cell | spoke-okn, nikg, ruralkg, spatialkg, hydrologykg, ufokn, fiokg |
| **Biomedical** | MeSH, ChEBI, UBERON | biobricks-mesh, biohealth, spoke-okn, spoke-genelab |
| **Industry** | NAICS | fiokg, sudokn |

**Gene identifier bridging** is particularly important. The `gene-expression-atlas-okn` graph stores both NCBI Gene IDs and Ensembl IDs for the same genes, making it a natural bridge between graphs that use different gene identifier systems:

```
spoke-genelab          gene-expression-atlas-okn          spoke-okn
(NCBI Gene ID)  ──────  (NCBI Gene + Ensembl)  ──────  (Ensembl ID)
(Gene Symbol)           (Gene Symbol)
```

### Unified Server (`unified_server.py`)

The server core that ties everything together. It:

1. Loads the graph registry at startup
2. Lazy-creates and caches `SPARQLServer` instances per graph on first use
3. Exposes 13 MCP tools that the AI assistant calls during conversation
4. Handles alias resolution, validation, and error reporting
5. Supports both stdio (local) and streamable-http (remote) transport

### SPARQLServer (`server.py`)

The existing per-graph query engine, reused unchanged. Each instance handles:

- **FROM clause injection** -- automatically scopes queries to the correct named graph
- **Ontology expansion** -- detects MONDO, UBERON, HP, GO URIs in queries and expands to include all descendants via Ubergraph
- **Query analysis** -- warns about missing LIMIT, ORDER BY, or edge property patterns
- **Result formatting** -- returns structured `{columns, data, count}` responses

## The 13 MCP Tools

The AI assistant uses these tools in sequence to navigate from a natural language question to structured cross-graph results, and to generate documentation and visualizations.

### Discovery Tools

| Tool | Purpose | When to Use |
|---|---|---|
| `list_graphs(domain?, entity_type?)` | Browse all 27 graphs with metadata | First call -- understand what data exists |
| `route_query(question)` | Match a natural language question to relevant graphs | When the user asks a question and you need to find the right graph(s) |
| `get_description(graph_name)` | Full description, example queries, identifier namespaces | Deep dive into a specific graph before querying |

### Schema and Query Tools

| Tool | Purpose | When to Use |
|---|---|---|
| `get_schema(graph_name)` | Classes, predicates, edge properties for a graph | **Always** before writing SPARQL for a graph |
| `query(graph_name, sparql)` | Execute SPARQL with ontology expansion and analysis | Primary query tool for individual graphs |
| `multi_graph_query(queries)` | Run different SPARQL per graph, merge results | Cross-graph analysis with `source_graph` column |
| `get_query_template(graph_name, relationship_name)` | SPARQL template showing RDF reification pattern for edge properties | When querying relationships with properties (e.g., differential expression with log2fc, p-values) |

### Cross-Graph Tools

| Tool | Purpose | When to Use |
|---|---|---|
| `get_join_strategy(graph_a, graph_b)` | Shared identifiers and join recommendations | Before merging results from two graphs |
| `lookup_uri(label)` | Find ontology URI by name via Ubergraph | When you have a term name and need its URI |
| `get_descendants(uri)` | Explore ontology hierarchy with distance | To see what subtypes exist under a concept |

### Visualization and Documentation Tools

| Tool | Purpose | When to Use |
|---|---|---|
| `visualize_schema(graph_name)` | Step-by-step workflow for generating a Mermaid class diagram of a graph's schema | When the user wants to see or save a visual schema diagram |
| `clean_mermaid_diagram(mermaid_content)` | Clean Mermaid diagrams by removing notes, empty braces, and invalid characters | Called automatically as part of `visualize_schema` workflow; can also be used standalone |
| `create_chat_transcript(graph_name?)` | Generate a markdown template for documenting a KG analysis session | When the user wants a reproducible record of the conversation |

## How the Components Interact

A typical cross-graph analysis follows this flow:

```
User Question
      │
      ▼
 ┌─────────────────┐
 │  1. DISCOVER     │  list_graphs() or route_query()
 │     Which graphs  │  → Registry keyword search
 │     are relevant? │  → Returns ranked candidates
 └────────┬──────────┘
          ▼
 ┌─────────────────┐
 │  2. UNDERSTAND   │  get_schema(graph) for each candidate
 │     What's the   │  → SPARQLServer.query_schema()
 │     schema?      │  → Classes, predicates, properties
 └────────┬──────────┘
          ▼
 ┌─────────────────┐
 │  3. QUERY        │  query(graph, sparql) per graph
 │     Get data     │  → FROM clause auto-injected
 │     from each    │  → Ontology URIs auto-expanded
 │     graph        │  → Results: {columns, data, count}
 └────────┬──────────┘
          ▼
 ┌─────────────────┐
 │  4. BRIDGE       │  get_join_strategy(graph_a, graph_b)
 │     How do       │  → Identifier mapping lookup
 │     identifiers  │  → Returns shared IDs + strategy
 │     connect?     │  → May suggest bridge graph
 └────────┬──────────┘
          ▼
 ┌─────────────────┐
 │  5. SYNTHESIZE   │  AI merges results using
 │     Combine and  │  identifier bridges, adds
 │     present      │  external sources (PubMed, etc.)
 └─────────────────┘
```

## Example: Cross-Graph Spaceflight Gene Expression Analysis

This example, drawn from a real session with the unified server, demonstrates how an AI assistant dynamically combines data from multiple knowledge graphs and PubMed to answer a complex biomedical question.

**User prompt:**
> Integrate GeneLab, SPOKE, and PubMed knowledge to characterize spaceflight-associated gene expression changes and their disease relevance for study OSD-161.

### Step 1: Discover and Inspect Schemas

The assistant calls `get_schema("spoke-genelab")` and `get_schema("spoke-okn")` to learn each graph's structure -- classes, predicates, edge property patterns, and URI conventions.

### Step 2: Query spoke-genelab for Differential Expression

Using the schema, the assistant writes SPARQL tailored to spoke-genelab's reification pattern for edge properties:

```sparql
PREFIX sglab: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?symbol ?log2fc ?adj_p_value
WHERE {
  <.../node/OSD-161> sglab:PERFORMED_SpAS ?assay .
  ?rel rdf:subject ?assay .
  ?rel rdf:predicate sglab:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG .
  ?rel rdf:object ?gene .
  ?rel sglab:log2fc ?log2fc .
  ?rel sglab:adj_p_value ?adj_p_value .
  ?gene sglab:symbol ?symbol .
}
```

**Result:** Top up-regulated genes including Fos (log2fc +1.96, adj_p 0.024), Btg2, Cited2, Dusp1. Top down-regulated: MHC class I genes H2-Q6, H2-Q7.

### Step 3: Map Mouse Genes to Human Orthologs

Still in spoke-genelab, the assistant queries the `IS_ORTHOLOG_MGiG` predicate to map mouse genes to human orthologs (e.g., mouse Fos → human FOS, NCBI Gene 2353).

### Step 4: Bridge Gene Identifiers Across Graphs

The assistant calls `get_join_strategy("spoke-genelab", "spoke-okn")` and learns:

- spoke-genelab uses **NCBI Gene IDs** and **gene symbols**
- spoke-okn uses **Ensembl IDs**
- The bridge graph **gene-expression-atlas-okn** stores both ID types

Using the bridge, the assistant converts NCBI Gene IDs to Ensembl IDs for querying spoke-okn.

### Step 5: Query spoke-okn for Disease Associations

With the correct Ensembl IDs, the assistant queries spoke-okn for gene-disease associations:

```sparql
PREFIX spoke: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?gene ?disease ?disease_label
WHERE {
  ?gene a biolink:Gene .
  ?disease spoke:ASSOCIATES_DaG ?gene .
  ?disease rdfs:label ?disease_label .
}
```

**Result:** FOS associated with diabetes, cardiomyopathy, depressive disorder, IBD. HLA genes associated with rheumatoid arthritis, psoriasis, viral susceptibility.

### Step 6: Enrich with PubMed Literature

Using a PubMed MCP server alongside the unified Proto-OKN server, the assistant searches for publications connecting these genes to spaceflight. Key finding: the Inspiration4 multi-omics study (Kim et al. 2024, Nature Communications) independently confirmed long-term MHC class I suppression in astronaut immune cells.

### Step 7: Synthesize

The assistant combines all results into a coherent narrative:

> Spaceflight induces a dual response in the adrenal gland: **(1) HPA axis stress activation** (Fos/Dusp1/Cited2/Btg2 up-regulated) alongside **(2) immune surveillance suppression** (MHC class I/II down-regulated). This creates an unfavorable state for long-duration missions -- elevated stress signaling coupled with reduced antigen presentation capacity. The disease associations to cardiovascular, metabolic, autoimmune, and neuropsychiatric conditions underscore the need for countermeasures.

### What Makes This Possible

This analysis required **no manual configuration** of endpoints, no pre-built federation queries, and no upfront knowledge of which graphs to use. The AI assistant dynamically:

1. Discovered relevant graphs via the registry
2. Learned each graph's schema on the fly
3. Wrote graph-specific SPARQL adapted to each schema
4. Used identifier bridges to connect results across graphs
5. Integrated external literature via a separate MCP server
6. Synthesized a domain-expert-level analysis

The unified server provided the infrastructure; the AI provided the reasoning.

## Available Knowledge Graphs

### By Domain

| Domain | Graphs |
|---|---|
| **Biology & Health** | spoke-okn, spoke-genelab, gene-expression-atlas-okn, biohealth, nde |
| **Toxicology & Chemistry** | biobricks-ice, biobricks-tox21, biobricks-toxcast, biobricks-aopwiki, biobricks-pubchem-annotations, biobricks-mesh |
| **Environment & Water** | sawgraph, hydrologykg, geoconnex, fiokg, spatialkg |
| **Climate & Earth Science** | climatemodelskg, nasa-gesdisc-kg, sockg |
| **Social & Urban** | dreamkg, scales, nikg, ruralkg, ufokn |
| **Technology & Manufacturing** | sudokn, securechainkg |
| **Wildlife** | wildlifekn |

## Installation

### Claude Desktop (local, stdio)

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "proto-okn": {
      "command": "/full/path/to/uv",
      "args": ["--directory", "/path/to/mcp-proto-okn", "run", "mcp-proto-okn-unified"]
    }
  }
}
```

Use `which uv` to find the full path. Claude Desktop has a limited PATH and may not find `uv` without it.

### Claude Code (local, stdio)

Add to `.mcp.json` in your project:

```json
{
  "mcpServers": {
    "proto-okn": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-proto-okn", "run", "mcp-proto-okn-unified"]
    }
  }
}
```

### Remote Deployment (HTTP)

Start the server:

```bash
uv run mcp-proto-okn-unified --transport streamable-http --port 8000
```

Connect from Claude Code:

```json
{
  "mcpServers": {
    "proto-okn": {
      "type": "url",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

For Claude Desktop remote connections, HTTPS with a valid domain is required. Use a reverse proxy (nginx, Caddy) or a tunnel (ngrok) for local testing.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MCP_PROTO_OKN_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `MCP_PROTO_OKN_HOST` | `0.0.0.0` | Bind address for HTTP |
| `MCP_PROTO_OKN_PORT` | `8000` | Bind port for HTTP |
| `MCP_PROTO_OKN_API_KEY` | *(none)* | Optional Bearer-token auth for HTTP |

## Testing

```bash
# Unit tests (no network, fast)
uv run python -m pytest tests/test_registry.py tests/test_identifier_mapping.py tests/test_unified_server.py -v

# Live integration tests (requires network access to frink.apps.renci.org)
uv run python -m pytest tests/test_real_data.py -v -m live

# All tests
uv run python -m pytest tests/ -v
```

## Project Structure

```
src/mcp_proto_okn/
├── unified_server.py      # Unified MCP server (13 tools + CLI entry point)
├── registry.py            # GraphRegistry + GraphInfo (graph catalog)
├── identifier_mapping.py  # Cross-graph identifier bridges + join strategies
├── server.py              # SPARQLServer (per-graph query engine, reused)
├── registry.json          # Packaged graph catalog (27 graphs)

config/
├── registry.json          # Source graph catalog
├── mcp.json               # Per-graph server configs (legacy)
├── mcp-unified.json       # Unified server config

scripts/
├── build_registry.py      # Generates registry.json from metadata

tests/
├── test_registry.py       # Registry unit tests (15 tests)
├── test_identifier_mapping.py  # Identifier mapping tests (17 tests)
├── test_unified_server.py # Unified server integration tests (11 tests)
├── test_real_data.py      # Live FRINK endpoint tests (7 tests)
├── fixtures/
│   └── test_registry.json # Test fixture (3 mock graphs)
```
