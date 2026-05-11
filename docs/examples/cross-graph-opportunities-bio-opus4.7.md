## Chat Transcript
Proto-OKN Cross-Graph Opportunity Analysis — Bio / Biomedical / Rare Disease / Clinical

👤 **User**

Proto-OKN cross-graph opportunity analysis
Focus area: Bio/Biomedical/Rare Diseases/Clinical
Run this prompt with proto-okn tools available.
Step 1 — Inventory the graphs
Call `list_graphs` for each domain tag relevant to focus area. For each graph returned, extract and record:

* Graph name and named graph URI
* All identifier namespaces (e.g. MONDO, HPO, Ensembl, InChIKey)
* All entity classes and their URIs
* Vocabulary/ontology frameworks used (Biolink, MeSH, Schema.org, RO, etc.)
* Whether the graph uses edge properties (reified associations vs simple triples) Present this as a structured inventory table with one row per graph.
Step 2 — Map shared identifiers across graphs
From the inventory above, identify every identifier namespace that appears in TWO OR MORE graphs. For each shared namespace:

* Name the namespace (e.g. NCBI_Gene, UMLS, InChIKey)
* List all graphs that use it
* State what entity type it identifies in each graph
* Flag any namespace mismatches (same ID system, different entity classes) Then identify shared ontology/vocabulary frameworks (e.g. Biolink Model, MeSH, GO, UBERON) and list which graphs use each one.
Step 3 — Identify bridge entity types
For each shared identifier namespace from Step 2, determine whether it can serve as a JOIN key between graphs. A bridge entity is one where:

* The same real-world entity (gene, disease, compound, anatomy) is represented in multiple graphs under the same identifier scheme
* A SPARQL query could match ?entity in Graph A to ?entity in Graph B using that shared identifier For each confirmed bridge, call `get_join_strategy` with the two graph names to get the recommended join approach. Note any caveats (e.g. URI vs literal, prefix differences, owl:sameAs links needed).
Step 4 — Score cross-graph query opportunities
For each pair of graphs connected by at least one bridge entity, propose a concrete cross-graph query opportunity. Use this scoring rubric: Richness — how many distinct entity types does the join unlock? Novelty — does the combination expose relationships not in either graph alone? Feasibility — is the join key clean (URI match) or fragile (string/literal match)? Rate each opportunity High / Medium / Low on each dimension. Rank the full list by overall opportunity score (H=3, M=2, L=1, sum across dims).
Step 5 — Write example SPARQL skeletons
For the TOP 3 ranked opportunities from Step 4:

1. Call `get_schema` on each graph involved to confirm predicate URIs
2. Write a SPARQL query skeleton that demonstrates the cross-graph join. Use SERVICE clauses or federated query patterns where appropriate. Use placeholder URIs like <ENTITY_URI> for the seed entity.
3. Annotate each query with a one-sentence scientific question it answers.
4. Note any owl:sameAs, skos:exactMatch, or identifier bridging triples that would be needed to execute the join.
Step 6 — Flag gaps and dead ends
Identify graph pairs that appear thematically related but lack a clean identifier bridge. For each gap:

* Name the two graphs and the thematic overlap
* Identify what identifier or mapping would be needed to connect them
* Suggest whether an intermediate graph (e.g. biobricks-mesh as a vocabulary hub) could bridge the gap
Output format
Deliver results in this order:

1. Inventory table (Step 1)
2. Shared identifier map (Step 2) — grouped by namespace
3. Bridge entity list (Step 3) — one row per confirmed bridge
4. Ranked opportunity table (Step 4) — sorted by score descending
5. Top-3 SPARQL skeletons (Step 5) — with scientific question annotation
6. Gap report (Step 6) — with bridging suggestions Keep SPARQL readable: use PREFIX declarations, indent consistently, and add inline comments explaining each clause.

---

🧠 **Assistant**

# Proto-OKN Cross-Graph Opportunity Analysis — Bio / Biomedical / Rare Disease / Clinical

The focus area pulls graphs from the `biology`, `biomedical`, `health`, `clinical_data`, and `rare_disease` domain tags. Combining these tags yields **14 distinct knowledge graphs** in scope.

---

## 1. Inventory Table (Step 1)

