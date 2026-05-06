# Proto-OKN Cross-Graph Opportunity Analysis — Bio/Biomedical/Rare Diseases/Clinical

👤 **User**

```
# Proto-OKN cross-graph opportunity analysis
# Focus area: Bio/Biomedical/Rare Diseases/Clinical
# Run this prompt with proto-okn tools available.
## Step 1 — Inventory the graphs
Call `list_graphs` for each domain tag relevant to focus area.
For each graph returned, extract and record:
  - Graph name and named graph URI
  - All identifier namespaces (e.g. MONDO, HPO, Ensembl, InChIKey)
  - All entity classes and their URIs
  - Vocabulary/ontology frameworks used (Biolink, MeSH, Schema.org, RO, etc.)
  - Whether the graph uses edge properties (reified associations vs simple triples)
Present this as a structured inventory table with one row per graph.
## Step 2 — Map shared identifiers across graphs
From the inventory above, identify every identifier namespace that appears
in TWO OR MORE graphs. For each shared namespace:
  - Name the namespace (e.g. NCBI_Gene, UMLS, InChIKey)
  - List all graphs that use it
  - State what entity type it identifies in each graph
  - Flag any namespace mismatches (same ID system, different entity classes)
Then identify shared ontology/vocabulary frameworks (e.g. Biolink Model,
MeSH, GO, UBERON) and list which graphs use each one.
## Step 3 — Identify bridge entity types
For each shared identifier namespace from Step 2, determine whether it can
serve as a JOIN key between graphs. A bridge entity is one where:
  - The same real-world entity (gene, disease, compound, anatomy) is
    represented in multiple graphs under the same identifier scheme
  - A SPARQL query could match ?entity in Graph A to ?entity in Graph B
    using that shared identifier
For each confirmed bridge, call `get_join_strategy` with the two graph names
to get the recommended join approach. Note any caveats (e.g. URI vs literal,
prefix differences, owl:sameAs links needed).
## Step 4 — Score cross-graph query opportunities
For each pair of graphs connected by at least one bridge entity, propose a
concrete cross-graph query opportunity. Use this scoring rubric:
  Richness  — how many distinct entity types does the join unlock?
  Novelty   — does the combination expose relationships not in either graph alone?
  Feasibility — is the join key clean (URI match) or fragile (string/literal match)?
Rate each opportunity High / Medium / Low on each dimension.
Rank the full list by overall opportunity score (H=3, M=2, L=1, sum across dims).
## Step 5 — Write example SPARQL skeletons
For the TOP 3 ranked opportunities from Step 4:
  1. Call `get_schema` on each graph involved to confirm predicate URIs
  2. Write a SPARQL query skeleton that demonstrates the cross-graph join.
     Use SERVICE clauses or federated query patterns where appropriate.
     Use placeholder URIs like <ENTITY_URI> for the seed entity.
  3. Annotate each query with a one-sentence scientific question it answers.
  4. Note any owl:sameAs, skos:exactMatch, or identifier bridging triples
     that would be needed to execute the join.
## Step 6 — Flag gaps and dead ends
Identify graph pairs that appear thematically related but lack a clean
identifier bridge. For each gap:
  - Name the two graphs and the thematic overlap
  - Identify what identifier or mapping would be needed to connect them
  - Suggest whether an intermediate graph (e.g. biobricks-mesh as a
    vocabulary hub) could bridge the gap
## Output format
Deliver results in this order:
  1. Inventory table (Step 1)
  2. Shared identifier map (Step 2) — grouped by namespace
  3. Bridge entity list (Step 3) — one row per confirmed bridge
  4. Ranked opportunity table (Step 4) — sorted by score descending
  5. Top-3 SPARQL skeletons (Step 5) — with scientific question annotation
  6. Gap report (Step 6) — with bridging suggestions
Keep SPARQL readable: use PREFIX declarations, indent consistently,
and add inline comments explaining each clause.
```

---

🧠 **Assistant**

*(Tools invoked: `tool_search` × 2, `proto-okn:list_graphs` × 3 [biology, health, rare_disease, biomedical domains], `proto-okn:get_join_strategy` × 14 pairs, `proto-okn:get_schema` × 4 graphs [spoke-okn, gene-expression-atlas-okn, biobricks-aopwiki, spoke-genelab], `visualize:read_me`, `visualize:show_widget`)*

## Summary of Findings

### Step 1 — Graph Inventory

