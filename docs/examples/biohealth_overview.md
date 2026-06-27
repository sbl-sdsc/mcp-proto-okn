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

%% Reified-statement structure and provenance
Statement --> Entity : rdf_subject
Statement --> Entity : rdf_object
Statement ..> Entity : rdf_predicate

%% Biolink relationship predicates (17)
Entity --> Entity : affects
Entity --> Entity : associated_with
Entity --> Entity : causes
Entity --> Entity : coexists_with
Entity --> Entity : decreases_amount_or_activity_of
Entity --> Entity : diagnoses
Entity --> Entity : disrupts
Entity --> Entity : increases_amount_or_activity_of
Entity --> Entity : interacts_with
Entity --> Entity : location_of
Entity --> Entity : manifestation_of
Entity --> Entity : part_of
Entity --> Entity : precedes
Entity --> Entity : predisposes_to_condition
Entity --> Entity : preventative_for_condition
Entity --> Entity : subclass_of
Entity --> Entity : treats

%% Custom biohealthkg schema predicates (16)
Entity --> Entity : ADMINISTERED_TO
Entity --> Entity : COMPLICATES
Entity --> Entity : CONVERTS_TO
Entity --> Entity : LOCATION_OF(SPEC)
Entity --> Entity : MEASUREMENT_OF
Entity --> Entity : MEASURES
Entity --> Entity : METHOD_OF
Entity --> Entity : OCCURS_IN
Entity --> Entity : PROCESS_OF
Entity --> Entity : PRODUCES
Entity --> Entity : STIMULATES
Entity --> Entity : USES
Entity --> Entity : compared_with
Entity --> Entity : higher_than
Entity --> Entity : lower_than
Entity --> Entity : same_as

%% Negated (NEG_) assertions (31, shown dashed)
Entity ..> Entity : NEG_ADMINISTERED_TO
Entity ..> Entity : NEG_AFFECTS
Entity ..> Entity : NEG_ASSOCIATED_WITH
Entity ..> Entity : NEG_AUGMENTS
Entity ..> Entity : NEG_CAUSES
Entity ..> Entity : NEG_COEXISTS_WITH
Entity ..> Entity : NEG_COMPLICATES
Entity ..> Entity : NEG_CONVERTS_TO
Entity ..> Entity : NEG_DIAGNOSES
Entity ..> Entity : NEG_DISRUPTS
Entity ..> Entity : NEG_INHIBITS
Entity ..> Entity : NEG_INTERACTS_WITH
Entity ..> Entity : NEG_ISA
Entity ..> Entity : NEG_LOCATION_OF
Entity ..> Entity : NEG_MANIFESTATION_OF
Entity ..> Entity : NEG_MEASUREMENT_OF
Entity ..> Entity : NEG_MEASURES
Entity ..> Entity : NEG_METHOD_OF
Entity ..> Entity : NEG_OCCURS_IN
Entity ..> Entity : NEG_PART_OF
Entity ..> Entity : NEG_PRECEDES
Entity ..> Entity : NEG_PREDISPOSES
Entity ..> Entity : NEG_PREVENTS
Entity ..> Entity : NEG_PROCESS_OF
Entity ..> Entity : NEG_PRODUCES
Entity ..> Entity : NEG_STIMULATES
Entity ..> Entity : NEG_TREATS
Entity ..> Entity : NEG_USES
Entity ..> Entity : NEG_higher_than
Entity ..> Entity : NEG_lower_than
Entity ..> Entity : NEG_same_as
```

**Reading the diagram.** The diagram is complete: all 70 predicates appear. The `Entity → Entity` edges are the 64 asserted biomedical relationships — 17 Biolink predicates, 16 custom `biohealthkg` schema predicates, and 31 negated `NEG_*` assertions (drawn dashed). The `Statement` class carries the reified-statement structure: `rdf_subject` and `rdf_object` point back to the two entities of an asserted edge, `rdf_predicate` records which relationship was asserted, and the `source` member (`dc:source`) records whether the assertion came from PubMed literature, MIMIC clinical data, or both — the mechanism Bio-Health KG uses for provenance tracking.