| # | Graph | Named Graph URI | Identifier Namespaces | Key Entity Classes | Vocabulary Frameworks | Reified Edges? |
|---|---|---|---|---|---|---|
| 1 | **biobricks-aopwiki** | `…/kg/biobricks-aopwiki` | CAS, ChEBI, ChEMBL, InChIKey, PubChem | AdverseOutcomePathway, KeyEvent, KeyEventRelationship, BiologicalProcess, OrganContext, CellTypeContext, ChemicalIdentifier, InChIKey, PubChemCID, ChEBI, SMILES, GeneIdentifier, ProteinIdentifier, Disease/Disorder | AOP-Wiki ontology, CHEMINF/SIO, GO, NCBITaxon, EDAM, NCIT, Dublin Core | No |
| 2 | **biobricks-ice** | `…/kg/biobricks-ice` | CAS, DTXSID, InChIKey, NCBI_Gene | BioassayResult, ChemicalEntity, ChemicalIdentifier, Bioassay, BiologicalTarget, GeneIdentifier, AssayDesign | BAO, CHEMINF, SIO, RO, UMLS | No |
| 3 | **biobricks-mesh** | `…/kg/biobricks-mesh` | MeSH | Descriptor, Qualifier, SCR, Concept, Term, plus all 16 MeSH tree branches (A–Z) | MeSH RDF, SKOS | No |
| 4 | **biohealth** | `…/kg/biohealth` | MeSH, MONDO, UMLS | (registry hides class list — uses Biolink predicates: `location_of`, `affects`, `treats`, `coexists_with`, `causes`) | Biolink Model, custom SDoH schema, RDF reification | Yes (reified statements) |
| 5 | **biomarkerkg** | `…/kg/biomarkerkg` | Biolink, HPO, MONDO, VoID | Disease, PhenotypicFeature, Disease↔Phenotype Association, Entity↔Disease Association, LogOddsAnalysisResult, ConceptCountAnalysisResult, Study, Dataset | Biolink, VoID | No (statistical edge metadata as analysis-result classes) |
| 6 | **gene-expression-atlas-okn** | `…/kg/gene-expression-atlas-okn` | CL, Ensembl, GeneSymbol, GO, NCBI_Gene, UBERON | Gene, Assay, Study, Disease, AnatomicalEntity, Cell, Pathway, BiologicalProcess, ProteinDomain, LifeStage, BiologicalSex, Population, GeneExpressionMixin (assoc), Attribute | Biolink Model, GO, UBERON, CL, EFO | Yes (GeneExpressionMixin association class) |
| 7 | **ncipidkg** | `…/kg/ncipidkg` | GO, INDRA, NCI-PID, RO, VoID | protein, Statement, Dataset | RDF reification, GO, RO, VoID, INDRA evidence | Yes (reified Statement carries `evidence count`, `evidence URL`, `process type`) |
| 8 | **nde** (NIAID) | `…/kg/nde` | PubMed | DataCatalog, Dataset, DataDownload, ScholarlyArticle, MonetaryGrant, Person, Organization, ResearchProject, DefinedTerm | Schema.org | No |
| 9 | **oard-kg** | `…/kg/oard-kg` | HPO, MONDO, UMLS | Disease, PhenotypicFeature, Disease↔PhenotypicFeature Assoc, Phenotype↔Phenotype Assoc, LogOddsAnalysisResult, ConceptCountAnalysisResult, Study, Dataset | Biolink Model, MONDO, HPO | No (uses analysis-result classes for stats) |
| 10 | **pankgraph** | `…/kg/pankgraph` | BioSample, dbSNP, Ensembl, GEO, GO, HGNC, NCBI_Gene, PanKbase, PubMed, SO | Gene, Disease (T1D, T2D), SNP, SNV, OpenChromatinRegion, Cell, CellLine, GO term, Article, Dataset, Statement | Biolink, GO, SO, dbSNP, RDF reification | Yes (reified Statement w/ pip, slope, qtl evidence) |
| 11 | **prokn** | `…/kg/prokn` | BAO, EC_Number, Ensembl, GO, InChIKey, NCBI_Taxon, NCIT, PubMed, SMILES, UniProt | Protein, Gene, Disease, Drug, NaturalVariantAnnotation, PTMAnnotation, SiteAnnotation, Pathway, Tissue, CellLine, GTExExpression, Antibody, Experiment, Patient, GO Term | UniProt, NCIT, GO, NCBITaxon, BAO, Schema.org, OBI, MI, MAXO | No (rich annotation classes instead) |
| 12 | **spoke-genelab** | `…/kg/spoke-genelab` | CL, GeneSymbol, NCBI_Gene, UBERON | Assay, Anatomy, CellType, Gene, Study, MethylationRegion, Mission, Organism (microbe) | Biolink Model, UBERON, CL, OBI, custom spoke-genelab schema | Yes (MEASURED_DIFFERENTIAL_* reified w/ log2fc, adj_p_value) |
| 13 | **spoke-okn** | `…/kg/spoke-okn` | ChEBI, DOID, Ensembl, FIPS, InChIKey, TAXON | Disease, Gene, ChemicalEntity, OrganismTaxon, AdministrativeArea, EnvironmentalFeature, SDoH | Biolink Model, Schema.org, GeoSPARQL, custom spoke-okn schema | Yes (TREATS, PREVALENCE, MORTALITY, etc. all reified) |
| 14 | **ruralkg** | `…/kg/ruralkg` | FIPS, RUCC | County, City, State, RUCC, Substance, NIBRS, NSDUH, MentalHealthService, TreatmentProvider | Custom RuralKG ontology (sail.ua.edu) | No |

---

## 2. Shared Identifier Map (Step 2) — grouped by namespace

### Gene / protein identifiers