Twelve graphs are in scope across the bio/biomedical/rare-disease/clinical domain cluster. The richest graphs for cross-graph work are **spoke-okn** (7 entity classes, 35 predicates, geospatial + drug + disease + gene), **gene-expression-atlas-okn** (15 entity classes, quantitative expression data via Biolink GeneExpressionMixin), and **spoke-genelab** (spaceflight multi-omics with three reified edge types carrying statistical scores). At the disease-phenotype end, **oard-kg** and **biomarkerkg** have nearly identical schemas — both Biolink-aligned with log-odds statistical evidence — making them natural merge candidates once URI format issues are resolved.

### Step 2 — Shared Identifier Map

Fourteen namespace-sharing pairs were identified. The clearest cross-cutting namespaces are **Ensembl** (4 graphs), **NCBI_Gene** (4 graphs), **InChIKey** (4 graphs), **GO** (5 graphs), and **MONDO** (3 graphs). The most important mismatches: NCBI_Gene is stored as a URI in spoke-genelab but as a string literal in gene-expression-atlas-okn, requiring a `STRAFTER()` cast to join. InChIKey in spoke-okn lives inside a compound `hasDbXref` literal of the form `"InChIKey:XXXXX"` — callers must use `STRAFTER(..., "InChIKey:")`.

### Step 3 — Bridge Entities

Seven confirmed cross-graph joins were returned by `get_join_strategy`. The three strongest bridges — **Ensembl** (spoke-okn ↔ GEA-atlas), **NCBI_Gene + UBERON** (GEA-atlas ↔ spoke-genelab), and **InChIKey + ChEBI** (spoke-okn ↔ biobricks-aopwiki) — are all executable without owl:sameAs or external mapping tables, using direct string-literal comparisons or URI prefix normalization. The weakest bridge is the three-hop spoke-okn → atlas → spoke-genelab chain, which should be materialized as a named graph or staging query rather than run as live SERVICE chaining.

### Step 4 — Ranked Opportunities

The top opportunity by score (9/9) is **spoke-okn ↔ gene-expression-atlas-okn**: connecting drug-disease-gene association knowledge to real differential expression measurements. Three pairs tie at score 8, with the **spoke-okn ↔ biobricks-aopwiki** pairing (score 8) being the most scientifically novel — it bridges therapeutic pharmacology with mechanistic adverse outcome pathway toxicology, a combination not found in either graph alone.

### Step 5 — SPARQL Skeletons

Three query skeletons are provided below. Each uses `SERVICE` federated query patterns against the FRINK SPARQL endpoints. Key implementation notes:
1. The GEA-Atlas `GeneExpressionMixin` uses Biolink `subject/object/predicate` triple-style reification — query via `?assocNode biolink:object ?gene` not a direct triple.
2. spoke-genelab uses standard RDF reification (`rdf:subject / rdf:predicate / rdf:object`) for its edge properties.
3. spoke-okn's `TREATS_CtD` predicate is also RDF-reified — use `rdf:subject / rdf:predicate / rdf:object` rather than a direct triple.

### Step 6 — Gaps and Dead Ends

Six gap pairs were identified. The most impactful unsolved gap is **oard-kg ↔ biomarkerkg**: two graphs with structurally identical schemas and overlapping namespaces (HPO + MONDO) that the join tool cannot connect — almost certainly a URI prefix format problem, not a true semantic mismatch. Resolving this with a SPARQL normalization query (using `rdfs:label` matching as fallback) would unlock a rare-disease phenotype + biomarker evidence supergraph. The **oard-kg / biomarkerkg ↔ spoke-okn** gap requires a MONDO→DOID mapping table; `biobricks-mesh` and `biohealth` can serve as partial vocabulary hubs but cannot fully close it without an external ontology mapping service.

---

## Step 1 — Graph Inventory Table

