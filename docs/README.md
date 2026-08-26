# How the Server Works — A Pseudocode Specification

This document specifies the mcp-proto-okn unified server as pseudocode. It is
intended to be read *before* the source, and to be complete enough that a reader
can assess the method without opening a `.py` file. Section 13 maps every
procedure here to the function that implements it. For a one-page summary of
the core concepts and control flow, see **[README-brief.md](README-brief.md)**.

## Scope, and one structural fact

The server does **not** translate natural language into SPARQL.

That translation is performed by the large language model on the other side of
the MCP connection. What the server contributes is everything the model needs in
order to do it against real data, plus a set of invariants the model's output
must satisfy before it reaches an endpoint:

| The model does | The server does |
|---|---|
| Interpret the question | Supply a catalog of graphs and a lexical ranking over it |
| Choose which graphs to use | Supply per-graph schemas: classes, predicates, edge properties |
| Write the SPARQL | Rewrite it for correct dataset scoping and ontology closure |
| Decide how to join results | Supply a curated identifier-bridge table and join strategies |
| Interpret the answer | Execute, batch, merge, and annotate results with warnings |

This division matters for interpreting the method. The system's behaviour is a
joint product of a general-purpose model and a set of grounded, deterministic
tools; the tools are what this document specifies. Nothing below involves
learning, embeddings, or training. Every procedure is deterministic given its
inputs and the state of the endpoints.

Throughout, *the federation* means the FRINK SPARQL service at
`https://apps.okn.us/federation/sparql`, which hosts every Proto-OKN knowledge
graph as a named graph, along with an `ubergraph` named graph holding the OBO
ontology closure.

## 0. Notation

```
PROCEDURE-NAME(arg1, arg2)          procedure definition
x ← expr                            assignment
A[k]                                lookup in map or array
⟨a, b⟩                              tuple
∅                                   empty set / map / list
|A|                                 size of A
"literal"                           string literal
▷ comment                           commentary
```

Procedures return maps with named fields, written `{field: value, …}`, matching
the JSON objects the MCP tools actually return.

---

## 1. Architecture

```
      ┌─────────────────────────────────────────────┐
      │  LLM client (Claude Desktop, ChatGPT, …)     │
      │  - reads the question                        │
      │  - chooses tools, writes SPARQL              │
      └───────────────────┬─────────────────────────┘
                          │  MCP (stdio | streamable-http)
      ┌───────────────────▼─────────────────────────┐
      │  UnifiedSPARQLServer            13 tools     │
      │  ┌────────────┐  ┌──────────────────────┐    │
      │  │GraphRegistry│  │IDENTIFIER_BRIDGES    │    │
      │  │ catalog +   │  │ static bridge table  │    │
      │  │ lexical rank│  │ + join strategies    │    │
      │  └────────────┘  └──────────────────────┘    │
      │  ┌──────────────────────────────────────┐    │
      │  │ SPARQLServer  (one per graph, cached)│    │
      │  │  guard → expand → clean → scope →    │    │
      │  │  analyze → execute → merge           │    │
      │  └──────────────────────────────────────┘    │
      └───────────────────┬─────────────────────────┘
                          │  HTTPS
      ┌───────────────────▼─────────────────────────┐
      │  FRINK federation  apps.okn.us              │
      │  <…/kg/spoke-okn>  <…/kg/ubergraph>  …      │
      └─────────────────────────────────────────────┘
```

Two out-of-band data sources are fetched over HTTPS on demand: the FRINK
registry page for a graph's prose description, and this repository's
`metadata/entities/<kg>_entities.csv` for its curated schema inventory. Both
degrade to empty rather than to an error if unreachable.

### The 13 tools, and where each is specified

| Function | Tools | Specified in |
|---|---|---|
| Graph discovery | `list_graphs`, `route_query`, `get_description` | §4 |
| Schema and query construction | `get_schema`, `get_query_template` | §5 |
| Query execution | `query`, `multi_graph_query` | §6, §9 |
| Ontology and federation | `lookup_uri`, `get_descendants`, `get_join_strategy` | §7, §8 |
| Documentation and visualization | `visualize_schema`, `clean_mermaid_diagram`, `create_chat_transcript` | §10 |

---

## 2. Startup

```
MAIN()
 1  args ← PARSE-ARGS()                    ▷ --registry, --transport, --host, --port
 2  registry ← LOAD-REGISTRY(args.registry)
 3  servers ← ∅                            ▷ graph name → SPARQLServer, lazily filled
 4  transport ← args.transport or ENV["MCP_PROTO_OKN_TRANSPORT"] or "stdio"
 5  mcp ← NEW-MCP-SERVER(instructions = workflow guidance for the model)
 6  for each of the 13 tools:
 7      REGISTER-TOOL(mcp, tool)           ▷ name, signature, docstring → MCP tool schema
 8  if transport = "stdio"
 9      RUN-STDIO(mcp)
10  else
11      app ← HTTP-APP(mcp)
12      app ← ADD-HEALTH-ROUTES(app)       ▷ /health /healthz /livez /readyz, unauthenticated
13      app ← WRAP-WITH-API-KEY-AUTH(app)  ▷ no-op unless MCP_PROTO_OKN_API_KEY is set
14      SERVE(app, host, port)
```

The docstring of each tool function *is* the specification the model sees; the
MCP layer converts signatures and docstrings into the tool schema advertised to
the client. Tool descriptions are therefore part of the method, not commentary.

```
LOAD-REGISTRY(path)
 1  path ← path or FIRST-EXISTING(package_dir/registry.json,
 2                                 project_root/config/registry.json,
 3                                 cwd/config/registry.json)
 4  entries ← PARSE-JSON(READ(path))
 5  graphs ← ∅ ;  aliases ← ∅
 6  for each entry in entries
 7      g ← GraphInfo(name, display_name, named_graph_uri, endpoint_url,
 8                    domain_tags, description_summary, entity_types,
 9                    identifier_namespaces, example_queries, aliases)
10      graphs[g.name] ← g
11      for each a in g.aliases:  aliases[a] ← g.name
12  return ⟨graphs, aliases⟩
```