| Namespace | Graphs | Entity meaning | Mismatch flags |
|---|---|---|---|
| **Ensembl** | spoke-okn, gene-expression-atlas-okn, pankgraph, prokn | Gene (in spoke-okn, gene-atlas, pankgraph) and Gene-product/Protein context (in prokn) | Stored as `node property` in spoke-okn / gene-atlas, but as URI in pankgraph; check prefix `ENSG…` vs full IRI |
| **NCBI_Gene** (Entrez) | biobricks-ice, gene-expression-atlas-okn, spoke-genelab, pankgraph | Gene (target/biological target in ice; gene node in others) | spoke-genelab uses NCBI Gene as the URI itself; gene-atlas exposes it as `ncbi_gene_id` literal; pankgraph uses HGNC as primary plus NCBI |
| **GeneSymbol** | gene-expression-atlas-okn, spoke-genelab | Gene symbol (literal) | Both literal — case-sensitive string match (fragile) |
| **HGNC** | pankgraph | Gene | Singleton — bridge via NCBI_Gene |
| **UniProt** | prokn | Protein | Singleton — needs UniProt↔Ensembl mapping for cross-graph |

### Chemical identifiers

| Namespace | Graphs | Entity meaning | Mismatch flags |
|---|---|---|---|
| **InChIKey** | biobricks-aopwiki, biobricks-ice, spoke-okn, prokn | Chemical structure hash | Cleanest cross-graph chemical key. spoke-okn exposes via `oboInOwl:hasDbXref`; biobricks-* expose as `CHEMINF_000407` instances |
| **CAS** | biobricks-aopwiki, biobricks-ice | CAS Registry Number | Stored as `CHEMINF_000405` in both — consistent |
| **ChEBI** | biobricks-aopwiki, spoke-okn | Chemical of biological interest | spoke-okn carries via `seeAlso` / `hasDbXref`; aopwiki has dedicated ChEBI Identifier class |
| **PubChem** | biobricks-aopwiki | PubChem CID | Singleton — but cross-resolves via InChIKey |
| **ChEMBL** | biobricks-aopwiki | Chemical bioactivity | Singleton — could be a bridge to external ChEMBL MCP |
| **DTXSID** | biobricks-ice | EPA CompTox ID | Singleton |
| **SMILES** | prokn (also as `node property` on spoke-okn ChemicalEntity) | Structure string | Fragile — canonicalisation differences |

### Disease identifiers

| Namespace | Graphs | Entity meaning | Mismatch flags |
|---|---|---|---|
| **MONDO** | biohealth, biomarkerkg, oard-kg | Mondo Disease Ontology disease | **Most important rare-disease bridge.** Tool's `get_join_strategy` returned `can_join: false` for these pairs even though all three list MONDO in registry — the tool appears conservative; the join is real if URIs use the same `obo:MONDO_xxxxxxx` format |
| **DOID** | spoke-okn | Disease Ontology | Different scheme from MONDO — needs `skos:exactMatch` mapping (available in biobricks-mesh / Ubergraph) |
| **UMLS** | biohealth, oard-kg, biobricks-ice (as predicate "UMLS Concept") | Concept | UMLS CUI strings; stable but licensed |
| **MeSH** | biobricks-mesh, biohealth, spoke-okn (`mesh_list` on Disease, `mesh_ids` on SDoH) | Vocabulary term | spoke-okn carries MeSH only as a literal *list* on Disease/SDoH nodes — must split list |

### Phenotype / anatomy / cell / function

| Namespace | Graphs | Entity meaning |
|---|---|---|
| **HPO** | biomarkerkg, oard-kg | Phenotypic feature (very strong rare-disease bridge) |
| **UBERON** | gene-expression-atlas-okn, spoke-genelab | Anatomical entity |
| **CL** (Cell Ontology) | gene-expression-atlas-okn, spoke-genelab | Cell type |
| **GO** | gene-expression-atlas-okn, ncipidkg, pankgraph, prokn | Gene Ontology term (BP/MF/CC) |

### Geographic / structural / metadata

| Namespace | Graphs | Entity meaning |
|---|---|---|
| **FIPS** | spoke-okn, ruralkg | County / state code |
| **PubMed** | nde, pankgraph, prokn | Publication |
| **TAXON / NCBI_Taxon** | spoke-okn (`TAXON`), prokn (`NCBI_Taxon`), spoke-genelab (`taxonomy` literal on Gene) | Organism / species (note slight prefix variation) |

### Shared ontology / vocabulary frameworks