| Graph | Named Graph URI (suffix) | Domain Tags | Identifier Namespaces | Key Entity Classes | Vocab / Ontology | Edge Props? |
|---|---|---|---|---|---|---|
| **biobricks-aopwiki** | /biobricks-aopwiki | biology, health, toxicology | CAS, ChEBI, ChEMBL, InChIKey, PubChem | AOP, Key Event, KER, Biological Process, Organ Context, Chemical Identifier, Disease/Disorder | AOP-Wiki ontology, GO, CHEMINF | No |
| **biobricks-ice** | /biobricks-ice | biology, chemistry, toxicology | CAS, DTXSID, InChIKey, NCBI_Gene | Bioassay, Chemical Entity, Biological Target, Gene Identifier, Assay Result | BAO, CHEMINF, SIO, RO | No |
| **biobricks-mesh** | /biobricks-mesh | biology, health, vocabulary | MeSH | Descriptor, Concept, Term, Disease [C], Chemicals [D], Anatomy [A] | MeSH RDF, SKOS | No |
| **biohealth** | /biohealth | biology, health, social_determinants | MeSH, MONDO, UMLS | Disease, SDoH entity, biomedical relationships (110M+ triples from PubMed + EHR) | Biolink, RDF reification | No* |
| **gene-expression-atlas-okn** | /gene-expression-atlas-okn | biology, genomics, health | CL, Ensembl, GeneSymbol, GO, NCBI_Gene, UBERON | Gene, Disease, AnatomicalEntity, Cell, Assay, Study, GeneExpressionMixin, Pathway | Biolink Model, UBERON, CL, GO | Yes |
| **ncipidkg** | /ncipidkg | biology, biomedical, cancer, pathways | GO, INDRA, NCI-PID, RO | Protein, Statement (reified), Dataset; regulatory interactions with GO process annotations | NCI-PID 2.0, RO, VoID, GO | No |
| **spoke-genelab** | /spoke-genelab | biology, genomics, space_biology | CL, GeneSymbol, NCBI_Gene, UBERON | Gene, Assay, Study, Mission, Anatomy, CellType, MethylationRegion, Organism | Biolink, UBERON, CL, OBI | Yes |
| **spoke-okn** | /spoke-okn | biology, chemistry, environment, geospatial, health | ChEBI, DOID, Ensembl, FIPS, InChIKey, TAXON | Disease, Gene, ChemicalEntity, AdministrativeArea, SDoH, OrganismTaxon, EnvironmentalFeature | Biolink, Schema.org, oboInOwl, GeoSPARQL | Yes |
| **biomarkerkg** | /biomarkerkg | biomarkers, biomedical, disease, phenotypes | Biolink, HPO, MONDO, VoID | Disease, PhenotypicFeature, Disease-Phenotype Association, Log Odds Analysis Result, Study | Biolink, VoID, HPO, MONDO | No |
| **oard-kg** | /oard-kg | clinical_data, health, phenotypes, rare_disease | HPO, MONDO, UMLS | Disease, PhenotypicFeature, Disease-Phenotype Association, Log Odds Analysis Result, Study | Biolink, VoID, HPO, MONDO | No |
| **pankgraph** | /pankgraph | biomedical, diabetes, genomics, pancreas | BioSample, dbSNP, Ensembl, GEO, GO, HGNC, NCBI_Gene, PubMed | Gene, SNP, SNV, Open Chromatin Region, Cell, Disease, GO Term, Article, Dataset | Biolink, GO, SO, HGNC | No |
| **prokn** | /prokn | biomedical, drug_discovery, genetic_variants, pathways, precision_medicine | BAO, EC_Number, Ensembl, GO, InChIKey, NCIT, PubMed, UniProt | Protein, Gene, Drug, PTM Annotation, Natural Variant, Pathway, Disease, Cell Line | UniProt RDF, GO, NCIT, SIO, Schema.org | No |

*\* biohealth uses RDF reification internally for provenance; edge properties not exposed via standard schema.*

---

## Step 2 — Shared Identifier Map