Each registry entry describes one knowledge graph. `config/registry.json` is the
source of truth for how many graphs are served and what they contain; it is a
build artifact regenerated from `metadata/` by `scripts/build_registry.py`.

```
GET-SERVER(graph_name)                     ▷ lazy construction, cached per process
 1  canonical ← RESOLVE-NAME(graph_name)    ▷ follows aliases
 2  if canonical = NIL
 3      raise ValueError("Unknown graph: …", list of available names)
 4  if canonical ∉ servers
 5      servers[canonical] ← NEW SPARQLServer(endpoint_url = registry[canonical].endpoint_url)
 6  return servers[canonical]
```

A `SPARQLServer` derives its knowledge-graph name from the endpoint URL path and
then points its client at the *federation* endpoint rather than the per-graph
one, so a single connection can address any graph. The per-graph URL survives
only as the source of the name used for dataset scoping (§6.3) and metadata
lookup.

---

## 3. The interaction loop

The control loop lives in the client model, not in the server. The server is
stateless between calls apart from its caches. A typical cross-graph session:

```
ANSWER-QUESTION(question)                  ▷ executed by the LLM client
 1  candidates ← route_query(question)              ▷ §4, ranked, never filtered
 2  G ← model's selection from candidates           ▷ judgment, not a threshold
 3  for each g in G
 4      schema[g] ← get_schema(g)                   ▷ §5, required before writing SPARQL
 5  if question names an ontology term by label
 6      uris ← lookup_uri(label)                    ▷ §8
 7  for each g in G
 8      sparql[g] ← model writes SPARQL from schema[g]
 9  results ← multi_graph_query(sparql)             ▷ §9
10  if |G| > 1
11      strategy ← get_join_strategy(G[i], G[j])    ▷ §7
12      model joins results on the identifier the strategy names
13  return model's synthesis of results
```

Steps 2, 8 and 12 are the model's; every other step is a deterministic server
procedure specified below.

---

## 4. Discovery: ranking graphs against a question

`route_query` is a **lexical prefilter, not a semantic router**. It is a
weighted bag-of-words overlap between the question's whitespace tokens and
registry metadata. There is no embedding model, no stemming, no stopword
removal, no synonym expansion, and no training.

```
SEARCH(question)
 1  terms ← SPLIT(LOWERCASE(question), whitespace)
 2  scored ← ∅
 3  for each graph g in registry
 4      s ← 0
 5      for each t in terms                                   ▷ once per term
 6          if t ⊆ LOWERCASE(g.description_summary):  s ← s + 1
 7          if t ⊆ LOWERCASE(g.name):                 s ← s + 1
 8      for each tag in g.domain_tags,        each t in terms:  ▷ per (item, term) pair
 9          if t ⊆ LOWERCASE(tag):                    s ← s + 2
10      for each c in g.entity_types.classes, each t in terms:
11          if t ⊆ LOWERCASE(c):                      s ← s + 2
12      for each p in g.entity_types.predicates, each t in terms:
13          if t ⊆ LOWERCASE(p):                      s ← s + 1
14      for each e in g.example_queries,      each t in terms:
15          if t ⊆ LOWERCASE(e):                      s ← s + 1
16      for each n in g.identifier_namespaces, each t in terms:
17          if t ⊆ LOWERCASE(n):                      s ← s + 1
18      APPEND(scored, ⟨s, g⟩)
19  SORT scored by (−s, g.name)                               ▷ score desc, name asc for stability
20  return every graph, each annotated with relevance_score
```

`⊆` is substring containment, so `"gene"` matches `"genelab"` and `"genetic"`.
Weights are hand-set: 2 for the two fields that name what a graph *is about*
(domain tags, entity classes), 1 for everything else.

Two consequences are properties of the method rather than defects to be worked
around:

- **Vocabulary mismatch scores zero.** A question asking about "cancer" against
  a registry that says "neoplasm" receives no credit for that term. A score of 0
  means *no literal token overlap*, not *not relevant*.
- **Nothing is filtered out.** All graphs are returned, ranked. The score orders
  the model's inspection; the model performs the actual selection, using the
  returned metadata and, where needed, `get_description` and `get_schema`. Were
  the server to truncate to a top-*k*, the vocabulary-mismatch failure would
  become unrecoverable rather than merely unhelpful.

`list_graphs(domain?, entity_type?)` is the non-ranked alternative: an exact,
case-insensitive filter on `domain_tags` or on `entity_types.classes`.

---

## 5. Grounding: schema retrieval

Schemas come from a curated CSV inventory in this repository when one exists,
and from live SPARQL introspection otherwise. The curated path is preferred
because it carries labels, descriptions, source/target classes, and — critically
— which predicates carry **edge properties**, none of which can be recovered by
enumerating triples.

