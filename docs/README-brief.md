# How the Server Works — Brief

A one-page condensation of the [full pseudocode specification](README.md), which
carries the sub-procedures, measurements, and a map from every procedure to its
implementing source line.

## The core concept

**The server does not translate natural language into SPARQL.** The language
model on the other side of the MCP connection does. The server supplies the
grounding that translation requires, and enforces the invariants its output must
satisfy.

| The model does | The server does |
|---|---|
| Interpret the question | Rank a catalog of graphs by lexical overlap |
| Choose the graphs | Serve per-graph schemas, incl. edge properties |
| Write the SPARQL | Rewrite it for dataset scoping and ontology closure |
| Join the results | Serve a curated identifier-bridge table |

Nothing in the server involves embeddings, learning, or training. Every
procedure is deterministic given its inputs and the state of the endpoints.

## Data flow

```
  LLM client ──MCP(stdio|http)──▶ UnifiedSPARQLServer ──HTTPS──▶ FRINK federation
                                   │  registry.json              apps.okn.us
                                   │  IDENTIFIER_BRIDGES         <…/kg/spoke-okn>
                                   │  SPARQLServer per graph     <…/kg/ubergraph>
                                   ▼
                    raw.githubusercontent.com  metadata/entities/<kg>_entities.csv
                    (curated schemas; FRINK registry pages fetched the same way)
```

## Control flow: one question, end to end

```
 1  [model]   reads the question
 2  [server]  route_query  → all graphs ranked by weighted keyword overlap
 3  [model]   selects graphs from the ranking + metadata
 4  [server]  get_schema   → classes, predicates, edge properties (per graph)
 5  [server]  lookup_uri   → label "arthritis" → MONDO_0005578   (if needed)
 6  [model]   writes one SPARQL query per graph
 7  [server]  query / multi_graph_query  → the pipeline below, per graph
 8  [server]  get_join_strategy(a, b)    → the identifier to join on
 9  [model]   joins, synthesizes, answers
```

Steps 1, 3, 6 and 9 are the model's judgment. Everything else is deterministic.
The server holds no state between calls apart from its per-graph caches (HTTP
client, schema, edge properties).

Three further tools sit outside this loop: `visualize_schema`,
`clean_mermaid_diagram` and `create_chat_transcript` return instructions or
cleaned text for reporting a session, not graph data.

## The query pipeline

```
EXECUTE(q):
  1  refuse if q has SERVICE outside apps.okn.us, or a variable endpoint
  2  detect OBO URIs in q; fetch their descendants from <…/kg/ubergraph>
  3  rewrite: <MONDO_x> → ?var + VALUES ?var {subtree}
     split into batches if the expansion totals more than 20 URIs
  4  strip FILTER(?x IN ()) clauses that would match nothing
  5  prepend FROM <…/kg/{graph}>, plus FROM NAMED for every GRAPH <iri> in q
     ▷ skipped entirely if q scopes itself, or uses GRAPH ?var
  6  warn: LIMIT without ORDER BY; edge predicate without RDF reification
  7  execute each batch, merge, return {columns, data, count} + warnings
```

Ontology expansion (2–3) pre-fetches the closure and injects it as `VALUES`
rather than using a property path, because the closure lives in a different
named graph than the data.

## Cross-graph joins

The graphs share no primary keys: one gene is an Ensembl ID here, an NCBI Entrez
ID there, a bare symbol elsewhere. `IDENTIFIER_BRIDGES` is a curated map
`identifier_type → graph → {property | uri_pattern}` over 13 identifier types
(genes, chemicals, diseases, locations, vocabularies, industry codes).

```
SUGGEST-JOIN-STRATEGY(a, b):
  common ← identifier types present in both graphs
  if common ≠ ∅       → join directly, naming where each graph stores the key
  else if both carry gene IDs in disjoint namespaces
                      → bridge through gene-expression-atlas-okn,
                        which stores NCBI, Ensembl and symbol on one node
  else                → cannot join
```

Results are stacked under a `source_graph` column, never auto-joined; the model
performs the join on the key the strategy names.

## Invariants worth knowing

Each guards a failure that is **silent** — a plausible, smaller, wrong number
rather than an error.

- **`FROM` without `FROM NAMED`** leaves the dataset with no named graphs, so
  every `GRAPH <iri>` block matches the empty graph. Measured: 0 rows instead of
  1592.
- **`SERVICE` outside the federation** returns results the federation cannot
  reproduce. Measured: 1,628 descendants externally vs. 1,592 in-federation.
- **No depth bound on ontology expansion.** The federation's `ubergraph` is a
  materialized closure, so one hop is the whole subtree; the depth-bounded
  `UNION` form it replaced timed out past depth ~6.
- **`VALUES` on the query side, never `LCASE` on the stored side.** A function
  on the stored value defeats the index: ~16s and HTTP 429, vs. ~0.3s.