| Namespace | Graphs | Entity type per graph | Mismatch? |
|---|---|---|---|
| **InChIKey** | biobricks-aopwiki, biobricks-ice, spoke-okn, prokn | Chemical stressor (aopwiki) · Chemical entity (ice) · ChemicalEntity node property via hasDbXref (spoke) · Drug/compound (prokn) | **Partial** — aopwiki: value on InChIKey class node; spoke: literal in xref; needs string normalization |
| **Ensembl** | gene-expression-atlas-okn, spoke-okn, pankgraph, prokn | Gene node property ensembl_id (atlas) · Gene node property ensembl (spoke) · Gene (pankgraph, prokn) | **Partial** — spoke/atlas: string literals; pankgraph/prokn: may use URI form |
| **NCBI_Gene** | biobricks-ice, gene-expression-atlas-okn, spoke-genelab, pankgraph | Gene target (ice) · Gene node property ncbi_gene_id (atlas) · Gene node URI (genelab) · Gene (pankgraph) | **Mismatch** — genelab: URI-based; atlas/ice: string literal |
| **GeneSymbol** | gene-expression-atlas-okn, spoke-genelab | Gene node property symbol (atlas) · Gene node property symbol (genelab) | **Clean** — both string literals; usable as fallback join key |
| **UBERON** | gene-expression-atlas-okn, spoke-genelab | AnatomicalEntity (atlas) · Anatomy node (genelab) | **Clean** — URI-based in both; enables tissue-level join |
| **CL** (Cell Ontology) | gene-expression-atlas-okn, spoke-genelab | Cell (atlas) · CellType (genelab) | **Clean** — URI-based in both |
| **MONDO** | biohealth, biomarkerkg, oard-kg | Disease (biohealth) · Disease (biomarkerkg) · Disease (oard-kg) | **Partial** — biohealth↔spoke-okn join confirmed; biomarkerkg/oard-kg URI patterns unresolved by tool |
| **HPO** | biomarkerkg, oard-kg | PhenotypicFeature (biomarkerkg) · PhenotypicFeature (oard-kg) | **Partial** — thematically identical schemas; join tool returned false — URI format mismatch suspected |
| **UMLS** | biohealth, oard-kg | Concept (biohealth) · Disease/Phenotype CUI (oard-kg) | **Partial** — potential bridge; not confirmed by join tool |
| **ChEBI** | biobricks-aopwiki, spoke-okn | Chemical stressor identifier (aopwiki) · ChemicalEntity xref (spoke) | **Clean** — join confirmed |
| **CAS** | biobricks-aopwiki, biobricks-ice | Chemical stressor (aopwiki) · Chemical entity (ice) | **Clean** — join confirmed |
| **GO** | biobricks-aopwiki, gene-expression-atlas-okn, ncipidkg, pankgraph, prokn | Biological Process xref (aopwiki) · BiologicalProcess (atlas) · Process type on edges (ncipid) · GO Term (pankgraph, prokn) | **Partial** — URI-based in atlas/pankgraph/prokn; thematic annotation only in ncipidkg edges |
| **MeSH** | biobricks-mesh, biohealth | All controlled vocab entities (mesh) · Disease/SDoH concept (biohealth) | **Clean** — biobricks-mesh is the MeSH authority; biohealth references MeSH URIs |
| **PubMed** | pankgraph, prokn, nde | Article/evidence (pankgraph, prokn) · Dataset metadata (nde) | **Metadata only** — useful for provenance linking, not entity-level joins |

**Shared vocabulary/ontology frameworks:**

| Framework | Graphs using it |
|---|---|
| **Biolink Model** | gene-expression-atlas-okn, spoke-genelab, spoke-okn, biohealth, biomarkerkg, oard-kg, pankgraph |
| **GO (Gene Ontology)** | biobricks-aopwiki, gene-expression-atlas-okn, ncipidkg, pankgraph, prokn |
| **UBERON** | gene-expression-atlas-okn, spoke-genelab |
| **MeSH** | biobricks-mesh, biohealth, spoke-okn (as node property) |
| **VoID** | biomarkerkg, oard-kg, ncipidkg, prokn |
| **CHEMINF** | biobricks-aopwiki, biobricks-ice |

---

## Step 3 — Bridge Entity List

| # | Graph A | Graph B | Namespace / JOIN key | Entity in A | Entity in B | Join mechanism | Caveat |
|---|---|---|---|---|---|---|---|
| B1 | spoke-okn | gene-expression-atlas-okn | **Ensembl** | Gene (`spoke:ensembl` node property) | Gene (`gea:ensembl_id` node property) | String literal FILTER(?ensemblA = ?ensemblB) | Both are string literals — clean |
| B2 | gene-expression-atlas-okn | spoke-genelab | **NCBI_Gene + GeneSymbol + UBERON** | Gene (ncbi_gene_id prop); AnatomicalEntity (URI) | Gene (URI-based); Anatomy (URI-based) | NCBI_Gene: literal↔URI; GeneSymbol: literal↔literal; UBERON: URI↔URI | NCBI_Gene: atlas stores as string, genelab as URI — use STR() cast on genelab URI |
| B3 | spoke-okn | biobricks-ice | **InChIKey** | ChemicalEntity (hasDbXref literal, format "InChIKey:XXXX") | Chemical Entity (InChIKey literal) | STRAFTER(xref, "InChIKey:") = ice:inchikey | Must strip "InChIKey:" prefix from spoke xref |
| B4 | spoke-okn | biobricks-aopwiki | **InChIKey + ChEBI** | ChemicalEntity (hasDbXref literals) | Chemical stressor (InChIKey class node label; ChEBI identifier) | InChIKey: label match; ChEBI: URI or identifier match | aopwiki stores InChIKey as rdfs:label on CHEMINF_000407 instance |
| B5 | biobricks-ice | biobricks-aopwiki | **CAS + InChIKey** | Chemical Entity (CAS literal, InChIKey literal) | Chemical stressor (CAS, InChIKey) | Dual-key join; CAS is cleanest (both plain string literals) | None — strongest bridge in the inventory |
| B6 | biohealth | spoke-okn | **MONDO** | Disease (MONDO URI) | Disease (MONDO URI via ISA_DiD hierarchy) | URI match: ?diseaseA = ?diseaseB | MONDO URI format should align; confirm with sample query |
| B7 | spoke-okn | spoke-genelab | **Via bridge: gene-expression-atlas-okn** | Gene (Ensembl) | Gene (NCBI_Gene URI) | Two-hop: spoke Ensembl → atlas Ensembl+NCBI_Gene → genelab NCBI_Gene URI | Fragile — two SERVICE hops; may time out on large queries |