```
QUERY-SCHEMA(compact)
 1  if kg_name = "ubergraph":  return ∅   ▷ >200K distinct triples; not enumerable
 2  meta ← FETCH-ENTITY-METADATA()        ▷ metadata/entities/<kg>_entities.csv over HTTPS
 3  if meta ≠ ∅
 4      classes, predicates, node_props ← ∅ ;  edge_props ← ∅
 5      for each ⟨uri, m⟩ in meta
 6          case m.type of
 7              "class":        APPEND(classes,    ⟨uri, m.label, m.description⟩)
 8              "predicate":    APPEND(predicates, ⟨uri, SHORT-NAME(uri), m.label,
 9                                                   m.source_class, m.target_class⟩)
10              "nodeproperty": APPEND(node_props, ⟨uri, m.label, m.source_class⟩)
11              "edgeproperty":
12                  for each rel in SPLIT(m.edge_property_of, ";")   ▷ one property, many parents
13                      APPEND(edge_props[rel], ⟨uri, m.label, m.description⟩)
14      for each p in predicates
15          p.has_edge_properties ← (p.short_name ∈ edge_props)
16      for each ⟨rel, props⟩ in edge_props
17          edge_props[rel].query_template ← GENERATE-REIFICATION-TEMPLATE(rel, props)
18      ▷ side effects that arm the query analyzer for this graph
19      self.edge_predicates_with_props ← { uris and labels in edge_props }
20      self.schema_fetched ← TRUE
21      return {classes, predicates, edge_properties: edge_props, node_properties}
22  ▷ fallback: introspect the live graph
23  classes    ← EXECUTE(SELECT DISTINCT ?class WHERE {
24                          {?s a ?class} UNION {?s rdf:type ?class}
25                          UNION {?class a rdfs:Class} UNION {?class a owl:Class} })
26  predicates ← EXECUTE(SELECT DISTINCT ?predicate WHERE { ?s ?predicate ?o })
27  discard any URI in the rdf: syntax namespace   ▷ drops rdf:_1, rdf:_2, … container props
28  return {classes, predicates, edge_properties: ∅, node_properties: ∅}
```

**Edge properties and reification.** Several Proto-OKN graphs attach data to
*relationships* rather than to nodes — a differential-expression edge carries
`log2fc` and `adj_p_value`, for instance. In RDF these are reified statements,
and a query written as a plain triple pattern will silently miss the properties.
`QUERY-SCHEMA` records which predicates are affected (line 19), which lets
`ANALYZE-QUERY` (§6.4) warn when a query mentions such a predicate without a
reification pattern, and lets `get_query_template` emit the correct shape:

```
GENERATE-REIFICATION-TEMPLATE(rel, source_class, target_class, props)
    return SPARQL of the form
        ?stmt rdf:subject   ?source ;
              rdf:predicate schema:<rel> ;
              rdf:object    ?target ;
              schema:<prop> ?value .        for each prop in props
```

---

## 6. Execution: the `query` pipeline

This is the core procedure. A SPARQL string written by the model enters; a
result set, plus any warnings the server can justify, leaves.

```
EXECUTE(q, analyze, auto_expand_descendants, max_descendants, bind_expansion_to)

    ▷ ── Stage 1: federation boundary (§6.1) ─────────────────────────────
 1  outside ← EXTERNAL-SERVICE-TARGETS(q)
 2  if outside ≠ ∅
 3      return {error: "SERVICE may only address the OKN federation …",
 4              refused_service_endpoints: outside}          ▷ nothing is executed

    ▷ ── Stage 2: ontology expansion (§6.2) ──────────────────────────────
 5  queries ← [q] ;  batched ← FALSE ;  expansion ← NIL
 6  if auto_expand_descendants
 7      uris ← DETECT-ONTOLOGY-URIS(q)
 8      if uris ≠ ∅
 9          ⟨rewritten, uri_to_desc⟩ ← EXPAND-WITH-DESCENDANTS(q, uris,
10                                          max_descendants, bind_expansion_to)
11          if rewritten is a list:  queries ← rewritten ; batched ← TRUE
12          else:                    queries ← [rewritten]
13          expansion ← {expanded: TRUE, original_uris: uris,
14                       expanded_uris: {u ↦ |uri_to_desc[u]|},
15                       total_concepts: Σ|uri_to_desc[u]|,
16                       batched, num_batches: |queries|}

    ▷ ── Stage 3: static repair and analysis (§6.4) ──────────────────────
17  warnings ← ∅
18  for each qi in queries
19      ⟨qi, removed⟩ ← REMOVE-EMPTY-FILTERS(qi)   ▷ FILTER(?x IN ()) matches nothing
20      accumulate removed into warnings
21  if analyze and not self.schema_fetched
22      APPEND(warnings, "call get_schema() before querying")
23  analysis ← ANALYZE-QUERY(queries[0])  if analyze

    ▷ ── Stage 4: scope and execute (§6.3) ───────────────────────────────
24  results ← ∅ ;  errors ← ∅
25  for each qi, i in queries
26      if kg_name ≠ ""
27          qi ← INSERT-DATASET-CLAUSE(qi, kg_name)
28      try
29          APPEND(results, COMPACT(SPARQL-GET(qi)))
30      catch e
31          if batched:  APPEND(errors, ⟨i, e, qi⟩) ; continue   ▷ keep partial results
32          else:        return {error: e, query: qi}

    ▷ ── Stage 5: assemble (§6.5) ────────────────────────────────────────
33  if batched and results = ∅:  return {error: errors[0]}
34  out ← MERGE-BATCHES(results)  if batched  else  results[0]
35  attach to out, when present:  query_analysis, schema_warnings,
36                                ontology_expansion, batch_errors
37  return out
```

The order is deliberate. The boundary check precedes all work, because a refused
query should cost nothing. Expansion precedes scoping because expansion rewrites
the query text and may split it into several queries, each of which then needs
its own dataset clause. Analysis runs on the post-expansion, post-cleaning
query, so its warnings describe what will actually execute.

### 6.1 Federation boundary on `SERVICE`

```
EXTERNAL-SERVICE-TARGETS(q)
 1  targets ← ∅
 2  for each match of  SERVICE [SILENT] (<iri> | ?var)  in q
 3      if the match is a variable
 4          APPEND(targets, var)      ▷ cannot be checked statically; reported, not trusted
 5      else if HOSTNAME(iri) ∉ {"apps.okn.us"}
 6          APPEND(targets, iri)
 7  return targets
```

A `SERVICE` clause pointing outside the federation produces a result the
federation cannot reproduce and that is not attributable to the graphs the
server serves; the external host may also drift, throttle, or disappear
independently. The failure is not hypothetical — the same ontology closure
returns 1,628 descendants from a public Ubergraph endpoint and 1,592 from the
federation's own `ubergraph` copy. Since the ontology hub is reachable
in-federation as `GRAPH <https://purl.org/okn/frink/kg/ubergraph>`, refusing
external `SERVICE` costs no capability.