| Framework | Graphs |
|---|---|
| **Biolink Model** | biohealth, biomarkerkg, gene-expression-atlas-okn, oard-kg, pankgraph, spoke-genelab, spoke-okn (7 graphs) |
| **GO** (Gene Ontology) | biobricks-aopwiki, gene-expression-atlas-okn, ncipidkg, pankgraph, prokn |
| **UBERON** | gene-expression-atlas-okn, spoke-genelab, biobricks-aopwiki (organ context) |
| **CL** | gene-expression-atlas-okn, spoke-genelab, biobricks-aopwiki (cell type context) |
| **CHEMINF / SIO** | biobricks-aopwiki, biobricks-ice |
| **MeSH** | biobricks-mesh, biohealth, spoke-okn |
| **Schema.org** | nde, prokn (partial), spoke-okn (AdministrativeArea) |
| **VoID** | biomarkerkg, ncipidkg, pankgraph, oard-kg (dataset metadata) |
| **RDF reification** | biohealth, ncipidkg, pankgraph, spoke-genelab, spoke-okn |

---

## 3. Bridge Entity List (Step 3)

Each row is a confirmed bridge based on `get_join_strategy` plus registry inspection. ✅ = tool-confirmed; ⚠️ = registry-asserted but tool returned no-join (use with caution / inspect URI form).

| Bridge ID | Entity Type | Graph A | Graph B | Strategy | Confidence |
|---|---|---|---|---|---|
| B1 | Chemical (InChIKey) | biobricks-aopwiki | spoke-okn | aopwiki InChIKey instance ↔ spoke-okn `hasDbXref` literal | ✅ High |
| B2 | Chemical (ChEBI) | biobricks-aopwiki | spoke-okn | aopwiki ChEBI Identifier ↔ spoke-okn ChemicalEntity ChEBI xref | ✅ High |
| B3 | Chemical (CAS + InChIKey) | biobricks-ice | biobricks-aopwiki | Both store CAS as CHEMINF_000405 and InChIKey as CHEMINF_000407 | ✅ High |
| B4 | Chemical (InChIKey) | biobricks-ice | spoke-okn | InChIKey hash | ✅ High |
| B5 | Gene (NCBI_Gene + GeneSymbol + UBERON + CL) | spoke-genelab | gene-expression-atlas-okn | NCBI Entrez ID URI; UBERON / CL ontology URIs | ✅ High (multi-key) |
| B6 | Gene (Ensembl) | spoke-okn | gene-expression-atlas-okn | Ensembl literal on Gene | ✅ High |
| B7 | Gene (3-graph chain) | spoke-genelab → gene-expression-atlas-okn → spoke-okn | bridge via gene-atlas-okn (NCBI↔Ensembl) | ✅ High (tool returned `bridge_graph: gene-expression-atlas-okn`) |
| B8 | Geographic (FIPS) | spoke-okn | ruralkg | FIPS county/state codes | ✅ High |
| B9 | MeSH vocabulary | biohealth | biobricks-mesh | MeSH descriptor URI | ✅ High |
| B10 | MeSH (text-list) | spoke-okn | biobricks-mesh | spoke-okn `mesh_list` literal — must `STRSPLIT` | ⚠️ Med (literal list) |
| B11 | Disease (MONDO) | biohealth | oard-kg | Both list MONDO; tool conservative | ⚠️ Med (registry-only) |
| B12 | Disease (MONDO) + Phenotype (HPO) | biomarkerkg | oard-kg | Both list MONDO + HPO; near-identical schemas | ⚠️ Med (registry-only) |
| B13 | UMLS | biohealth | oard-kg | Both list UMLS | ⚠️ Med (registry-only) |
| B14 | Gene (NCBI_Gene) | biobricks-ice | gene-expression-atlas-okn | Both list NCBI_Gene; ice uses Entrez Gene ID literal | ⚠️ Med |
| B15 | Gene (NCBI_Gene) | biobricks-ice | spoke-genelab | NCBI Entrez Gene ID | ⚠️ Med |
| B16 | Gene (NCBI_Gene) | pankgraph | spoke-genelab | Both list NCBI_Gene | ⚠️ Med (tool returned no-join) |
| B17 | Gene (Ensembl) | pankgraph | spoke-okn | Both list Ensembl | ⚠️ Med (tool returned no-join) |
| B18 | Gene (Ensembl) | pankgraph | gene-expression-atlas-okn | Both list Ensembl | ⚠️ Med |
| B19 | GO term | ncipidkg | gene-expression-atlas-okn | GO URI | ⚠️ Med |
| B20 | GO term | ncipidkg | pankgraph | GO URI | ⚠️ Med |
| B21 | GO term | ncipidkg | prokn | GO URI | ⚠️ Med |
| B22 | InChIKey | prokn | spoke-okn | InChIKey | ⚠️ Med |
| B23 | InChIKey | prokn | biobricks-aopwiki | InChIKey | ⚠️ Med |
| B24 | PubMed ID | nde | pankgraph | PubMed ID | ⚠️ Med (tool returned no-join) |
| B25 | PubMed ID | nde | prokn | PubMed ID | ⚠️ Med |
| B26 | Taxonomy | spoke-okn | prokn | TAXON / NCBI_Taxon | ⚠️ Med (prefix mismatch) |

---

## 4. Ranked Opportunity Table (Step 4)