---

## Step 4 — Ranked Opportunity Table

Scored on Richness (entity types unlocked), Novelty (relationships not in either graph alone), Feasibility (join key cleanliness). H=3, M=2, L=1.

| Rank | Graph pair | Bridge | Richness | Novelty | Feasibility | Score | Scientific question |
|---|---|---|---|---|---|---|---|
| 1 | **spoke-okn ↔ gene-expression-atlas-okn** | Ensembl | H | H | H | **9** | Which genes associated with a disease (SPOKE) also show significant differential expression in disease-context assays, and can drug-gene perturbation data explain the expression direction? |
| 2 | **gene-expression-atlas-okn ↔ spoke-genelab** | NCBI_Gene + GeneSymbol + UBERON | H | H | M | **8** | Do genes dysregulated in a human disease also show conserved perturbation during spaceflight in the same tissue — suggesting shared stress-response pathways? |
| 2 | **spoke-okn ↔ biobricks-aopwiki** | InChIKey + ChEBI | H | H | M | **8** | For drugs known to treat a disease, which adverse outcome pathways do they initiate, and what key events bridge therapeutic action to potential off-target toxicity? |
| 4 | **biobricks-ice ↔ biobricks-aopwiki** | CAS + InChIKey | M | H | H | **8** | Which in vitro bioassay-active chemicals also map to AOPs with adverse outcomes relevant to human health — bridging assay data to mechanistic toxicology? |
| 5 | **biohealth ↔ spoke-okn** | MONDO | H | M | M | **7** | Do social determinants of health (MONDO-linked, from biohealth) correlate geographically with disease prevalence patterns (SPOKE) for the same disease? |
| 5 | **spoke-okn ↔ spoke-genelab** (3-graph) | Via atlas bridge | H | H | L | **7** | Which drug-regulated genes (SPOKE) are also perturbed in spaceflight experiments (spoke-genelab) — identifying candidates for spaceflight countermeasure drugs? |
| 7 | **spoke-okn ↔ biobricks-ice** | InChIKey | M | M | M | **6** | Among drugs treating a disease, which also show activity in vitro assays for relevant biological targets — informing mechanism of action or repurposing? |

---

## Step 5 — Top-3 SPARQL Skeletons

### Query 1 — spoke-okn ↔ gene-expression-atlas-okn (rank 1, score 9)

**Scientific question:** For a seed disease, which SPOKE-associated genes also show significant differential expression (log₂FC, adj-p) in Gene Expression Atlas disease assays — and can we rank them by expression effect size?

*Join key: Ensembl ID string literal. Both graphs store it as a node property (`spoke:ensembl` · `gea:ensembl_id`). No prefix normalization needed — clean string match.*

