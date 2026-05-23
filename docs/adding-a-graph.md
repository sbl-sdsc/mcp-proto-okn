# Adding a New Knowledge Graph

This guide explains how to add a new knowledge graph to the unified MCP Proto-OKN server. The unified server reads [`config/registry.json`](../config/registry.json) to discover the graphs it exposes, but **`registry.json` is generated** — it should not be edited by hand. Direct edits will be overwritten the next time the registry is rebuilt.

The build script [`scripts/build_registry.py`](../scripts/build_registry.py) assembles the registry from the `metadata/` directory plus a few hardcoded mappings in the script itself. Adding a new graph means adding files under `metadata/` and updating those mappings, then re-running the build.

## Prerequisites

- The new graph must be hosted as a SPARQL endpoint on the OKN platform at `https://apps.okn.us/<name>/sparql` and registered in the [OKN Knowledge Graph Registry](https://registry.okn.us/registry/). The build script derives endpoint URLs from the graph name using that pattern.
- A working local checkout with `uv sync` completed (see [local installation](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/develop.md#option-2-uv-run--local-source-development-mode)).

## Step-by-Step

Substitute your graph name (kebab-case, e.g. `mygraph-okn`) for `<kg_name>` throughout.

### 1. Add the entity inventory

Create an entity inventory file at:

```text
metadata/entities/<kg_name>_entities.csv
```

This file should describe the classes and predicates used in the KG schema.

To generate an initial draft, run:

```bash
python scripts/extract_entities <kg_name>
```

Review the generated file and refine it manually as needed.

#### Populate entity metadata

Use a chat assistant with web search enabled, such as the latest versions of Claude Sonnet, Claude Opus, or GPT, to help populate the `Label` and `Description` columns.

Steps:

1. Attach `metadata/entities/<kg_name>_entities.csv` to the chat session.
2. Enable web search.
3. Run the prompt below.
4. Save the completed file as `metadata/entities/<kg_name>_entities.csv`.
5. Review the result manually before committing it.

#### Prompt

```text
Update the attached CSV file for kg_name = <kg_name>.

Use the KG registry page as the starting point:

https://registry.okn.us/registry/kgs/<kg_name>/

The CSV file must contain exactly 7 columns in this order:

1. URI — Full URI of the entity
2. Label — Human-readable label for the entity
3. Description — Comment, definition, or description of the entity
4. Type — Either "Class" or "Predicate"
5. EdgePropertyOf — If the entity is an edge property, specify the predicate it belongs to; otherwise leave empty
6. SourceClass — For predicates, the source class of the relationship; otherwise leave empty
7. TargetClass — For predicates, the target class of the relationship; otherwise leave empty

Search ontology files, GitHub repositories, registry links, schema files, documentation, and other linked resources to find missing labels and descriptions.

Requirements:

- Preserve existing valid values.
- Fill in missing `Label` and `Description` values where reliable information is available.
- Do not invent labels or descriptions when no reliable source is found.
- Do not add extra columns.
- Do not remove columns.
- Do not reorder columns.
- Keep the output as a valid CSV file.
- Return the completed CSV file.
```
---

After the assistant updates the file, review all changes manually. Verify that labels and descriptions are accurate, concise, and consistent with the KG source materials.

### 2. Add a description

Create a plain-text description file at:

```text
metadata/descriptions/<kg_name>.txt
```

This file should contain 1–3 paragraphs describing the knowledge graph. The text becomes the graph's `description_summary` in the registry and is used by LLMs to determine whether the graph is relevant to a user's question.

#### Generate a draft description

Use a chat assistant with web search enabled, such as the latest versions of Claude Sonnet, Claude Opus, or GPT, to generate an initial draft.

Steps:

1. Attach `metadata/entities/<kg_name>_entities.csv` to the chat session.
2. Enable web search.
3. Run the prompt below.
4. Save the completed description as `metadata/descriptions/<kg_name>.txt`.
5. Review the result manually before committing it.

#### Prompt

```text
Generate a description for kg_name = <kg_name>.

Use the attached entity inventory file as the primary source.

Use the KG registry page as an additional source:

https://raw.githubusercontent.com/frink-okn/okn-registry/refs/heads/main/docs/registry/kgs/<kg_name>

Search publicly available documentation, ontology files, GitHub repositories, registry links, schema files, and other linked resources to understand the KG.

Write a plain-text description of approximately 150 words.

The description should explain:

1. What the knowledge graph contains
2. What domain, entities, and relationships it covers
3. What kinds of questions it can help answer

Requirements:

- Be accurate, concise, and specific.
- Base the description only on reliable source material.
- Do not invent unsupported claims.
- Do not use Markdown headings, bullet points, or tables.
- Do not include citations or URLs in the final description.
- Return only the completed description text.
```
---

After the assistant generates the file, review it manually. Verify that the description is accurate, concise, and consistent with the KG source materials.

### 2. Add the entity inventory

Create an entity inventory file at:

```text
metadata/entities/<kg_name>_entities.csv
```

This file should describe the classes and predicates used in the KG schema.

To generate an initial draft, run:

```bash
python scripts/extract_entities <kg_name>
```

Review the generated file and refine it manually as needed.

#### Populate entity metadata

Use a chat assistant with web search enabled, such as the latest versions of Claude Sonnet, Claude Opus, or GPT, to help populate the `Label` and `Description` columns.

Steps:

1. Attach `metadata/entities/<kg_name>_entities.csv` to the chat session.
2. Enable web search.
3. Run the prompt below.
4. Save the completed file as `metadata/entities/<kg_name>_entities.csv`.
5. Review the result manually before committing it.

#### Prompt

```text
Update the attached CSV file for kg_name = <kg_name>.

Use the KG registry page as the starting point:

https://registry.okn.us/registry/kgs/<kg_name>/

The CSV file must contain exactly 7 columns in this order:

1. URI — Full URI of the entity
2. Label — Human-readable label for the entity
3. Description — Comment, definition, or description of the entity
4. Type — Either "Class" or "Predicate"
5. EdgePropertyOf — If the entity is an edge property, specify the predicate it belongs to; otherwise leave empty
6. SourceClass — For predicates, the source class of the relationship; otherwise leave empty
7. TargetClass — For predicates, the target class of the relationship; otherwise leave empty

Search ontology files, GitHub repositories, registry links, schema files, documentation, and other linked resources to find missing labels and descriptions.

Requirements:

- Preserve existing valid values.
- Fill in missing `Label` and `Description` values where reliable information is available.
- Do not invent labels or descriptions when no reliable source is found.
- Do not add extra columns.
- Do not remove columns.
- Do not reorder columns.
- Keep the output as a valid CSV file.
- Return the completed CSV file.
```

After the assistant updates the file, review all changes manually. Verify that labels and descriptions are accurate, concise, and consistent with the KG source materials.

### 3. Update `scripts/build_registry.py`

The build script holds three hardcoded dicts keyed by graph name. Add an entry for `<kg_name>` to each:

- **`DOMAIN_TAGS`** — a list of short tags. Existing examples: `biology`, `health`, `toxicology`, `geospatial`, `climate`, `social_determinants`, `genomics`, `pathways`. Reuse existing tags where possible so the `list_graphs(domain=...)` filter remains useful.
- **`IDENTIFIER_NAMESPACES`** — list of identifier systems used by the graph (e.g. `["MONDO", "Ensembl", "NCBI Gene"]`). This populates the cross-graph identifier bridge — see [identifier_mapping.py](../src/mcp_proto_okn/identifier_mapping.py) for the canonical names.
- **`EXAMPLE_QUERIES`** — list of natural-language questions the graph can answer well. The unified server surfaces these to the LLM as hints; 1–3 well-chosen questions are more useful than a long list.

If the graph is commonly referred to by a short alias (e.g. `spoke` → `spoke-okn`), add it to the `ALIASES` dict.

### 4. Rebuild the registry

```bash
uv run python scripts/build_registry.py
```

Expected output: `Built registry with <n> graphs → /path/to/config/registry.json`. Confirm the count went up by one and that your graph appears in the JSON.

### 5. Test locally

Restart your MCP client (the unified server is started by the client at session start, so any registry change requires a fresh session to be picked up). Then verify in Claude Code:

```
/mcp
```

`proto-okn` should still be connected. Then ask:

> List the available Proto-OKN knowledge graphs.

The new graph should appear with its `display_name`, `domain_tags`, and `description_summary`. Try a follow-up such as:

> What can I ask the `<kg_name>` graph about?

The LLM will use the entity inventory and example queries to answer.

### 6. (Optional) Add an overview document

If you want the new graph to appear in the README's "Knowledge Graph Overviews" table, generate an overview document:

> @<kg_name>: Give a high-level overview of this knowledge graph, including its main entities, relationships, and purpose. Then create a chat transcript.

Save the resulting transcript as `docs/examples/<name>_overview.md` and add a link to the appropriate domain column in the README's overview table.

## Submitting Changes

Open a pull request against [sbl-sdsc/mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn). The changed files in a typical "add a graph" PR are:

```
metadata/descriptions/<name>.txt           # new
metadata/entities/<name>_entities.csv      # new
scripts/build_registry.py                  # 3 dict additions
config/registry.json                       # regenerated
docs/examples/<name>_overview.md           # optional
README.md                                  # optional, if overview added
```