Scoring: Richness (entity-type breadth unlocked), Novelty (relations not in either graph alone), Feasibility (URI-clean = High; literal/list = Med; needs external mapping = Low). Score = sum (H=3, M=2, L=1).

| Rank | Opportunity | Bridge | Richness | Novelty | Feasibility | Score |
|---|---|---|---|---|---|---|
| **1** | **Chemical → AOP → therapeutic** (toxicology meets pharmacology): connect AOP-implicated chemicals to drugs that treat human disease | B1, B2 (aopwiki ↔ spoke-okn) | H | H | H | **9** |
| **2** | **Earth tissue expression vs spaceflight expression**: compare differential expression of the same gene in space-bio assays vs Earth disease assays | B5 (spoke-genelab ↔ gene-atlas) | H | H | H | **9** |
| **3** | **Drug-disease-gene network annotated with tissue-specific expression**: enrich SPOKE drug→gene→disease edges with tissue-of-action evidence | B6 (spoke-okn ↔ gene-atlas) | H | H | H | **9** |
| 4 | **3-graph chain: spaceflight gene → human gene ortholog → drug**: human therapeutics inferred from microgravity gene response | B7 (spoke-genelab → gene-atlas → spoke-okn) | H | H | M (multi-hop) | 8 |
| 5 | **Bioassay screening hits → AOP key events**: link ICE bioassay actives to mechanistic AOPs | B3 (ice ↔ aopwiki) | M | H | H | 8 |
| 6 | **Toxicology assays → therapeutic compound dossier**: chemicals in ICE bioassays cross-referenced with SPOKE drug-disease network | B4 (ice ↔ spoke-okn) | M | H | H | 8 |
| 7 | **County health × rural health**: SPOKE disease prevalence/SDoH joined to RuralKG substance-abuse/treatment-provider data by FIPS | B8 (spoke-okn ↔ ruralkg) | M | H | H | 8 |
| 8 | **Rare-disease phenotype + biomarker**: OARD HPO-MONDO clinical evidence joined with biomarker-disease associations | B12 (oard-kg ↔ biomarkerkg) | H | H | M (registry-only confirm) | 8 |
| 9 | **Diabetes islet QTL → SPOKE drug-gene network**: pankgraph T1D variant-gene evidence cross-referenced to drugs that up/downregulate same gene | B17 (pankgraph ↔ spoke-okn) | H | H | M (tool unconfirmed) | 8 |
| 10 | **Pancreas QTL × tissue expression context**: PanKgraph T1D evidence checked against ATLAS pan-tissue expression | B18 (pankgraph ↔ gene-atlas) | M | M | M | 6 |
| 11 | **NCI-PID pathway × differential expression**: cancer-pathway proteins ranked by tissue-specific expression | B19, B21 (ncipidkg ↔ gene-atlas / prokn via GO) | M | M | M | 6 |
| 12 | **MeSH-driven SDoH literature enrichment**: biohealth associations annotated with full MeSH tree context | B9 (biohealth ↔ biobricks-mesh) | M | M | H | 7 |
| 13 | **Disease-SDoH-Phenotype**: biohealth's MONDO-keyed SDoH disease links extended with OARD's clinical phenotype evidence | B11 (biohealth ↔ oard-kg) | H | H | M | 8 |
| 14 | **Protein PTM × pathway regulation**: ProKN PTM annotations joined to NCI-PID directed regulation via GO | B21 (prokn ↔ ncipidkg) | M | M | M | 6 |
| 15 | **NIAID datasets → pankgraph evidence by PubMed**: discover datasets that supplied evidence to PanKbase | B24 (nde ↔ pankgraph) | L | M | M | 5 |

---

## 5. Top-3 SPARQL Skeletons (Step 5)

> **Federation note.** All FRINK SPARQL endpoints support `SERVICE` clauses pointing to peer endpoints (`https://apps.okn.us/<graph>/sparql`). For richer joins, the `multi_graph_query` tool can also issue per-graph queries and merge in the application layer; the skeletons below show the federated form first.

### 🥇 Opportunity #1 — Chemicals on AOPs that already have a clinical drug indication

**Scientific question.** *"For chemicals whose toxicity is described by an Adverse Outcome Pathway, which ones are simultaneously approved/used as therapeutic compounds for some disease in SPOKE — i.e., where does therapeutic use overlap with mechanistic toxicity?"*

**Bridge.** InChIKey (preferred — canonical) and ChEBI (secondary). InChIKey lives as `CHEMINF_000407` literal in aopwiki and as a `oboInOwl:hasDbXref` value or node-property in spoke-okn.

```sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:      <http://purl.org/dc/elements/1.1/>
PREFIX aop:     <http://aopkb.org/aop_ontology#>
PREFIX cheminf: <http://semanticscience.org/resource/>
PREFIX oboInOwl:<http://www.geneontology.org/formats/oboInOwl#>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX spoke:   <https://purl.org/okn/frink/kg/spoke-okn/schema/>

# AOP-Wiki side: AOP → chemical → InChIKey literal
SELECT ?aopLabel ?chemLabel ?inchikey ?disease ?diseaseLabel ?phase
WHERE {
  # ---------- biobricks-aopwiki ----------
  SERVICE <https://apps.okn.us/biobricks-aopwiki/sparql> {
    ?aop  a aop:AdverseOutcomePathway ;
          rdfs:label ?aopLabel ;
          aop:has_chemical_entity ?chem .                 # AOP linked to chemical stressor
    ?chem rdfs:label ?chemLabel ;
          cheminf:CHEMINF_000200 ?inchikeyNode .          # chemical → has-attribute → InChIKey
    ?inchikeyNode a cheminf:CHEMINF_000407 ;              # CHEMINF_000407 = InChIKey class
                  cheminf:SIO_000300 ?inchikey .          # SIO_000300 = has-value
  }

  # ---------- spoke-okn ----------
  SERVICE <https://apps.okn.us/spoke-okn/sparql> {
    ?compound a biolink:ChemicalEntity ;
              oboInOwl:hasDbXref ?xref .                  # SPOKE chemical xref carries InChIKey
    FILTER( CONTAINS(STR(?xref), ?inchikey) )             # join on InChIKey string

    # reified TREATS edge (CtD) carries clinical-trial Phase
    ?stmt rdf:subject   ?compound ;
          rdf:predicate spoke:TREATS_CtD ;
          rdf:object    ?disease ;
          spoke:phase   ?phase .
    ?disease rdfs:label ?diseaseLabel .
  }
}
LIMIT 100
```

**Caveats / mappings needed.** (a) SPOKE's `hasDbXref` mixes namespaces; the `CONTAINS` filter is robust but slow — pre-filter with `STRSTARTS(STR(?xref), "InChIKey:")` if available. (b) For ChEBI as a fallback bridge, swap the InChIKey block for `?compound rdfs:seeAlso ?chebiURI` and join `?chebiURI` to AOP-Wiki's `cheminf:CHEMINF_000409` instances. (c) No `owl:sameAs` is required since the InChIKey hash is itself canonical.

---

### 🥈 Opportunity #2 — Spaceflight differential expression vs Earth disease differential expression

**Scientific question.** *"For genes that the EBI Gene Expression Atlas reports as differentially expressed in a human disease (e.g., breast cancer), are the same genes (or their model-organism orthologs) also differentially expressed in NASA spaceflight assays — and in which tissues?"*

**Bridge.** NCBI_Gene (URI in spoke-genelab; literal in gene-atlas) plus UBERON for tissue alignment. Gene-atlas exposes both Ensembl and NCBI gene IDs as literals on the Gene node.

```sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX gl:      <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX gxa:     <https://spoke.ucsf.edu/genelab/>
PREFIX obo:     <http://purl.obolibrary.org/obo/>

# Seed: a human disease URI (e.g. breast carcinoma MONDO_0007254 or EFO term)
SELECT ?humanGene ?ncbiId ?diseaseLabel ?gxaLog2fc ?gxaP
       ?spaceAssayLabel ?orthologGene ?tissueLabel ?spaceLog2fc ?spaceAdjP
WHERE {
  # ---------- gene-expression-atlas-okn: human disease → DE genes ----------
  SERVICE <https://apps.okn.us/gene-expression-atlas-okn/sparql> {
    ?study  biolink:studies      <DISEASE_URI> ;          # e.g. obo:MONDO_0007254
            biolink:has_output   ?assay .
    <DISEASE_URI> rdfs:label ?diseaseLabel .
    ?assoc  a biolink:GeneExpressionMixin ;
            biolink:subject ?assay ;
            biolink:object  ?humanGene ;
            gxa:p_value     ?gxaP ;
            gxa:effect_size ?gxaLog2fc .
    ?humanGene gxa:ncbi_gene_id ?ncbiId .                 # bridge key (literal)
    FILTER ( ?gxaP < 0.01 )
  }

  # ---------- spoke-genelab: model-organism gene → human ortholog ----------
  SERVICE <https://apps.okn.us/spoke-genelab/sparql> {
    # Build URI from the NCBI gene literal returned above
    BIND( IRI(CONCAT("https://www.ncbi.nlm.nih.gov/gene/", ?ncbiId)) AS ?humanGeneURI )
    ?modelGene gl:IS_ORTHOLOG_MGiG ?humanGeneURI .        # model→human ortholog edge
    ?orthologGene gl:IS_ORTHOLOG_MGiG ?humanGeneURI .

    # Reified differential-expression measurement
    ?stmt rdf:subject   ?spaceAssay ;
          rdf:predicate gl:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG ;
          rdf:object    ?modelGene ;
          gl:log2fc     ?spaceLog2fc ;
          gl:adj_p_value ?spaceAdjP .
    ?spaceAssay rdfs:label ?spaceAssayLabel ;
                gl:INVESTIGATED_ASiA ?tissue .            # UBERON anatomy
    ?tissue rdfs:label ?tissueLabel .
    FILTER ( ?spaceAdjP < 0.05 )
  }
}
ORDER BY ?humanGene ?spaceAdjP
LIMIT 200
```