```sparql
# PREFIX declarations
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX spoke:   <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX gea:     <https://spoke.ucsf.edu/genelab/>
PREFIX obo:     <http://www.geneontology.org/formats/oboInOwl#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?geneName ?ensemblId ?log2fc ?adjPval ?studyTitle ?assayLabel
WHERE {

  # ── GRAPH A: spoke-okn ─────────────────────────────────────────────────
  SERVICE <https://frink.apps.renci.org/spoke-okn/sparql> {
    # Seed: genes associated with the disease of interest
    <DISEASE_URI>          # e.g. https://purl.org/okn/frink/kg/spoke-okn/…/DOID_9351
      spoke:ASSOCIATES_DaG  ?gene .

    # Pull Ensembl ID (the JOIN key) and human-readable label
    ?gene spoke:ensembl  ?ensemblId ;
          rdfs:label     ?geneName .
  }

  # ── GRAPH B: gene-expression-atlas-okn ────────────────────────────────
  SERVICE <https://frink.apps.renci.org/gene-expression-atlas-okn/sparql> {
    # Find atlas Gene node matching the same Ensembl ID (string literal JOIN)
    ?atlasGene  gea:ensembl_id  ?ensemblId .      # ← JOIN key

    # GeneExpressionMixin: reified association carries quantitative stats
    ?assocNode  biolink:object   ?atlasGene ;
                biolink:subject  ?assay ;
                gea:effect_size  ?log2fc ;
                gea:p_value      ?adjPval .

    # Optionally restrict to assays studying the same disease context
    OPTIONAL { ?assay biolink:has_input ?diseaseCtx . }

    # Study metadata for provenance
    OPTIONAL {
      ?study  biolink:has_output  ?assay ;
              gea:project_title   ?studyTitle ;
              rdfs:label          ?assayLabel .
    }

    FILTER (?adjPval < 0.05)
  }

}
ORDER BY ASC(?adjPval)
LIMIT 100

# BRIDGING NOTE: Both graphs use Ensembl IDs as plain string literals.
# owl:sameAs or skos:exactMatch are NOT required — FILTER equality suffices.
# If results are sparse, relax FILTER to ?adjPval < 0.1 first.
```

---

### Query 2 — gene-expression-atlas-okn ↔ spoke-genelab (rank 2, score 8)

**Scientific question:** Which genes dysregulated in a human disease (GEA Atlas disease studies) are also significantly perturbed in spaceflight experiments in the same tissue type (spoke-genelab) — identifying putative stress-response or disease-linked genes conserved across environmental stressors?

*Join key: NCBI Gene ID (STRAFTER on genelab URI) or GeneSymbol literal fallback. UBERON enables optional tissue-level join. **Caveat:** genelab stores gene as URI (`ncbi:<id>`); atlas as string property — use `STR()` or `STRAFTER()` to normalize.*

```sparql
# PREFIX declarations
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX gea:     <https://spoke.ucsf.edu/genelab/>
PREFIX gl:      <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obi:     <http://purl.obolibrary.org/obo/OBI_>

SELECT ?geneSymbol ?ncbiId ?gea_log2fc ?gea_pval
       ?gl_log2fc ?gl_adjPval ?tissueLabel ?sfAssay ?sfStudy
WHERE {

  # ── GRAPH A: gene-expression-atlas-okn ────────────────────────────────
  SERVICE <https://frink.apps.renci.org/gene-expression-atlas-okn/sparql> {
    # Studies focusing on the seed disease
    ?geaStudy biolink:studies  <DISEASE_URI> ;
              biolink:has_output ?geaAssay .

    # GeneExpressionMixin with quantitative properties
    ?geaAssoc  biolink:subject   ?geaAssay ;
               biolink:object    ?geaGene ;
               gea:effect_size   ?gea_log2fc ;
               gea:p_value       ?gea_pval .

    # Extract both identifiers for cross-graph matching
    ?geaGene  gea:ncbi_gene_id  ?ncbiId ;     # string, e.g. "7157"
              biolink:symbol     ?geneSymbol .

    FILTER (?gea_pval < 0.05)
  }

  # ── GRAPH B: spoke-genelab ────────────────────────────────────────────
  SERVICE <https://frink.apps.renci.org/spoke-genelab/sparql> {
    # Gene node in genelab uses NCBI URI — extract numeric ID to compare
    ?glGene  a  biolink:Gene .
    BIND(STRAFTER(STR(?glGene), "ncbigene/") AS ?glNcbiStr)
    FILTER(?glNcbiStr = ?ncbiId)              # ← JOIN key: NCBI Gene ID

    # Reified differential expression edge with statistics
    ?glStmt  rdf:subject    ?sfAssay ;
             rdf:predicate  gl:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG ;
             rdf:object     ?glGene ;
             gl:log2fc      ?gl_log2fc ;
             gl:adj_p_value ?gl_adjPval .

    # Optional: tissue join via UBERON (second JOIN key)
    OPTIONAL {
      ?sfAssay  gl:INVESTIGATED_ASiA  ?anatomy .
      ?anatomy  rdfs:label            ?tissueLabel .
    }

    # Study metadata for context
    OPTIONAL {
      ?sfStudy  gl:PERFORMED_SpAS  ?sfAssay ;
                gl:project_title   ?sfStudyTitle .
    }

    FILTER (?gl_adjPval < 0.05)
  }

}
ORDER BY DESC(ABS(?gl_log2fc))
LIMIT 50

# BRIDGING NOTE: No owl:sameAs needed — use STRAFTER on genelab URI to
# extract the numeric NCBI Gene ID and compare to atlas string literal.
# GeneSymbol can serve as a secondary FILTER if NCBI IDs are sparse.
# UBERON URIs are shared natively — ?anatomy URI = URI in both graphs.
```

