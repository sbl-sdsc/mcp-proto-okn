# Ontology Expansion Walkthrough — Cardiovascular Disease Datasets

This example shows the unified server's **automatic ontology expansion** in action: a single user question is silently rewritten to cover an entire ontology subtree, returning matches across hundreds of disease subtypes that the user never had to enumerate.

The graph queried is [`nde`](https://frink.renci.org/registry/kgs/nde/) — NIAID's data discovery catalog of biomedical datasets, tagged with MONDO disease URIs.

---

## The User's Prompt

👤 **User**
> For cardiovascular disease, list the diseases studied and the number of datasets covering each. Show the top 20 by dataset count.

---

## What the Server Does Behind the Scenes

The assistant calls `lookup_uri("cardiovascular disease")` and gets back `MONDO:0004995`. It then writes a single-URI SPARQL query against `nde`:

```sparql
PREFIX schema: <http://schema.org/>

SELECT ?conditionName ?conditionUri (COUNT(DISTINCT ?dataset) AS ?datasetCount)
WHERE {
  ?dataset a schema:Dataset ;
           schema:healthCondition ?conditionUri .
  ?conditionUri schema:name ?conditionName .
  FILTER(?conditionUri = <http://purl.obolibrary.org/obo/MONDO_0004995>)
}
GROUP BY ?conditionName ?conditionUri
ORDER BY DESC(?datasetCount)
```

This query, as written, would match only datasets tagged with the exact URI `MONDO_0004995` — i.e. those labeled "cardiovascular disease" at the root level. In practice, that's a small fraction of the datasets that touch the cardiovascular space.

The `query()` tool detects the MONDO URI and transparently fetches its descendants from [Ubergraph](https://frink.renci.org/registry/kgs/ubergraph/), then rewrites the FILTER to also accept any of those descendants. The expansion is reported alongside the results:

```json
"ontology_expansion": {
  "expanded": true,
  "original_uris": ["http://purl.obolibrary.org/obo/MONDO_0004995"],
  "expanded_uris": {"http://purl.obolibrary.org/obo/MONDO_0004995": 1592},
  "total_concepts": 1592,
  "batched": true,
  "num_batches": 80
}
```

One URI in, **1,592 URIs out**. The user wrote nothing about specific cardiovascular subtypes.

---

## Result (Top 20 by Dataset Count)

🧠 **Assistant**

| Disease Name | MONDO ID | Datasets |
|---|---|---|
| Cardiac arrest | MONDO_0000745 | 1,409 |
| Atrial fibrillation | MONDO_0004981 | 1,096 |
| Heart disorder | MONDO_0005267 | 967 |
| Atherosclerosis | MONDO_0005311 | 859 |
| Hypertensive disorder | MONDO_0005044 | 793 |
| Heart failure | MONDO_0005252 | 677 |
| Myocardial infarction | MONDO_0005068 | 525 |
| Stroke disorder | MONDO_0005098 | 520 |
| Cardiovascular disorder (root) | MONDO_0004995 | 447 |
| Cardiomyopathy | MONDO_0004994 | 384 |
| Coronary artery disorder | MONDO_0005010 | 382 |
| Ischemic disease | MONDO_0005053 | 259 |
| Hypotensive disorder | MONDO_0005468 | 219 |
| Dilated cardiomyopathy | MONDO_0005021 | 215 |
| Pulmonary hypertension | MONDO_0005149 | 162 |
| Preeclampsia | MONDO_0005081 | 144 |
| Multifocal atrial tachycardia | MONDO_0017988 | 143 |
| Kaposi's sarcoma | MONDO_0005055 | 123 |
| Brain ischemia | MONDO_0005299 | 108 |
| Situs inversus | MONDO_0010029 | 101 |

**284 distinct cardiovascular conditions** in total were matched across the descendant subtree — from common ones like atherosclerosis and heart failure down to rare Mendelian syndromes (Holt-Oram, Loeys-Dietz, Brugada, etc.) that no flat keyword search would have surfaced.

---

## Why This Matters

Without ontology expansion, a query for "cardiovascular disease" against `nde` returns only the 447 datasets tagged with the exact root MONDO URI. With expansion, it returns **10,000+ dataset–condition pairs** spanning every subtype the data curators chose to tag at — without the user (or the LLM) having to know what those subtypes are called or what URI each one has.

The expansion is bounded (`max_depth=5`, `max_descendants=2000` by default), batched to keep the SPARQL endpoint happy, and reported back to the assistant so it can mention the breadth of the search when summarizing results. It works on any URI from MONDO, UBERON, HP, GO, CL, CHEBI, and the other Ubergraph ontologies, applied automatically to whichever graphs use those identifier systems.

---

*Generated with the unified `mcp-proto-okn` server. Reproduce by asking Claude (or any MCP client) the user prompt above with the `proto-okn` server connected.*
