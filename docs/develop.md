# For Developers

This section is for people who want to **run the server locally**, **contribute code**, or **host their own copy**. The unified server is a small Python package; runtime requirements are minimal (a `t3.small` is plenty — it doesn't host data, just proxies SPARQL to FRINK).

## Running Locally

There are three supported ways to run the server locally — pick whichever matches your workflow.

### Option 1: `uvx` — published PyPI package (no clone)

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation/), then add to your MCP client config:

```json
{
  "mcpServers": {
    "proto-okn": {
      "command": "uvx",
      "args": ["mcp-proto-okn-unified"]
    }
  }
}
```

`uvx` downloads and runs the latest release automatically. Best when you want a stable local process without managing dependencies.

### Option 2: `uv run` — local source (development mode)

For contributors and anyone testing local changes.

```bash
git clone https://github.com/sbl-sdsc/mcp-proto-okn.git
cd mcp-proto-okn
uv sync
uv run mcp-proto-okn-unified --help
```

Then wire it into your MCP client:

```json
{
  "mcpServers": {
    "proto-okn": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-proto-okn", "run", "mcp-proto-okn-unified"]
    }
  }
}
```

Use an **absolute path** — `~` and relative paths won't resolve correctly from inside an MCP client.

> If your MCP client (especially Claude Desktop) reports `command not found: uv`, replace `"command": "uv"` with the full path from `which uv` (often `/Users/yourname/.local/bin/uv`).

### Option 3: Docker

```bash
docker build -t mcp-proto-okn .
docker run -p 8000:8000 -e MCP_PROTO_OKN_TRANSPORT=streamable-http mcp-proto-okn
```

Then point your client at the container:

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

## Transport Modes

The server supports two transports:

- **`stdio`** (default) — local subprocess, used by `uvx mcp-proto-okn-unified`
- **`streamable-http`** — HTTP, for hosting a server that multiple clients connect to over the network

Start in HTTP mode:

```bash
uv run mcp-proto-okn-unified --transport streamable-http --port 8000
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MCP_PROTO_OKN_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `MCP_PROTO_OKN_HOST` | `0.0.0.0` | Bind address for HTTP transport |
| `MCP_PROTO_OKN_PORT` | `8000` | Bind port for HTTP transport |
| `MCP_PROTO_OKN_API_KEY` | *(none)* | Optional Bearer-token auth for HTTP |

CLI flags `--transport`, `--host`, `--port` override the environment variables.

### Claude Desktop (remote / HTTPS)

Claude Desktop requires HTTPS with a valid domain name for remote MCP servers (it does **not** support `http://localhost`). To host your own:

1. Deploy the server to a host with a domain name
2. Set up HTTPS via a reverse proxy (nginx, Caddy) or a managed service
3. Optionally set `MCP_PROTO_OKN_API_KEY` for Bearer-token auth

```json
{
  "mcpServers": {
    "proto-okn": {
      "type": "url",
      "url": "https://your-domain.example.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY_HERE" }
    }
  }
}
```

For an end-to-end AWS recipe, see [Deploying on AWS](deploy-aws.md).

## How the Server Is Structured

```
src/mcp_proto_okn/
├── unified_server.py      # MCP server + 13 tools + CLI entry point
├── registry.py            # GraphRegistry + GraphInfo (graph catalog)
├── identifier_mapping.py  # Cross-graph identifier bridges + join strategies
├── server.py              # SPARQLServer (per-graph query engine)
└── registry.json          # Packaged graph catalog (33 graphs)

config/
└── registry.json          # Source graph catalog (build artifact, packaged with the wheel)

metadata/
├── descriptions/<kg>.txt              # Per-graph description text
└── entities/<kg>_entities.csv         # Per-graph class/predicate inventory

scripts/
└── build_registry.py                  # Regenerates config/registry.json from metadata

tests/
├── test_registry.py
├── test_identifier_mapping.py
├── test_unified_server.py
└── test_real_data.py                  # Live FRINK endpoint tests (network required)
```

### The 13 MCP Tools

The AI assistant uses these tools in sequence to navigate from a natural-language question to structured cross-graph results.