---

### Query 3 — spoke-okn ↔ biobricks-aopwiki (rank 2, score 8)

**Scientific question:** For compounds that treat a given disease (SPOKE pharmacological knowledge), which adverse outcome pathways (AOP-Wiki) do those same compounds initiate — linking therapeutic use to mechanistic toxicology pathways and key events?

*Join keys: InChIKey (extract from spoke `hasDbXref` literals) and ChEBI ID (spoke xref → aopwiki ChEBI identifier node). **Caveat:** aopwiki stores InChIKey as `rdfs:label` on a `CHEMINF_000407` instance — navigate via cheminf:has_identifier chain.*

```sparql
# PREFIX declarations
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX spoke:   <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX aop:     <http://aopkb.org/aop_ontology#>
PREFIX cheminf: <http://semanticscience.org/resource/>
PREFIX obo:     <http://www.geneontology.org/formats/oboInOwl#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dc:      <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?compoundName ?inchikey
                ?aopTitle ?keyEventLabel ?adverseOutcomeLabel
WHERE {

  # ── GRAPH A: spoke-okn ─────────────────────────────────────────────────
  SERVICE <https://frink.apps.renci.org/spoke-okn/sparql> {
    # Reified TREATS_CtD edge (has optional phase/sources edge properties)
    ?treatStmt  rdf:subject    ?compound ;
                rdf:predicate  spoke:TREATS_CtD ;
                rdf:object     <DISEASE_URI> .      # seed disease

    ?compound  rdfs:label  ?compoundName ;
               obo:hasDbXref  ?xref .

    # Extract InChIKey from xref string "InChIKey:XXXXXXXXXXXXXX"
    FILTER(STRSTARTS(STR(?xref), "InChIKey:"))
    BIND(STRAFTER(STR(?xref), "InChIKey:") AS ?inchikey)
  }

  # ── GRAPH B: biobricks-aopwiki ─────────────────────────────────────────
  SERVICE <https://frink.apps.renci.org/biobricks-aopwiki/sparql> {
    # InChIKey is stored as rdfs:label on a CHEMINF_000407 (InChIKey class) instance
    ?inchikeyNode  a          cheminf:CHEMINF_000407 ;   # InChIKey class
                   rdfs:label ?inchikey .                  # ← JOIN key

    # Navigate from InChIKey node → parent chemical info → AOP
    ?chemInfo   cheminf:has_identifier  ?inchikeyNode .
    ?aop        aop:has_chemical_entity ?chemInfo .

    # AOP title and key events
    ?aop  dc:title               ?aopTitle ;
          aop:has_key_event      ?ke .
    ?ke   rdfs:label             ?keyEventLabel .

    # Adverse outcome (terminal key event)
    OPTIONAL {
      ?aop  aop:has_adverse_outcome  ?ao .
      ?ao   rdfs:label               ?adverseOutcomeLabel .
    }
  }

}
ORDER BY ?compoundName ?aopTitle
LIMIT 200

# BRIDGING NOTE: InChIKey is a string label, not a URI — no owl:sameAs needed.
# ChEBI is an alternative JOIN key if InChIKey coverage is low:
#   spoke:  FILTER(STRSTARTS(STR(?xref), "ChEBI:"))  BIND(STRAFTER(...) AS ?chebi)
#   aopwiki: ?chebiNode a cheminf:CHEMINF_000409 ; rdfs:label ?chebi .
# Use both join paths with UNION for maximum recall.
```

---

## Step 6 — Gap Report

### Gap 1 — oard-kg ↔ biomarkerkg

**Thematic overlap:** Nearly identical schemas — both model Disease–PhenotypicFeature associations with log-odds statistics, both declare HPO and MONDO namespaces. OARD derives from EHR clinical NLP; BiomarkerKG from biomarker evidence. A join would create the richest rare-disease phenotype + biomarker evidence resource in the network.