**Caveats / mappings needed.** (a) `IS_ORTHOLOG_MGiG` is a non-reified predicate, but `MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG` *is* reified — the template above uses `rdf:subject/predicate/object` correctly. (b) `ncbi_gene_id` in gene-atlas is a literal; spoke-genelab uses the NCBI URI form `https://www.ncbi.nlm.nih.gov/gene/<id>` as the actual node URI, so the `BIND(IRI(CONCAT(...)))` step is required. (c) `<DISEASE_URI>` is the seed — replace with the OBO URI (auto-expand_descendants in the `query` tool will pick up MONDO subclasses automatically). (d) For richer tissue alignment, also join the gene-atlas Assay's UBERON term (look up via `gxa:term_id`) to the spoke-genelab `?tissue`.

---

### 🥉 Opportunity #3 — Drug → gene → disease network enriched by tissue-specific expression

**Scientific question.** *"For a SPOKE drug that treats a given disease and modulates a given gene, is that gene actually expressed (and at what magnitude) in the tissue most commonly affected by the disease — i.e., is there an expression-level rationale for the drug-gene-disease triangle?"*

**Bridge.** Ensembl on Gene (high-confidence URI-clean join).

```sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX spoke:   <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX gxa:     <https://spoke.ucsf.edu/genelab/>

# Seed: a disease URI in spoke-okn (DOID); replace <DISEASE_URI>
SELECT ?drugLabel ?geneLabel ?ensembl
       ?gxaStudyTitle ?tissue ?gxaLog2fc ?gxaP
WHERE {
  # ---------- spoke-okn: drug TREATS disease and Up/Down-regulates gene ----------
  SERVICE <https://apps.okn.us/spoke-okn/sparql> {
    ?treatStmt rdf:subject   ?drug ;
               rdf:predicate spoke:TREATS_CtD ;
               rdf:object    <DISEASE_URI> ;
               spoke:phase   ?phase .
    ?drug a biolink:ChemicalEntity ;
          rdfs:label ?drugLabel .

    # Drug → gene (either upregulates or downregulates)
    { ?drug spoke:UPREGULATES_CuG  ?gene . }
    UNION
    { ?drug spoke:DOWNREGULATES_CdG ?gene . }
    ?gene a biolink:Gene ;
          rdfs:label ?geneLabel ;
          spoke:ensembl ?ensembl .                        # bridge key
    FILTER ( ?phase >= 3 )                                # late-stage drugs only
  }

  # ---------- gene-expression-atlas-okn: tissue expression for that Ensembl gene ----------
  SERVICE <https://apps.okn.us/gene-expression-atlas-okn/sparql> {
    ?gxaGene gxa:ensembl_id ?ensembl .                    # join on Ensembl literal
    ?assoc a biolink:GeneExpressionMixin ;
           biolink:subject ?assay ;
           biolink:object  ?gxaGene ;
           gxa:effect_size ?gxaLog2fc ;
           gxa:p_value     ?gxaP .
    ?study biolink:has_output ?assay ;
           gxa:project_title  ?gxaStudyTitle .
    ?assay biolink:has_input ?gxaDisease .
    OPTIONAL { ?assay rdfs:label ?tissue . }
    FILTER ( ?gxaP < 0.05 )
    FILTER ( ABS(?gxaLog2fc) > 1.0 )
  }
}
ORDER BY DESC(ABS(?gxaLog2fc))
LIMIT 100
```

**Caveats / mappings needed.** (a) `spoke:ensembl` is a node-property (literal) on Gene, and `gxa:ensembl_id` is also a literal — the join is a plain string match; no `owl:sameAs` is required. (b) Both literals are typically the bare `ENSGxxxxxxx` ID without an IRI prefix; verify casing. (c) `<DISEASE_URI>` should be a `DOID` URI for spoke-okn — for cross-graph use, look it up via Ubergraph (`lookup_uri` tool) by label. (d) Phase ≥ 3 filter optional but useful to limit to clinically-validated drugs. (e) If you need the gene-atlas disease too, join `?gxaDisease` (which carries an EFO/MONDO URI) back to the SPOKE disease via `mesh_list` or via Ubergraph cross-walks.

---

## 6. Gap Report (Step 6) — thematic siblings without a clean ID bridge