A variable endpoint is reported alongside external ones: it cannot be verified
statically, and a rule that silently admits what it cannot check is not a rule.

### 6.2 Ontology expansion

Expansion is what makes a query for a disease match its subtypes without the
model enumerating them. It is done by **pre-fetching the closure from
`ubergraph` and injecting it as a `VALUES` clause**, rather than by embedding a
property path in the user's query — the closure lives in a different named graph
than the data, so a single path expression would not cross the boundary.

```
DETECT-ONTOLOGY-URIS(q)
 1  return the set of URIs in angle brackets in q matching any of
 2      http://purl.obolibrary.org/obo/{PREFIX}_{DIGITS}      ▷ MONDO, GO, UBERON, CL, HP, CHEBI, PR, SO, …
 3      http://purl.obolibrary.org/obo/{ontology}#{property}  ▷ hash-form annotation properties
 4      http://birdgenenames.org/cgnc/GeneReport?id={DIGITS}
 5      http://www.w3.org/2002/07/owl#{Name}
```

```
FETCH-DESCENDANTS(uri, max_results)
 1  r ← SPARQL-GET("
 2        SELECT DISTINCT ?descendant
 3        FROM <https://purl.org/okn/frink/kg/ubergraph>
 4        WHERE { ?descendant rdfs:subClassOf* <uri> }
 5        LIMIT max_results ")
 6  if r failed:  return [uri]                 ▷ degrade to the literal term, never to an error
 7  return ([uri] ++ (r ∖ {uri}))[0 … max_results]
```

There is deliberately **no depth bound**. The federation's `ubergraph` ships a
fully materialized closure: every descendant is asserted as a *direct*
`rdfs:subClassOf` of every ancestor, so one hop already returns the entire
subtree and there is no deeper structure to reach. See §12 for the measurements
that establish this and for why an earlier depth-bounded formulation was
strictly worse.

Note on how this reads in a rewritten query. Expansion never edits a `FILTER`
in place; it replaces the *literal URI* with a variable and binds that variable
with `VALUES`. When the URI happened to sit inside a filter, the visible effect
is nonetheless that the filter now accepts the whole subtree:

```
before   FILTER(?conditionUri = <MONDO_0004995>)
after    VALUES ?expanded_uri_0004995 { <MONDO_0004995> <MONDO_0005267> … }
         FILTER(?conditionUri = ?expanded_uri_0004995)
```

Describing the mechanism as *rewriting the filter* is therefore right about the
outcome and wrong about the operation — and the distinction matters, because the
same substitution applies to a URI in a plain triple pattern, where no filter is
involved at all.

```
EXPAND-WITH-DESCENDANTS(q, uris, max_descendants, bind_vars)
 1  bind_vars ← each name normalized to start with "?"
 2  desc ← ∅ ;  var_desc ← ∅
 3  for each u in uris
 4      desc[u] ← FETCH-DESCENDANTS(u, max_descendants)
 5      if |desc[u]| ≤ 1:  continue                ▷ leaf term: nothing to expand
 6      var_desc[VAR-NAME(u)] ← desc[u]            ▷ VAR-NAME("…MONDO_0005178") = "?expanded_uri_0005178"
 7  total ← Σ |var_desc[v]|
 8
 9  if total ≤ MAX_VALUES_PER_BATCH                ▷ = 20
10      out ← q ;  clauses ← ∅
11      for each u with |desc[u]| > 1
12          target ← bind_vars[0]  if bind_vars ≠ ∅  else VAR-NAME(u)
13          out ← REPLACE(out, "<u>", target)      ▷ literal URI becomes a variable
14          APPEND(clauses, "VALUES target { <d> for each d in desc[u] }")
15      out ← INSERT clauses immediately after the first "WHERE {"
16      return ⟨out, desc⟩
17
18  ▷ too many URIs for one VALUES clause: split into a Cartesian product of batches
19  per_var ← MAX(1, MAX_VALUES_PER_BATCH / |var_desc|)
20  chunks[v] ← PARTITION(var_desc[v], per_var)    for each v
21  batch_queries ← ∅
22  for each combo in CARTESIAN-PRODUCT(indices of chunks[v] over all v)
23      bq ← q
24      for each u with |desc[u]| > 1:  bq ← REPLACE(bq, "<u>", target as line 12)
25      clauses ← one "VALUES target { … }" per v, using chunks[v][combo[v]]
26      DEDUPE clauses that target the same variable
27      bq ← INSERT clauses after the first "WHERE {"
28      APPEND(batch_queries, bq)
29  return ⟨batch_queries, desc⟩
```

Batching exists because a `VALUES` block with hundreds of URIs is rejected or
times out at the endpoint. Splitting the budget per variable guarantees that no
single emitted query exceeds `MAX_VALUES_PER_BATCH` URIs in total. Batches are
executed independently and merged; a batch that fails is recorded rather than
discarding the batches that succeeded (§6.5).

**The `bind_expansion_to` parameter.** By default each expanded URI becomes its
own fresh variable, which *filters* the result to the subtree. Passing
`bind_expansion_to=["disease"]` instead routes the expansion onto a variable the
model already selects and groups by, which *aggregates per descendant*. The
distinction is not cosmetic:

```
▷ without bind_expansion_to — ?disease is unconstrained
SELECT ?disease (COUNT(?dataset) AS ?n) WHERE {
  ?dataset schema:healthCondition <MONDO_0005578> .   ▷ expanded
  ?dataset schema:healthCondition ?disease .          ▷ matches ANY co-occurring disease
} GROUP BY ?disease
   → counts every disease appearing on an arthritis dataset, including unrelated ones

▷ with bind_expansion_to=["disease"] — the URI and the variable are unified
SELECT ?disease (COUNT(?dataset) AS ?n) WHERE {
  VALUES ?disease { <MONDO_0005578> <MONDO_0008383> … }
  ?dataset schema:healthCondition ?disease .
} GROUP BY ?disease
   → counts each arthritis subtype independently
```

