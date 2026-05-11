# MCP Proto-OKN Server

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://img.shields.io/pypi/v/mcp-proto-okn?label=PyPI)](https://pypi.org/project/mcp-proto-okn/)

A single [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes **33 [Proto-OKN](https://www.proto-okn.net/) knowledge graphs** through one unified interface. The server enables AI assistants (Claude, ChatGPT, GitHub Copilot, etc.) to discover graphs, inspect their schemas, query them with SPARQL, bridge identifiers across graphs, and combine results from multiple sources — all through natural-language conversation. The graphs are hosted on the [FRINK](https://frink.renci.org/) federation platform.

> **Beta:** the proto-okn MCP server is in beta. We welcome feedback and bug reports via [issues](https://github.com/sbl-sdsc/mcp-proto-okn/issues).

### [Video introduction](https://www.youtube.com/watch?v=50L-tKCoXJE) · [Technical review presentation](https://nebigdatahub.org/wp-content/uploads/2026/01/MCP-Proto-OKN-Technical-Review.pdf)

---

## Features

- **🌐 Unified access** — one MCP server, 33 knowledge graphs, one endpoint
- **🔎 Graph discovery** — list, filter, and search graphs by domain, entity type, or natural language
- **📐 Schema inspection** — understand each graph's classes, predicates, and properties before writing queries
- **🧭 Per-graph SPARQL** — query any individual graph with automatic FROM-clause injection
- **🔗 Cross-graph bridging** — built-in identifier maps (Ensembl ↔ NCBI Gene ↔ Symbol; CAS, DTXSID, InChIKey; MONDO, FIPS, NAICS, …)
- **🧬 Multi-graph queries** — run different SPARQL across multiple graphs in a single call and merge results
- **🌳 Ontology-driven search expansion** — queries are automatically expanded using ontology hierarchies (MONDO, UBERON, HP, GO, CL, ChEBI, …) via [Ubergraph](https://frink.renci.org/registry/kgs/ubergraph/), so a query for "arthritic joint disease" matches all of its subtypes without manual enumeration
- **🖼️ Schema visualization & transcripts** — generate Mermaid class diagrams and chat transcripts directly from the conversation

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI Assistant (Claude, ChatGPT, …)               │
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
│  │ 13 MCP Tools  │  │Graph Registry│  │ Identifier Mapping           ││
│  │ list_graphs   │  │ 33 graphs    │  │ Gene: Ensembl ↔ NCBI ↔       ││
│  │ route_query   │  │ domain tags  │  │       Symbol (via bridge)    ││
│  │ get_schema    │  │ entity types │  │ Chemical: CAS, InChIKey,     ││
│  │ query         │  │ identifiers  │  │           DTXSID             ││
│  │ multi_graph   │  │ examples     │  │ Disease: MONDO               ││
│  │ join_strategy │  │              │  │ Location: FIPS, S2Cell       ││
│  │ lookup_uri    │  │              │  │ Industry: NAICS              ││
│  │ get_descend.  │  │              │  │                              ││
│  │ query_template│  │              │  │                              ││
│  │ viz_schema    │  │              │  │                              ││
│  │ chat_transcr. │  │              │  │                              ││
│  └──────┬────────┘  └──────────────┘  └──────────────────────────────┘│
│         │                                                             │
│  ┌──────▼──────────────────────────────────────────────────────────┐  │
│  │  Per-graph SPARQL engine (lazy-cached SPARQLServer instances)   │  │
│  │  • FROM clause injection (named graph)                          │  │
│  │  • Ontology expansion (MONDO, UBERON, HP, GO, CL, ChEBI, …)     │  │
│  │  • Query analysis and warnings                                  │  │
│  │  • Result formatting                                            │  │
│  └──────┬──────────────────────────────────────────────────────────┘  │
└─────────┼────────────────────────────────────────────────────────────┘
          │  SPARQL over HTTPS
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRINK Federation Platform                           │
│                    frink.apps.renci.org                                │
│                                                                       │
│  spoke-okn │ spoke-genelab │ biobricks-ice │ biobricks-tox21 │ …     │
│  sawgraph  │ dreamkg       │ scales        │ ruralkg        │ …     │
│                  … 33 named graphs total …                            │
│                                                                       │
│  + Ubergraph (ontology services: MONDO, UBERON, HP, GO, ChEBI, …)    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# For Users

This section is for people who want to **use** the unified server through an MCP-compatible client (Claude Desktop, ChatGPT, Claude Code, VS Code Insiders with GitHub Copilot, etc.). No installation, no local setup — the server is already hosted, you just point your client at it.

**Hosted endpoint URL:** `https://apps.okn.us/okn-mcp/mcp`

## Connecting Your Client

### Claude Desktop

1. Launch Claude Desktop → **Settings → Connectors → Add custom connector**
2. Name: `proto-okn`, URL: `https://apps.okn.us/okn-mcp/mcp`
3. Click **Configure** and set tool permissions to **Always allow**
4. In a new chat, click `+` and toggle `proto-okn` on. Toggle Web search off.

Full walkthrough with screenshots: **[Claude Desktop setup](docs/claude-setup.md)**.

> A Claude Pro or Max subscription is required for MCP connectors in Claude Desktop.

### ChatGPT

ChatGPT supports MCP services only in the web app (https://chatgpt.com) with **Developer mode** enabled. Then **Settings → Apps → Create app**, MCP Server URL `https://apps.okn.us/okn-mcp/mcp`.

Full walkthrough with screenshots: **[ChatGPT setup](docs/chatgpt-setup.md)**.

### Claude Code

Add to `.mcp.json` in your project root (or `~/.claude/settings.json` for all projects):

```json
{
  "mcpServers": {
    "proto-okn": {
      "type": "url",
      "url": "https://apps.okn.us/okn-mcp/mcp"
    }
  }
}
```

Verify with `/mcp` — you should see `proto-okn` connected.

### VS Code Insiders + GitHub Copilot

VS Code Insiders supports MCP in Agent mode with the GitHub Copilot extension. Use the same URL: `https://apps.okn.us/okn-mcp/mcp`.

---

## Example Prompts

Once the server is connected, try these conversational prompts in your client. The assistant will pick the right graphs, write the SPARQL, and combine results for you.

- Default: query across all Proto-OKN KGs
  > Generate a table of all Proto-OKN Knowledge Graphs with two columns: "KG Name" and "Description."
  →  [Result](docs/examples/proto-okn-overview.md)

- Target a specific KG with `@kg-name`
  > @spoke-genelab: Give a high-level overview of this knowledge graph, including its main entities, relationships, and purpose.

- Save a session
  > Create a chat transcript.

  The transcript downloads as `.md` or `.pdf` and includes the model name and version.

### Ontology-Driven Search Expansion

Queries are automatically expanded using ontology hierarchies (MONDO, HP, GO, UBERON, ChEBI, …) via [Ubergraph](https://frink.renci.org/registry/kgs/ubergraph/) to include all descendant concepts. A search for "cardiovascular disease" automatically matches every subtype the data is tagged at — without you having to enumerate them.

1. **[Cardiovascular Disease Datasets — full walkthrough (nde)](docs/examples/cardiovascular-disease-ontology-expansion.md)** — shows how one URI in the query expands to 1,592 descendant concepts and matches 284 disease subtypes
2. [Arthritic Joint Disease Datasets (nde)](docs/examples/nde-arthritic_joint_disease_ontology_expansion.md)
3. [Space Flight Studies Investigating Muscles (spoke-genelab)](docs/examples/spoke-genelab_muscle_studies_ontology_expansion.md)

### Knowledge Graph Overviews & Class Diagrams

Each link points to a chat transcript that generated an overview and class diagram for a Proto-OKN Theme 1 KG.

| 🧬 Biology & Health | 🌱 Environment | ⚖️ Justice | 🛠️ Technology & Manufacturing | NASA/NIH/ARCH(*)
|--------------------|---------------|-----------|-------------------------------|-------------|
| [biobricks-aopwiki](docs/examples/biobricks-aopwiki_overview.md) | [sawgraph](docs/examples/sawgraph_overview.md) | [ruralkg](docs/examples/ruralkg_overview.md) | [securechainkg](docs/examples/securechainkg_overview.md) | [nasa-gesdisc-kg](docs/examples/nasa-gesdisc-kg_overview.md) |
| [biobricks-ice](docs/examples/biobricks-ice_overview.md) | [fiokg](docs/examples/fiokg_overview.md) | [scales](docs/examples/scales_overview.md) | [sudokn](docs/examples/sudokn_overview.md) | [nde](docs/examples/nde_overview.md)
| [biobricks-mesh](docs/examples/biobricks-mesh_overview.md) | [geoconnex](docs/examples/geoconnex_overview.md) | [nikg](docs/examples/nikg_overview.md) | | [gene-expression-atlas-okn](docs/examples/gene-expression-atlas-okn_overview.md) |
| [biobricks-pubchem-annotations](docs/examples/biobricks-pubchem-annotations_overview.md) | [spatialkg](docs/examples/spatialkg_overview.md) | [dreamkg](docs/examples/dreamkg_overview.md) |  | [biomarkerkg](docs/examples/biomarkerkg-overview.md)
| [biobricks-tox21](docs/examples/biobricks-tox21_overview.md) | [hydrologykg](docs/examples/hydrologykg_overview.md) |  |  | [evoweb](docs/examples/evoweb-overview.md)
| [biobricks-toxcast](docs/examples/biobricks-toxcast_overview.md) | [ufokn](docs/examples/ufokn_overview.md) |  |  | [oard-kg](docs/examples/oard-kg-overview.md)
| [spoke-genelab](docs/examples/spoke-genelab_overview.md) | [wildlifekn](docs/examples/wildlifekn_overview.md) |  |  | [ncipidkg](docs/examples/ncipidkg-overview.md)
| [spoke-okn](docs/examples/spoke-okn_overview.md) | [climatemodelskg](docs/examples/climatemodelskg_overview.md) |  |  | [pankgraph](docs/examples/pankgraph-overview.md)
|  | [sockg](docs/examples/sockg_overview.md) |  | | [prokn](docs/examples/prokn_overview.md)

**(*) ARCH: Advancing Research Capacity in Health, NSF supplemental awards.**

### Use Cases

1. [Spaceflight Missions (spoke-genelab)](docs/examples/spoke-genelab_breakdown.md)
2. [Spaceflight Gene Expression Analysis (spoke-genelab, spoke-okn)](docs/examples/spoke_spaceflight_analysis.md)
3. [Spaceflight Gene Expression with Literature Analysis (spoke-genelab, spoke-okn, MCP:PubMed)](docs/examples/spoke-genelab-OSD-244_verbatim.md)
4. [Spaceflight Gene Expression — Disease Associations (spoke-genelab, spoke-okn, prokn, MCP:Open Targets, MCP:PubMed)](docs/examples/space-flight-disease-relationships.md)
5. [Spaceflight Microbiome Investigation (spoke-genelab, spoke-okn, MCP:PubMed)](docs/examples/spaceflight_microbiome_cross-graph_investigation.md)
6. [Disease Prevalence in the US (spoke-okn)](docs/examples/us_county_disease_prevalence.md)
7. [Disease Prevalence — Socio-Economic Factors Correlation (spoke-okn)](docs/examples/disease_socio_economic_correlation.md)
8. [NIAID Data Exploration — COVID-19 Vaccine Research (nde)](docs/examples/nde_COVID-19-Vaccine-Research.md)
9. [Diabetic Nephropathy Meta-Analysis (gene-expression-atlas-okn)](docs/examples/diabetic-nephropathy-meta-analysis.md)
10. [Diabetic Nephropathy Differential Expression Analysis (gene-expression-atlas-okn, ARCHS4)](docs/examples/dn_differential_expression_archs4_analysis.md)
11. [APOE Gene Info (prokn)](docs/examples/prokn-apoe-gene.md)
12. [Prostate Cancer Biomarkers (biomarkerkg)](docs/examples/biomarkerkg-prostate-cancer.md)
13. [Marfan Syndrome Phenotypes (oard-kg)](docs/examples/oard-kg-marfan-syndrom-phenotypes.md)
14. [Pancreatic Acinar Cell Adhesion Genes (pankgraph)](docs/examples/pankgraph-pancreatic-acinar-cell-adhesion-genes.md)
15. [Contamination at Superfund Sites (spoke-okn)](docs/examples/superfund-contaminants.md)
16. [PFOA in Drinking Water (spoke-okn)](docs/examples/spoke_okn_pfoa_drinking_water.md)
17. [Data about PFOA (spoke-okn, biobricks-toxcast)](docs/examples/pfoa_data_spoke_okn_biobricks_toxcast.md)
18. [PFAS Environmental Health Analysis (sawgraph, spoke-okn, biobricks-ice)](docs/examples/pfas_environmental_health_kg_analysis.md)
19. [Biological Targets for PFOA (biobricks-toxcast, biobricks-ice, biobricks-aopwiki, spoke-okn)](docs/examples/biobricks_toxcast_PFOA_targets.md)
20. [PFOA Safety Profile (biobricks-ice, biobricks-aopwiki, sawgraph, spoke-okn)](docs/examples/pfoa-safety-profile.md)
21. [Bisphenol A Safety Profile (biobricks-ice, biobricks-aopwiki, spoke-okn)](docs/examples/bpa-safety-profile.md)
22. [Criminal Justice Patterns (scales)](docs/examples/scales_criminal_justice_analysis.md)
23. [Drug Possession Charges (scales)](docs/examples/scales_drug_possession.md)
24. [Environmental Justice (sawgraph, scales, spatialkg, spoke-okn)](docs/examples/environmental-justice-kg-analysis.md)
25. [Rural Health Access (ruralkg, dreamkg, spoke-okn)](docs/examples/rural-health-access-mapping.md)
26. [Michigan Flooding Event (ufokn)](docs/examples/ufokn_michigan_flood.md)
27. [Flooding and Socio-Economic Factors (ufokn, spatialkg, spoke-okn)](docs/examples/flooding-socioeconomic-correlation.md)
28. [Philadelphia Area Incidents (nikg)](docs/examples/nikg_philadelphia_incidents.md)
29. [Mining Suppliers in North Dakota (sudokn)](docs/examples/sudokn_mining_suppliers.md)

### Proto-OKN Integration Opportunities

1. [Cross-KG Geolocation Data Exploration](docs/examples/cross-kg-geolocation-analysis.md)
2. [Cross-KG Chemical Compound Data Exploration](docs/examples/cross-kg-compound-analysis.md)
3. [Cross-KG Bio Data Exploration (Opus 4.7)](docs/examples/cross-graph-opportunities-bio-opus4.7.md)
4. [Cross-KG Bio Data Exploration (Sonnet 4.6)](docs/examples/cross-graph-opportunities-bio-sonnet4.7.md)

### Cross-Platform LLM Benchmarks

The same prompt run across Claude Desktop and VS Code Insiders with several LLMs.

| Query | Claude Sonnet 4.5 (Desktop) | Claude Sonnet 4.5 (VS Code) | Gemini 3 Pro | Groq Code Fast 1 | GPT-5.2 |
|-------|-----------------------------|-----------------------------|--------------|------------------|---------|
| **Spaceflight Missions** | [link](docs/examples/spacex-missions-sonnet-4.5-claude.md) | [link](docs/examples/spacex-missions-sonnet-4.5-vs-studio.md) | [link](docs/examples/spacex-missions-Gemini-3-Pro.md) | [link](docs/examples/spacex-missions-Gorc-Code-Fast-1.md) | [link](docs/examples/spacex-missions-GPT-5.2.md) |
| **Gene Expression Analysis** | [link](docs/examples/OSD-161-sonnet-4.5-claude.md) | [link](docs/examples/OSD-161-sonnet-4.5-vs-studio.md) | [link](docs/examples/OSD-161_Gemini-3-ProPreview-vs-studio.md) | [link](docs/examples/OSD-161-Groc-Code-Fact-1-vs-studio.md) | [link](docs/examples/OSD-161-GPT-5.2-vs-studio.md) |

[Benchmarks (in progress)](docs/benchmarks.md) — mcp-proto-okn vs. SPARQL ground-truth evaluation.

---

## Available Knowledge Graphs

| Domain | Graphs |
|---|---|
| **Biology & Health** | spoke-okn, spoke-genelab, gene-expression-atlas-okn, biohealth, nde, prokn, biomarkerkg, evoweb, ncipidkg, oard-kg, pankgraph |
| **Toxicology & Chemistry** | biobricks-ice, biobricks-tox21, biobricks-toxcast, biobricks-aopwiki, biobricks-pubchem-annotations, biobricks-mesh |
| **Environment & Water** | sawgraph, hydrologykg, geoconnex, fiokg, spatialkg |
| **Climate & Earth Science** | climatemodelskg, nasa-gesdisc-kg, sockg |
| **Social & Urban** | dreamkg, scales, nikg, ruralkg, ufokn |
| **Technology & Manufacturing** | sudokn, securechainkg |
| **Wildlife** | wildlifekn |

The authoritative list is [`config/registry.json`](config/registry.json) — generated from the metadata sources described below.

---

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

For an end-to-end AWS recipe, see [Deploying on AWS](docs/deploy-aws.md).

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

Full API reference: **[docs/api.md](docs/api.md)**.

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

# Live integration tests (requires network access to frink.apps.renci.org)
uv run python -m pytest tests/test_real_data.py -v -m live

# All tests
uv run python -m pytest tests/ -v
```

## Adding a New Knowledge Graph

See **[Adding a New Knowledge Graph](docs/adding-a-graph.md)** for the full step-by-step. In brief:

1. Add `metadata/descriptions/<name>.txt` (1–3 paragraph description).
2. Add `metadata/entities/<name>_entities.csv` (classes, predicates, edge properties).
3. Update the `DOMAIN_TAGS`, `IDENTIFIER_NAMESPACES`, and `EXAMPLE_QUERIES` dicts in [`scripts/build_registry.py`](scripts/build_registry.py).
4. Run `uv run python scripts/build_registry.py` to regenerate `config/registry.json`.
5. Restart your MCP client and test with `list_graphs` / `@<name>`.

The graph must be hosted on FRINK at `https://frink.apps.renci.org/<name>/sparql` — the registry builder assumes that endpoint pattern.

## Building and Publishing

See **[docs/build_publish.md](docs/build_publish.md)** (maintainers only — PyPI release workflow).

---

## Troubleshooting

**MCP server not appearing in Claude Desktop**
- Completely quit and restart Claude Desktop (closing the window is not enough)
- Validate your JSON config (attach the file to a chat and ask Claude to fix syntax errors)
- For local installs, verify `uvx` is on PATH (`which uvx`); if not, use the absolute path in `command`

**Connection errors**
- Check that the FRINK endpoints are reachable: `curl https://frink.apps.renci.org/spoke-okn/sparql`
- Some FRINK endpoints may have rate limits or temporary downtime

**Slow or hung queries**
- Complex SPARQL can take time; break it into smaller parts
- Ontology expansion across very broad concepts (e.g. "disease") may take several seconds

## License

This project is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE).

## Citation

```bibtex
@software{rose2025mcp-proto-okn,
  title={MCP Server Proto-OKN},
  author={Rose, P.W. and Good, B.M. and Nelson, C.A. and Saravia-Butler, A.M. and Shi, Y. and Su, A.I. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/sbl-sdsc/mcp-proto-okn}
}

@software{rose2025spoke-genelab,
  title={NASA SPOKE-GeneLab Knowledge Graph},
  author={Rose, P.W. and Nelson, C.A. and Gebre, S.G. and Saravia-Butler, A.M. and Soman, K. and Grigorev, K.A. and Sanders, L.M. and Costes, S.V. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/BaranziniLab/spoke_genelab}
}
```

### Related Publications

- Nelson, C.A., Rose, P.W., Soman, K., Sanders, L.M., Gebre, S.G., Costes, S.V., Baranzini, S.E. (2025). "Nasa Genelab-Knowledge Graph Fabric Enables Deep Biomedical Analysis of Multi-Omics Datasets." *NASA Technical Reports*, 20250000723. [Link](https://ntrs.nasa.gov/citations/20250000723)
- Sanders, L., Costes, S., Soman, K., Rose, P., Nelson, C., Sawyer, A., Gebre, S., Baranzini, S. (2024). "Biomedical Knowledge Graph Capability for Space Biology Knowledge Gain." *45th COSPAR Scientific Assembly*, July 13-21, 2024. [Link](https://ui.adsabs.harvard.edu/abs/2024cosp...45.2183S/abstract)

## Acknowledgments

### Funding

- **National Science Foundation** Award [#2333819](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333819): "Proto-OKN Theme 1: Connecting Biomedical information on Earth and in Space via the SPOKE knowledge graph"
- **National Science Foundation** Award [#2535091](https://www.nsf.gov/awardsearch/show-award?AWD_ID=2535091): "Proto-OKN Theme 2: OKN-Fabric"

### Related Projects

- [Proto-OKN Project](https://www.proto-okn.net/) — Prototype Open Knowledge Network initiative
- [FRINK Platform](https://frink.renci.org/) — Knowledge-graph hosting infrastructure
- [Knowledge Graph Registry](https://frink.renci.org/registry/) — Catalog of available knowledge graphs
- [Model Context Protocol](https://modelcontextprotocol.io/) — AI-assistant integration standard
- [Original MCP Server SPARQL](https://github.com/ekzhu/mcp-server-sparql/) — Base implementation reference

---

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/sbl-sdsc/mcp-proto-okn).*