| Gap | Graphs | Thematic overlap | Missing identifier / mapping | Suggested intermediary |
|---|---|---|---|---|
| **G1** | spoke-okn ↔ oard-kg | Disease centric; both rich in disease–entity assoc | spoke-okn uses **DOID**, oard-kg uses **MONDO** — no overlap in registry | **biobricks-mesh** as MeSH hub plus Ubergraph: `lookup_uri` → `mondo:exactMatch doid:`. SPOKE Disease nodes carry a `mesh_list` literal that biobricks-mesh resolves; oard-kg can be reached via MONDO↔MeSH cross-walks in MeSH RDF |
| **G2** | spoke-okn ↔ biohealth | Both Disease + SDoH; massive thematic overlap | spoke-okn = DOID + MeSH list; biohealth = MONDO + MeSH + UMLS | **biobricks-mesh** is the natural bridge — spoke-okn's `spoke:mesh_list` literal is split and joined to biohealth's MeSH-keyed disease nodes |
| **G3** | spoke-okn ↔ biomarkerkg | Disease–gene/biomarker | DOID vs MONDO + HPO | Bridge through Ubergraph (`mondo:exactMatch doid:` triples) or through gene-atlas-okn for the gene side |
| **G4** | biobricks-aopwiki ↔ biohealth | Toxicology adverse outcomes are diseases | aopwiki Disease/Disorder uses NCIT (`Thesaurus.owl#C54571`); biohealth uses MONDO/MeSH | NCIT↔MONDO mapping exists in OLS / Ubergraph but not directly in any current Proto-OKN graph |
| **G5** | spoke-genelab ↔ pankgraph | Both have differential gene measures, both list NCBI_Gene | Tool returns `can_join: false` despite shared registry namespace — likely URI-vs-literal storage mismatch | Use **gene-expression-atlas-okn** as the bridge graph; it stores both NCBI and Ensembl as literals per gene |
| **G6** | nde ↔ spoke-okn / pankgraph / prokn | Datasets about diseases/pathogens; underlying graphs *describe* the same diseases | nde uses Schema.org `healthCondition` and `infectiousAgent` as DefinedTerms — typically MeSH or NCBI Taxonomy strings; bio graphs use MONDO/DOID | A **MeSH cross-walk through biobricks-mesh** plus a NCBI Taxonomy cross-walk would let you link NIAID datasets to in-graph mechanistic evidence |
| **G7** | prokn ↔ spoke-okn | Both have proteins/genes and chemicals | prokn primary key = UniProt; spoke-okn = Ensembl (gene-level) | Need UniProt↔Ensembl mapping. **gene-expression-atlas-okn** (Ensembl) plus a UniProt cross-reference table (or external SPARQL service to UniProt's RDF) would bridge |
| **G8** | ncipidkg ↔ spoke-okn | NCI-PID pathways = cancer biology; SPOKE has cancer-relevant gene-disease + drug-gene | ncipidkg proteins are URIs in NCI-PID space (no Ensembl/UniProt declared); spoke-okn genes are Ensembl-keyed | Same UniProt↔Ensembl cross-walk problem as G7. Could also approach via **prokn** (UniProt) → ncipidkg (protein URI) if those happen to overlap |
| **G9** | biobricks-ice ↔ biohealth | Both speak to disease via biological targets / clinical context | ice has UMLS as a *predicate value* but UMLS is not in ice's declared identifier_namespaces; biohealth has UMLS namespace | Possibly bridgeable on UMLS CUIs if ice's `UMLS Concept` predicate values are in the same form. Worth a small probe query before relying on it |
| **G10** | ruralkg ↔ biohealth / oard-kg | Rural mental-health / substance abuse vs SDoH-disease evidence | ruralkg uses FIPS/RUCC only — no biomedical IDs | **spoke-okn is the natural pivot** (FIPS for ruralkg, MeSH/MONDO indirectly for biohealth/oard-kg via further bridging) |

### Common bridging recommendation

**`biobricks-mesh` is the single most valuable vocabulary hub** for closing biomedical gaps in this collection. It contains the full MeSH tree as RDF and is referenced (as a literal `mesh_list`) by spoke-okn, by SDoH labels in biohealth, and indirectly by NIAID's `healthCondition` strings. A small set of `skos:exactMatch` overlay triples connecting MeSH ↔ MONDO ↔ DOID (sourced from Ubergraph) would unlock ~6 of the 10 gaps above.

**Secondary recommendation:** use **`gene-expression-atlas-okn` as a gene-ID cross-walk hub** — it stores both Ensembl and NCBI gene IDs as literals on every Gene node. The `get_join_strategy` tool already recognises this for the spoke-genelab ↔ spoke-okn pair (B7), and the same pattern applies to pankgraph and biobricks-ice.

---

### Notes on tool behaviour

A handful of `get_join_strategy` calls returned `can_join: false` for graph pairs that share namespaces in the registry (e.g., oard-kg ↔ biohealth on MONDO/UMLS; pankgraph ↔ spoke-okn on Ensembl). The tool appears to require not just shared *namespaces* but a tighter alignment of how the namespace is realised in each graph (URI form vs literal vs db-xref). For a complete picture, registry-level overlap should be treated as the upper bound and `get_join_strategy` as the lower bound; the bridges flagged ⚠️ in §3 are worth a fast probe query (e.g., `SELECT … FROM <graph> { ?s ?p ?o . FILTER STRSTARTS(STR(?o),"http://purl.obolibrary.org/obo/MONDO_") }`) before committing them to a federated workflow.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-06*

Model: claude-opus-4-7