Unifying on the model's own variable, rather than intersecting two separately
bound variables, is what avoids both undercounting (an intersection requires
co-occurrence) and substring corruption of names like `?diseaseLabel`.

### 6.3 Dataset-clause injection

```
INSERT-DATASET-CLAUSE(q, kg_name)
 1  if q already contains  FROM <…>  or  FROM NAMED <…>
 2      return q                     ▷ the caller is scoping deliberately; do not second-guess
 3  if q contains  GRAPH ?var
 4      return q                     ▷ named graphs cannot be enumerated statically
 5  lines ← [ "FROM <https://purl.org/okn/frink/kg/{kg_name}>" ]
 6  for each distinct iri in occurrences of  GRAPH <iri>  in q
 7      APPEND(lines, "FROM NAMED <{iri}>")
 8  return q with the first "WHERE {" replaced by  lines ++ "WHERE {"
```

Line 5 is the convenience: the model writes `?s ?p ?o` and means "in this graph".

Lines 6–7 are a **correctness requirement**, not decoration. In SPARQL, `FROM`
builds the default graph and `FROM NAMED` determines which named graphs the
dataset contains. A query carrying only `FROM` has *no* named graphs, so every
`GRAPH <other>` block matches the empty graph and contributes nothing — with no
error and no warning, just zero rows. Measured against the federation on a
cardiovascular-disease closure:

| Dataset clause | Rows |
|---|---|
| none | 1592 |
| `FROM <…/nde>` alone | **0** |
| `FROM <…/nde>` + `FROM NAMED <…/ubergraph>` | 1592 |

Without lines 6–7, every cross-graph query written the ordinary way — default
graph for one graph, `GRAPH` blocks for the others — silently returns nothing,
while the identical query text answers correctly when sent to the endpoint
directly.

The two exemptions are equally deliberate. A self-scoping query is left alone. A
query using `GRAPH ?g` cannot have its graphs enumerated before execution, and
the endpoint's default dataset already exposes every graph as named, which is
what such a query needs.

### 6.4 Static analysis

```
ANALYZE-QUERY(q)
 1  limit ← the integer in "LIMIT n", if any
 2  ordered ← q contains "ORDER BY"
 3  if limit ≠ NIL and not ordered
 4      warn: "LIMIT n without ORDER BY returns arbitrary rows, not the top n"
 5      suggest ORDER BY DESC over the first SELECT variable whose name reads as
        numeric (count, value, score, p_value, log2fc, …), else the second one
 6  if q mentions a predicate in self.edge_predicates_with_props   ▷ armed by §5, line 19
 7     and q does not contain an rdf:subject / rdf:predicate / rdf:object pattern
 8      warn: "this relationship stores data on the edge; use RDF reification" + template
 9  return the warnings
```

```
REMOVE-EMPTY-FILTERS(q)
 1  strip every  FILTER( [LCASE(] [STR(] ?var [)] [)] IN () )
 2  return the cleaned query and the list of what was removed
```

An empty `IN ()` list arises when the model interpolates a lookup that returned
nothing. Left in place it matches zero rows and produces an empty result that
looks like a substantive finding. Removed, the query returns the unconstrained
result and the response carries a warning naming each clause dropped.

Analysis never blocks execution. Only the federation-boundary check (§6.1) does.

### 6.5 Result assembly

```
COMPACT(sparql_json)
 1  return {columns: sparql_json.head.vars,
 2          data:    one array per binding, values in column order, "" for unbound,
 3          count:   number of rows}
```

A columnar shape rather than a list of objects: it removes one repetition of
every key per row, which materially reduces the token cost of returning a large
result to a language model.

```
MERGE-BATCHES(results)
 1  concatenate the data arrays under a single column header
 2  count ← total rows
 3  carry any per-batch errors through as a non-fatal batch_errors field
```

---

## 7. Cross-graph bridging: identifier mapping and join strategy

The Proto-OKN graphs are independently constructed and do not share primary
keys. The same gene is an Ensembl ID in one graph, an NCBI Entrez ID in another,
and a bare symbol in a third. Joining results therefore requires knowing *which
identifier namespace* two graphs have in common and *where in each graph* it is
stored. That knowledge is curated, not inferred.

### 7.1 The bridge table

`IDENTIFIER_BRIDGES` is a static three-level map:

```
IDENTIFIER_BRIDGES : identifier_type → graph_name → {
        description : prose describing how the graph carries the identifier
        property?   : the predicate URI holding it, when it is a node property
        uri_pattern?: the URI shape encoding it, when it is part of the node URI
    }
```

It covers 13 identifier types across six categories:

| Category | Identifier types |
|---|---|
| Genes | `NCBI_Gene`, `Ensembl`, `GeneSymbol` |
| Chemicals | `CAS`, `DTXSID`, `InChIKey` |
| Diseases | `MONDO` |
| Locations | `FIPS`, `S2Cell` |
| Biomedical vocabularies | `MeSH`, `ChEBI`, `UBERON` |
| Industry | `NAICS` |

The distinction between `property` and `uri_pattern` is what makes the table
actionable: a join on a node property is a triple pattern, whereas a join on a
URI-encoded identifier is a string operation on the URI. Recording which applies
per graph is precisely the information a model cannot recover from a schema
listing alone.

### 7.2 Finding a shared key

```
FIND-COMMON-IDENTIFIERS(a, b)
 1  return [ t : t ∈ IDENTIFIER_BRIDGES, a ∈ IDENTIFIER_BRIDGES[t], b ∈ IDENTIFIER_BRIDGES[t] ]
```

### 7.3 Suggesting a join strategy