| Tool | Purpose |
|---|---|
| `list_graphs(domain?, entity_type?)` | Browse all 33 graphs with metadata |
| `route_query(question)` | Match a natural-language question to relevant graphs |
| `get_description(graph_name)` | Full description, example queries, identifier namespaces |
| `get_schema(graph_name)` | Classes, predicates, edge properties for a graph |
| `query(graph_name, sparql)` | SPARQL with auto FROM clause and ontology expansion |
| `multi_graph_query(queries)` | Run different SPARQL per graph; merge with `source_graph` column |
| `get_query_template(graph_name, relationship_name)` | SPARQL template for RDF-reified edge properties |
| `get_join_strategy(graph_a, graph_b)` | Shared identifiers and join recommendations |
| `lookup_uri(label)` | Find ontology URI by name via Ubergraph |
| `get_descendants(uri)` | Explore ontology hierarchy with distance |
| `visualize_schema(graph_name)` | Step-by-step workflow for a Mermaid class diagram |
| `clean_mermaid_diagram(mermaid_content)` | Strip notes / empty braces / invalid chars from Mermaid output |
| `create_chat_transcript(graph_name?)` | Markdown template for documenting an analysis session |

Full API reference: **[docs/api.md](api.md)**.

### Components

**Graph Registry (`registry.py` + `registry.json`)** — a structured catalog of all 33 graphs. Each entry contains `name`, `display_name`, `endpoint_url`, `domain_tags`, `description_summary`, `entity_types`, `identifier_namespaces`, `example_queries`, and optional `aliases`. The registry enables **discovery without querying**.

**Identifier Mapping (`identifier_mapping.py`)** — a static bridge table that maps identifier types to graphs and URI patterns, so the assistant can pick the right join key when bridging two graphs:

| Category | Identifier Types | Graphs |
|---|---|---|
| **Genes** | Ensembl, NCBI Gene, Symbol | spoke-okn, spoke-genelab, gene-expression-atlas-okn, biobricks-ice |
| **Chemicals** | CAS, DTXSID, InChIKey | biobricks-tox21, biobricks-ice, biobricks-toxcast, sawgraph, spoke-okn |
| **Diseases** | MONDO | spoke-okn, biohealth |
| **Locations** | FIPS, S2Cell | spoke-okn, nikg, ruralkg, spatialkg, hydrologykg, ufokn, fiokg |
| **Biomedical** | MeSH, ChEBI, UBERON | biobricks-mesh, biohealth, spoke-okn, spoke-genelab |
| **Industry** | NAICS | fiokg, sudokn |

The `gene-expression-atlas-okn` graph stores both NCBI Gene IDs and Ensembl IDs, making it a natural bridge between graphs that use different gene-identifier systems.

**SPARQLServer (`server.py`)** — the per-graph query engine. Each instance handles FROM-clause injection (auto-scoping to the named graph), ontology expansion (MONDO/UBERON/HP/GO/CL/ChEBI URIs in the query are expanded to descendants via Ubergraph), query analysis (warnings for missing `LIMIT`, `ORDER BY`, edge-property patterns), and result formatting.

**Unified Server (`unified_server.py`)** — loads the registry at startup, lazy-creates and caches a `SPARQLServer` per graph on first use, exposes the 13 MCP tools, handles alias resolution, and supports both `stdio` and `streamable-http` transports.

## Testing

```bash
# Unit tests (no network, fast)
uv run python -m pytest tests/test_registry.py tests/test_identifier_mapping.py tests/test_unified_server.py -v

# Live integration tests (requires network access to apps.okn.us)
uv run python -m pytest tests/test_real_data.py -v -m live

# All tests
uv run python -m pytest tests/ -v
```

## Adding a New Knowledge Graph

See **[Adding a New Knowledge Graph](adding-a-graph.md)** for the full step-by-step. In brief:

1. Add `metadata/descriptions/<name>.txt` (1–3 paragraph description).
2. Add `metadata/entities/<name>_entities.csv` (classes, predicates, edge properties).
3. Update the `DOMAIN_TAGS`, `IDENTIFIER_NAMESPACES`, and `EXAMPLE_QUERIES` dicts in [`scripts/build_registry.py`](../scripts/build_registry.py).
4. Run `uv run python scripts/build_registry.py` to regenerate `config/registry.json`.
5. Restart your MCP client and test with `list_graphs` / `@<name>`.

The graph must be hosted on the OKN platform at `https://apps.okn.us/<name>/sparql` and registered in the [OKN Knowledge Graph Registry](https://registry.okn.us/registry/) — the registry builder assumes that endpoint pattern.

## Building and Publishing

See **[docs/build_publish.md](build_publish.md)** (maintainers only — PyPI release workflow).