**Gap:** `get_join_strategy` returned false despite declared HPO and MONDO namespaces — strongly suggests URI prefix or format differences (e.g., OARD may use `hp:0001250` while biomarkerkg uses `http://purl.obolibrary.org/obo/HP_0001250`).

**Needed:** A normalization layer mapping both graphs' disease/phenotype node URIs to a canonical prefix (OBO PURL standard). An alternative: query both graphs for the same HPO label string using `rdfs:label` as the join key — slower but avoids URI format mismatch.

**Intermediate bridge:** `biobricks-mesh` can serve as a MeSH–UMLS vocabulary hub. Since both OARD and biomarkerkg also list UMLS, a UMLS CUI join via a mapping service (or the biohealth UMLS nodes) might work.

---

### Gap 2 — oard-kg / biomarkerkg ↔ spoke-okn

**Thematic overlap:** OARD and biomarkerkg contain disease–phenotype association statistics; spoke-okn has disease–gene associations, drug treatments, and geospatial disease prevalence. Joining would enable: for a rare disease, find its phenotypes (OARD), its genes (SPOKE), and its spatial prevalence pattern — a powerful translational query.

**Gap:** OARD/biomarkerkg use MONDO and HPO; spoke-okn uses DOID for diseases (not MONDO).

**Needed:** A MONDO→DOID mapping (available via Monarch Initiative and OBO cross-references). Path: OARD MONDO → biohealth MONDO → biohealth MeSH → spoke `mesh_list` node property.

---

### Gap 3 — pankgraph ↔ gene-expression-atlas-okn

**Thematic overlap:** Pankgraph focuses on pancreatic gene expression, eQTLs, and T1D genetics; GEA Atlas has disease-expression studies (potentially including pancreas tissue). Both list Ensembl in their namespaces. A join would cross-validate pancreatic eQTL variants with population-level gene expression studies.

**Gap:** `get_join_strategy` returned false. Pankgraph likely stores Ensembl IDs in a different RDF pattern vs. GEA's `gea:ensembl_id` string property.

**Needed:** Inspect pankgraph Gene nodes with a SPARQL probe (`SELECT ?g ?p ?o WHERE { ?g a <Gene> } LIMIT 5`) to surface the actual predicate carrying the Ensembl value. Once confirmed, a string literal join should work.

---

### Gap 4 — prokn ↔ spoke-okn

**Thematic overlap:** ProKN has UniProt proteins with PTMs, variants, kinase-substrate interactions, and drug targets; spoke-okn has drug–disease–gene associations. Joining would link SPOKE drug→gene perturbation to ProKN protein-level mechanism — enabling mechanistic interpretation of drug action.

**Gap:** spoke-okn uses Ensembl gene IDs; prokn uses UniProt protein IDs. The Ensembl→UniProt mapping (via "encodes" in prokn) is not exposed as a shared namespace.

**Needed:** Use prokn's `gene product of` / `encodes` predicates to map Gene (Ensembl) → Protein (UniProt) within prokn, then join the Ensembl ID from prokn's Gene nodes to spoke-okn's Gene nodes. `gene-expression-atlas-okn` may help bridge as a Gene identifier hub.

---

### Gap 5 — ncipidkg ↔ gene-expression-atlas-okn

**Thematic overlap:** NCI-PID has protein regulatory interactions annotated with GO biological process types; GEA Atlas has gene→GO biological process associations. Both describe genes/proteins in terms of GO processes.

**Gap:** NCI-PID uses GO terms as edge annotations (process type) on reified Statements; GEA Atlas uses GO as class membership for BiologicalProcess nodes. The query pattern differs entirely.

**Needed:** A thematic join (not entity-level) via GO term URI: find NCI-PID interactions annotated with a GO process, then find GEA Atlas genes associated with that same GO process. GO process URIs are standard OBO PURLs — no owl:sameAs needed. The join returns process-level associations rather than gene-level ones.

---

### Gap 6 — biohealth ↔ oard-kg

**Thematic overlap:** Both model disease knowledge with UMLS and MONDO identifiers; biohealth is literature-derived (PubMed + EHR); OARD is EHR-derived (clinical NLP). Joining would provide complementary evidence sources for the same disease–phenotype associations.

**Gap:** `get_join_strategy` returned false despite shared UMLS and MONDO namespace declarations. URI format normalization is likely required.

**Needed:** UMLS CUI as a string literal join key — FILTER equality on CUI strings (format "C0XXXXXXX") extracted from both graphs' disease or phenotype nodes.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-06*

*Model: claude-sonnet-4-6*