```
SUGGEST-JOIN-STRATEGY(a, b)
 1  common ← FIND-COMMON-IDENTIFIERS(a, b)
 2
 3  if common ≠ ∅                                   ▷ direct join
 4      strategies ← ∅
 5      for each t in common
 6          APPEND(strategies, "Join on t: a (how a carries t) ↔ b (how b carries t)")
 7      return {can_join: TRUE, common_identifiers: common,
 8              strategy: JOIN(strategies, "; ")}
 9
10  ▷ no shared namespace — try the gene bridge
11  gene_types ← ["NCBI_Gene", "Ensembl", "GeneSymbol"]
12  a_ids ← [t ∈ gene_types : a ∈ IDENTIFIER_BRIDGES[t]]
13  b_ids ← [t ∈ gene_types : b ∈ IDENTIFIER_BRIDGES[t]]
14  if a ≠ b and a_ids ≠ ∅ and b_ids ≠ ∅ and a_ids ∩ b_ids = ∅
15      ▷ both are gene graphs, in mutually unintelligible namespaces
16      return {can_join: TRUE, common_identifiers: ∅,
17              bridge_graph: "gene-expression-atlas-okn",
18              source_id_types: a_ids, target_id_types: b_ids,
19              strategy: "no direct shared identifier; bridge through a graph
20                         that stores both namespaces for the same gene"}
21
22  return {can_join: FALSE, common_identifiers: ∅,
23          strategy: "No shared identifier namespaces found between a and b."}
```

The condition at line 14 is the whole idea of the fallback. If `a_ids ∩ b_ids`
were non-empty the graphs would share a namespace and line 3 would already have
returned. If either side has no gene identifier at all, no gene bridge exists.
The remaining case — both are gene graphs, in disjoint namespaces — is exactly
the case a third graph can repair.

### 7.4 The gene bridge

`gene-expression-atlas-okn` records `ncbi_gene_id`, `ensembl_id`, and `symbol`
on the same `Gene` node. It is therefore a translation table between any two
gene namespaces, and a two-graph join becomes a three-graph path:

```
    graph A ──(NCBI Gene ID)──▶ gene-expression-atlas-okn ──(Ensembl ID)──▶ graph B
```

```
BUILD-GENE-BRIDGE-QUERY(source_graph, target_graph, gene_ids)
 1  if gene_ids = ∅:  return NIL
 2  source_type ← first gene identifier type source_graph carries
 3  target_type ← first gene identifier type target_graph carries
 4  if either is undefined:  return NIL
 5  ⟨src_prop, src_var⟩ ← PROPERTY-MAP[source_type]   ▷ NCBI_Gene ↦ glab:ncbi_gene_id
 6  ⟨tgt_prop, tgt_var⟩ ← PROPERTY-MAP[target_type]   ▷ Ensembl   ↦ glab:ensembl_id
 7                                                    ▷ GeneSymbol↦ biolink:symbol
 8  return SPARQL:
 9        SELECT ?gene src_var tgt_var ?name WHERE {
10          VALUES src_var { the gene_ids }
11          ?gene a biolink:Gene .
12          ?gene src_prop src_var .
13          ?gene tgt_prop tgt_var .
14          OPTIONAL { ?gene biolink:name ?name }
15        }
```

A companion procedure, `BUILD-GENE-LOOKUP-QUERY(graph, gene)`, emits a
schema-appropriate lookup for each gene-bearing graph — matching on
`spoke:ensembl` in one, on `sglab:symbol` in another, on any of three properties
in the bridge graph — because a single generic query would match none of them.

---

## 8. Ontology services

These two tools are graph-independent: both address the federation's `ubergraph`
named graph rather than any Proto-OKN graph.

```
LOOKUP-URI(label, max_results)
 1  variants ← DEDUPE([label, lower(label), upper(label), title(label), capitalize(label)])
 2  r ← SPARQL-GET("
 3        SELECT DISTINCT ?uri ?matchedLabel ?matchType
 4        FROM <https://purl.org/okn/frink/kg/ubergraph>
 5        WHERE {
 6          { ?uri rdfs:label ?matchedLabel .
 7            VALUES ?matchedLabel { variants }  BIND('exact_label' AS ?matchType) }
 8          UNION
 9          { ?uri oboInOwl:hasExactSynonym ?matchedLabel .
10            VALUES ?matchedLabel { variants }  BIND('exact_synonym' AS ?matchType) }
11        } LIMIT max_results ")
12  return {query_label: label, match_count: |r|, matches: r}
```

Case-insensitivity is obtained by enumerating casings **on the query side**, not
by applying `LCASE` to the stored label. The distinction is the difference
between an indexed lookup and a full scan: a function on the stored side cannot
be served by any index, so the endpoint scans every label in `ubergraph`, twice
(once per `UNION` branch), and `max_results` does not help because `LIMIT`
applies after the scan — asking for 10 matches costs exactly what asking for
2000 costs. Measured: ~16s and frequent HTTP 429, versus ~0.3s for the `VALUES`
form.

The trade is explicit: matching is case-insensitive for every realistic spelling
of an OBO label rather than for literally every one. A deliberately mixed-case
string such as `"mUsClE oRgAn"` will not match.

```
GET-DESCENDANTS(uri, max_results, include_distance)
 1  label ← SPARQL-GET("SELECT ?label FROM <ubergraph> WHERE { <uri> rdfs:label ?label }")
 2  total ← SPARQL-GET("SELECT (COUNT(DISTINCT ?d) AS ?n) FROM <ubergraph>
 3                      WHERE { ?d rdfs:subClassOf* <uri> . FILTER(?d != <uri>) }")
 4  rows  ← SPARQL-GET("SELECT DISTINCT ?d ?label [ (1 AS ?min_distance) ] FROM <ubergraph>
 5                      WHERE { ?d rdfs:subClassOf<*> <uri> . FILTER(?d != <uri>)
 6                              OPTIONAL { ?d rdfs:label ?label } }
 7                      ORDER BY ?d LIMIT max_results ")
 8  return {uri, label, descendants: rows,
 9          descendant_count: |rows|,
10          total_count: total,
11          truncated: (total ≠ NIL and |rows| < total)}
```

