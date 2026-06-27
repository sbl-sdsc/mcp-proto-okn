# Bio-Health KG Chat Transcript

👤 **User**
Give a high-level overview of the @biohealth knowledge graph, including its main entities, relationships, and purpose.

---

🧠 **Assistant**
Here's a high-level overview of the **Bio-Health KG**:

**What it is.** Bio-Health KG is a dynamically-updated open knowledge network for health, developed by the University of Virginia under NSF Proto-OKN Theme 1 funding (Award #2333740). It integrates biomedical facts with Social Determinants of Health (SDoH) data to study healthcare disparities. The graph holds over 110 million triples covering 250,976 biomedical entities connected through 18.3 million biomedical relationships, and continuously refreshes from streams of scientific literature (primarily PubMed) and Electronic Health Records (including MIMIC clinical data).

**Domain.** Biomedicine · health · social determinants of health. Entity nodes are normalized to UMLS concepts (CUIs), with disease and condition concepts also reachable through MeSH and MONDO.

**Core entity types.** The schema is deliberately compact, with two classes:

- `Entity` (`biolink:Entity`) — a biomedical concept normalized to a UMLS CUI: genes and proteins, chemicals and drugs, diseases and signs/symptoms, anatomical structures, biological processes, and social determinants of health. Each entity carries a Biolink `category` (a UMLS semantic type) and a human-readable `label`.
- `Statement` (`rdf:Statement`) — a reified RDF triple (subject–predicate–object) that records one asserted relationship and attaches its provenance.

**Relationships.** Entities are connected directly by 64 relationship predicates drawn from two vocabularies. The Biolink layer provides normalized predicates such as `treats`, `causes`, `affects`, `coexists_with`, `location_of`, `interacts_with`, `predisposes_to_condition`, and `preventative_for_condition`. A custom schema layer (the `biohealthkg` namespace, derived from SemMedDB-style predications) adds predicates like `ADMINISTERED_TO`, `MEASURES`, `OCCURS_IN`, `PRODUCES`, `STIMULATES`, and `USES`, together with a full set of negated `NEG_*` variants (e.g. `NEG_TREATS`, `NEG_CAUSES`, `NEG_AFFECTS`) that capture explicitly negated assertions extracted from text.

**Provenance via reification.** Every relationship is also expressed as an `rdf:Statement` whose `rdf:subject`, `rdf:predicate`, and `rdf:object` mirror the asserted edge, and whose `dc:source` names the evidence it was derived from — for example `PubMed`, `MIMIC`, or `MIMIC;PubMed`. This lets a query trace any assertion back to literature versus clinical-record support.

**What it can answer.** Because it fuses literature-derived biomedical relationships with clinical-record signal and SDoH context, Bio-Health KG is well suited to questions such as: which social determinants are associated with a given disease; what treats, causes, or predisposes to a condition; which assertions are supported by clinical records (MIMIC) versus literature (PubMed); and where negated evidence contradicts a proposed relationship.

**Access.** SPARQL endpoint at `https://apps.okn.us/biohealth/sparql`, with a Linked Data Fragments interface at `https://apps.okn.us/ldf/biohealth`.

---

👤 **User**
Visualize the schema as a class diagram.

---

🧠 **Assistant**
Here's the schema. Entities are the nodes connected directly by the relationship predicates (Biolink + custom `biohealthkg` schema), and each relationship is mirrored by a reified `Statement` that carries its `dc:source` provenance:

```mermaid
classDiagram
direction LR

class Entity {
  string label
  string category
}

class Statement {
  string source
}

Entity --> Entity : treats / causes / affects
Entity --> Entity : coexists_with / location_of
Entity --> Entity : interacts_with / part_of
Entity --> Entity : predisposes_to_condition
Entity --> Entity : preventative_for_condition
Entity --> Entity : ADMINISTERED_TO / MEASURES
Entity --> Entity : OCCURS_IN / PRODUCES / USES
Entity --> Entity : NEG_TREATS / NEG_CAUSES (negated)

Statement --> Entity : rdf:subject
Statement --> Entity : rdf:object
Statement ..> Entity : rdf:predicate (relationship IRI)

note for Statement "Reification of one asserted edge.\ndc:source = PubMed, MIMIC, or both."
note for Entity "UMLS CUI node.\n64 relationship predicates total:\n17 Biolink + 16 custom + 31 NEG_*"
```

**Reading the diagram.** `Entity → Entity` edges are the asserted biomedical relationships (only a representative subset of the 64 predicates is labeled). For every such edge there is a parallel `Statement` whose `rdf:subject`/`rdf:object` point back to the same two entities and whose `dc:source` records whether the assertion came from PubMed literature, MIMIC clinical data, or both — the mechanism Bio-Health KG uses for provenance tracking.