`total_count` and `truncated` are computed independently of `max_results` so a
truncated list cannot be mistaken for a complete one — a caller asking for 100
of 1,591 descendants would otherwise receive `descendant_count: 100` with no
indication that anything was cut.

`include_distance` is retained but reports a **constant 1**. A materialized
closure preserves no hop counts; it cannot distinguish a child from a
great-grandchild. Reporting a constant is what the data can honestly support.

---

## 9. Multi-graph execution

```
MULTI-GRAPH-QUERY(queries)                  ▷ queries : graph_name → SPARQL string
 1  rows ← ∅ ;  columns ← NIL ;  per_graph ← ∅ ;  errors ← ∅
 2  for each ⟨g, q⟩ in queries
 3      try
 4          r ← GET-SERVER(g).EXECUTE(q)    ▷ full pipeline of §6, per graph
 5          if columns = NIL:  columns ← ["source_graph"] ++ r.columns
 6          for each row in r.data:  APPEND(rows, [g] ++ row)
 7          per_graph[g] ← {count: r.count, status: "success"}
 8      catch e
 9          errors[g] ← e
10          per_graph[g] ← {count: 0, status: "error", error: e}
11  return {columns, data: rows, count: |rows|, per_graph, errors}
```

Each graph receives its *own* SPARQL, written against its own schema — the
graphs share no schema, so a single query text cannot serve two of them. Results
are stacked under a prepended `source_graph` column rather than joined; the
join is performed by the model, on the key that `get_join_strategy` identifies.

A failure in one graph does not abort the others. `per_graph` reports the
outcome for every graph requested, so a partial result is always distinguishable
from a complete one.

---

## 10. Reporting and visualization tools

Three tools produce no data of their own. They return *instructions* — text the
model is expected to act on — which makes them part of the method rather than
conveniences: the reproducibility of a session's diagrams and transcripts rests
on these strings, not on server-side rendering.

```
VISUALIZE-SCHEMA(graph_name)
 1  validate graph_name, resolving aliases
 2  return a procedure for the model to follow:
 3      call get_schema(graph_name)
 4      classify each entity as node class, plain edge, or edge-with-properties
 5      render plain edges as labelled arrows;
 6             edges with properties as an intermediary class holding them
 7      pass the draft through CLEAN-MERMAID-DIAGRAM        ▷ mandatory
 8      present only the cleaned output, and save it as .mermaid
```

```
CLEAN-MERMAID-DIAGRAM(text)                ▷ the only one that transforms input
 1  truncate any token at an embedded "\n"
 2  drop every `note` statement            ▷ renders as an unreadable overlay
 3  replace "|" with " "                   ▷ invalid in a Mermaid class diagram
 4  collapse empty `class X { }` to `class X`, single- and multi-line forms
 5  return the cleaned text
```

```
CREATE-CHAT-TRANSCRIPT(graph_name?)
 1  return a Markdown skeleton — prompts, responses and diagrams inline —
 2         stamped with the package version and the current date
```

`VISUALIZE-SCHEMA` is prescriptive about calling `CLEAN-MERMAID-DIAGRAM` because
a model that skips it emits diagrams that fail to render. The cleaning step is
the only deterministic transformation of the three; the other two are templates.

---

## 11. Worked trace

A question spanning a biomedical graph and a chemical-assay graph:

```
  "Which environmental chemicals interact with genes implicated in arthritis?"

  route_query(question)
      → all graphs ranked; "gene" hits entity classes in several,
        "chemical" hits domain tags in the biobricks family
  get_schema("spoke-okn")            → classes incl. Gene, Disease; property spoke:ensembl
  get_schema("biobricks-ice")        → assay predicates; ice:assay_entrez_gene_id
  lookup_uri("arthritis")            → http://purl.obolibrary.org/obo/MONDO_0005578
  query("spoke-okn", …<MONDO_0005578>…)
      §6.1  no SERVICE clause                            → proceed
      §6.2  detects MONDO_0005578
            FETCH-DESCENDANTS → parent + subtypes
            |URIs| > 20 → Cartesian batching into k queries
      §6.3  each batch gains FROM <…/kg/spoke-okn>
      §6.4  LIMIT-without-ORDER-BY check; edge-property check
            executes k batches, merges, reports total_concepts
      → genes associated with arthritis and its subtypes, as Ensembl IDs
  get_join_strategy("spoke-okn", "biobricks-ice")
      common ← ∅                                 (Ensembl vs NCBI_Gene)
      gene fallback: a_ids = [Ensembl], b_ids = [NCBI_Gene], disjoint
      → can_join, bridge_graph = "gene-expression-atlas-okn"
  query("gene-expression-atlas-okn", BUILD-GENE-BRIDGE-QUERY(…, ensembl_ids))
      → Ensembl → NCBI Gene ID translation table
  query("biobricks-ice", … ice:assay_entrez_gene_id VALUES {ncbi_ids} …)
      → assays, and the chemicals tested in them
  model joins on the translated identifiers and answers
```

Every step above is either a deterministic server procedure or an explicit model
decision, and the boundary between the two is the boundary drawn in §1.

---

## 12. Cost and correctness notes

Behaviour of the federation that the procedures above are shaped around.
Measurements were taken against `apps.okn.us` on `MONDO_0004995`
(cardiovascular disorder), which has 1,591 descendants.

**The ontology closure is materialized.** Every descendant is asserted as a
direct `rdfs:subClassOf` of every ancestor:

| Query form | Descendants |
|---|---|
| `?d rdfs:subClassOf <uri>` (one hop, no path operator) | 1592 |
| `?d rdfs:subClassOf* <uri>` | 1592 |
| exactly two hops but not one | 0 |

One hop is therefore the entire subtree, and hop counts do not survive in the
data. This is why `FETCH-DESCENDANTS` and `GET-DESCENDANTS` take no depth
parameter, and why `include_distance` can only report a constant.

**Depth bounds were strictly harmful.** An earlier formulation avoided
`rdfs:subClassOf*` on the theory that an unbounded path operator would time out
on large ontologies, and built a `UNION` of explicit join chains instead — one
branch per depth, each up to `max_depth` joins long. This defeats the
precomputed transitive index that the path operator exists to use:

| Form | Time |
|---|---|
| `rdfs:subClassOf*` | 0.4–0.5s |
| `UNION`, depth 5 | 0.7–0.9s |
| `UNION`, depth 10 | times out (~45s) |
| `UNION`, depth 15 | times out |

Every branch past the first recomputed rows the first had already found, at
exponential cost, so the workaround caused the failure it was written to
prevent — and raising the bound in pursuit of completeness triggered it every
time.

**`VALUES` size is bounded at 20 URIs per query** (`MAX_VALUES_PER_BATCH`).
Larger blocks produce HTTP 403 or timeouts, which is why §6.2 batches.

**Function-on-stored-value defeats indexing.** `FILTER(LCASE(?label) = …)`
forces a full label scan; `VALUES ?label { … }` is an indexed lookup. ~16s and
frequent HTTP 429, versus ~0.3s (§8).

**`FROM` without `FROM NAMED` silently empties `GRAPH` blocks** — 0 rows
instead of 1592, with no error raised (§6.3).

The recurring pattern in all five is worth stating plainly, since it shaped the
design: against this endpoint, the failure mode to guard against is not the
loud one. It is the query that returns a plausible, wrong, smaller number.

---

## 13. Pseudocode → source map

| Procedure | Implementation |
|---|---|
| `MAIN`, tool registration, transports | `main()` — `src/mcp_proto_okn/unified_server.py:136` |
| `LOAD-REGISTRY` | `GraphRegistry.__init__` — `src/mcp_proto_okn/registry.py:44` |
| `GET-SERVER` | `UnifiedSPARQLServer._get_server` — `src/mcp_proto_okn/unified_server.py:47` |
| `SEARCH` (§4) | `GraphRegistry.search` — `src/mcp_proto_okn/registry.py:119` |
| `QUERY-SCHEMA` (§5) | `SPARQLServer.query_schema` — `src/mcp_proto_okn/server.py:1122` |
| `GENERATE-REIFICATION-TEMPLATE` | `SPARQLServer._generate_query_template` — `src/mcp_proto_okn/server.py:1089` |
| `EXECUTE` (§6) | `SPARQLServer.execute` — `src/mcp_proto_okn/server.py:850` |
| `EXTERNAL-SERVICE-TARGETS` (§6.1) | `external_service_targets` — `src/mcp_proto_okn/server.py:70` |
| `DETECT-ONTOLOGY-URIS` (§6.2) | `SPARQLServer._detect_ontology_uris` — `src/mcp_proto_okn/server.py:496` |
| `FETCH-DESCENDANTS` (§6.2) | `SPARQLServer._fetch_descendants_for_uri` — `src/mcp_proto_okn/server.py:541` |
| `EXPAND-WITH-DESCENDANTS` (§6.2) | `SPARQLServer._expand_query_with_descendants` — `src/mcp_proto_okn/server.py:587` |
| `INSERT-DATASET-CLAUSE` (§6.3) | `SPARQLServer._insert_from_clause` — `src/mcp_proto_okn/server.py:321` |
| `ANALYZE-QUERY` (§6.4) | `QueryAnalyzer.analyze_query` — `src/mcp_proto_okn/server.py:237` |
| `REMOVE-EMPTY-FILTERS` (§6.4) | `QueryAnalyzer.remove_empty_filters` — `src/mcp_proto_okn/server.py:218` |
| `COMPACT` (§6.5) | `SPARQLServer._compact_result` — `src/mcp_proto_okn/server.py:390` |
| `MERGE-BATCHES` (§6.5) | `SPARQLServer._merge_batch_results` — `src/mcp_proto_okn/server.py:797` |
| `IDENTIFIER_BRIDGES` (§7.1) | `src/mcp_proto_okn/identifier_mapping.py:13` |
| `FIND-COMMON-IDENTIFIERS` (§7.2) | `find_common_identifiers` — `src/mcp_proto_okn/identifier_mapping.py:174` |
| `SUGGEST-JOIN-STRATEGY` (§7.3) | `suggest_join_strategy` — `src/mcp_proto_okn/identifier_mapping.py:189` |
| `BUILD-GENE-BRIDGE-QUERY` (§7.4) | `build_gene_bridge_query` — `src/mcp_proto_okn/identifier_mapping.py:324` |
| `BUILD-GENE-LOOKUP-QUERY` (§7.4) | `build_gene_lookup_query` — `src/mcp_proto_okn/identifier_mapping.py:248` |
| `LOOKUP-URI` (§8) | `SPARQLServer.lookup_uri` — `src/mcp_proto_okn/server.py:1505` |
| `GET-DESCENDANTS` (§8) | `SPARQLServer.get_descendants_detailed` — `src/mcp_proto_okn/server.py:1592` |
| `MULTI-GRAPH-QUERY` (§9) | `multi_graph_query` tool — `src/mcp_proto_okn/unified_server.py:353` |
| `VISUALIZE-SCHEMA` (§10) | `visualize_schema` tool — `src/mcp_proto_okn/unified_server.py:664` |
| `CLEAN-MERMAID-DIAGRAM` (§10) | `clean_mermaid_diagram` tool — `src/mcp_proto_okn/unified_server.py:537` |
| `CREATE-CHAT-TRANSCRIPT` (§10) | `create_chat_transcript` tool — `src/mcp_proto_okn/unified_server.py:618` |

## Related documents

- **[api.md](api.md)** — tool-by-tool API reference: signatures, parameters, return shapes.
- **[develop.md](develop.md)** — running the server locally, module layout, transports, testing.
- **[adding-a-graph.md](adding-a-graph.md)** — extending the registry with a new knowledge graph.
- **[examples.md](examples.md)** — worked analysis sessions.
