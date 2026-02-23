# Integrated Multi-KG Analysis: Genetic Parts Discovery for Terpene Biomanufacturing

*Corresponding to the hypothetical WOBD scenario — executed across 6 Proto-OKN knowledge graphs, Open Targets, FRINK analysis tools, and PubMed*

**Date:** 2026-02-23
**Analysis Platform:** Proto-OKN / FRINK federated knowledge graphs

---

## 1. Analysis Architecture

We queried **6 knowledge graphs** and **3 analytical tools** to mirror the three-layer WOBD scenario:

| Layer | WOBD Equivalent | Proto-OKN Resource Used |
|---|---|---|
| **Gene-function network** | Enzyme discovery for terpene biosynthesis | **SPOKE-OKN** (gene-compound-disease), **Wikidata** (GO annotations), **AOP-Wiki** (adverse outcome pathways) |
| **Expression data** | RNA-seq/proteomics under fermentation conditions | **Gene Expression Atlas OKN** (200 differential expression assays), **SPOKE-GeneLab** (spaceflight transcriptomics) |
| **Metadata / datasets** | Experimental datasets supporting relationships | **NDE** (NIAID Data Ecosystem — 50 datasets), **g:Profiler enrichment** (84 enriched terms) |

---

## 2. Layer 1 — Terpene Biosynthesis Gene Network (SPOKE-OKN + Wikidata)

### 2a. Core Mevalonate (MVA) Pathway Genes Resolved

All 12 key MVA pathway enzymes were resolved to Ensembl IDs via Open Targets:

| Gene | Ensembl ID | Enzyme | Pathway Step |
|---|---|---|---|
| **ACAT2** | ENSG00000120437 | Acetoacetyl-CoA thiolase | Acetyl-CoA → Acetoacetyl-CoA |
| **HMGCS1** | ENSG00000112972 | HMG-CoA synthase | Acetoacetyl-CoA → HMG-CoA |
| **HMGCR** | ENSG00000113161 | HMG-CoA reductase | HMG-CoA → Mevalonate (**rate-limiting**) |
| **MVK** | ENSG00000110921 | Mevalonate kinase | Mevalonate → Mevalonate-5P |
| **PMVK** | ENSG00000163344 | Phosphomevalonate kinase | Mevalonate-5P → Mevalonate-5PP |
| **MVD** | ENSG00000167508 | Mevalonate decarboxylase | Mevalonate-5PP → IPP |
| **IDI1** | ENSG00000067064 | IPP isomerase | IPP ↔ DMAPP |
| **FDPS** | ENSG00000160752 | FPP synthase | IPP + DMAPP → FPP |
| **GGPS1** | ENSG00000152904 | GGPP synthase | FPP → GGPP |
| **FDFT1** | ENSG00000079459 | Squalene synthase | FPP → Squalene (sterol branch) |
| **SQLE** | ENSG00000104549 | Squalene epoxidase | Squalene → Squalene oxide |
| **DHDDS** | ENSG00000117682 | Dehydrodolichyl diphosphate synthase | Long-chain prenyl synthesis |

### 2b. Gene-Compound Regulatory Network (SPOKE-OKN neighborhood)

Querying the **HMGCR** neighborhood in SPOKE-OKN revealed compound-gene regulatory edges critical for strain engineering:

| Compound | Regulation of HMGCR | Relevance |
|---|---|---|
| **Hexachlorophene** | ↑ Upregulates | Chemical inducer of mevalonate flux |
| **Pentobarbital** | ↑ Upregulates | Metabolic modulator |
| **Thiabendazole** | ↑ Upregulates | Antifungal — potential cross-pathway activator |
| **Fluorouracil** | ↓ Downregulates | Pyrimidine analog — suppresses pathway |

### 2c. Disease Associations (SPOKE-OKN)

HMGCR is associated with 9 diseases in SPOKE-OKN, including **arteriosclerosis**, **coronary artery disease**, **diabetes mellitus**, **obesity**, and **liver disease** — confirming its centrality in lipid metabolism and validating pathway target selection.

### 2d. Cross-Species Orthologs (SPOKE-GeneLab + Wikidata)

- **HMGCR** has orthologs in mouse (NCBI Gene 15357) and rat (NCBI Gene 25675) via SPOKE-GeneLab
- **FDPS** has an ortholog **ERG20** in *S. cerevisiae* (Wikidata), the key farnesyl pyrophosphate synthase in yeast — a critical target for microbial chassis engineering
- Wikidata confirms HMGCR participates in **isoprenoid biosynthetic process** and **ubiquinone metabolic process**

### 2e. Adverse Outcome Pathways (AOP-Wiki)

HMGCR appears in **AOP 124** via Key Event 2269 (KE 2269) and Key Event Relationship 3367 — establishing a toxicology framework for pathway perturbation. This is directly relevant to assessing safety windows when overexpressing mevalonate pathway enzymes.

---

## 3. Layer 2 — Differential Expression Data (Gene Expression Atlas OKN)

The Gene Expression Atlas OKN returned **200 assay-gene associations** across the mevalonate pathway genes. Key findings organized by biological context:

### 3a. Statin Treatment Studies (Direct Mevalonate Pathway Perturbation)

The most represented study category — **"Atorvastatin, rosuvastatin and rifampicin effect on human primary hepatocyte transcriptome"** — returned differential expression for:
- **HMGCR** (multiple dose/time conditions)
- **FDPS** (multiple dose/time conditions)
- **FDFT1** (multiple dose/time conditions)
- **PMVK** (compound treatment)

This is the gold-standard dataset for understanding pathway feedback regulation — statins inhibit HMGCR, triggering SREBP-mediated upregulation of the entire pathway.

### 3b. Cancer Biology Studies (Pathway Dysregulation)
- **Mutant p53 disrupts mammary acinar morphogenesis via the mevalonate pathway** → HMGCR expression data
- **MCF-7 breast cancer cells with estradiol** → FDPS, FDFT1 expression
- **Leukemia progenitor compartments** → FDPS differential expression

### 3c. Metabolic Condition Studies
- **White-to-brown adipocyte conversion** → HMGCR expression (JAK inhibition)
- **Leucine-devoid medium** (nutrient stress) → HMGCR, FDPS, FDFT1
- **Idiopathic pulmonary fibrosis** → HMGCR, FDPS
- **Simvastatin-treated monocytes** → HMGCR, FDPS (anti-inflammatory context)

### 3d. Summary Gene Hit Counts (Expression Atlas)

| Gene | # Assay Associations | Top Experimental Factors |
|---|---|---|
| **HMGCR** | ~50 | Compound, dose, time, genotype, disease |
| **FDPS** | ~40 | Compound, dose, time, disease |
| **FDFT1** | ~60 | Compound, treatment, growth condition |
| **PMVK** | ~8 | Growth condition, disease, clinical |
| **SQLE** | ~3 | Treatment, phenotype |

---

## 4. Layer 3 — Experimental Dataset Discovery (NDE)

The NDE metadata graph returned **50 datasets** directly relevant to terpene biomanufacturing. We grouped them into actionable categories:

### 4a. Microbial Isoprenoid Engineering (Most Directly Relevant)

| Dataset | Organism | Key Finding |
|---|---|---|
| **GSE102672** — IPP toxicity in isoprenoid-producing *E. coli* | *E. coli* | IPP accumulation causes growth inhibition; proteomics identified PMK reduction as recovery mechanism |
| **GSE125123** — Oxygen exposure in *Z. mobilis*: implications for isoprenoid production | *Z. mobilis* | O₂ induces bottleneck in MEP pathway via Fe-S cluster damage; suf operon upregulation resolves it |
| **GSE108411** — spt15_A101T mutant (MVA pathway flux increasing) | *S. cerevisiae* | Global transcription machinery engineering (gTME) mutant increasing mevalonate pathway flux |
| **GSE136169** — Mevalonate bypass in malaria parasites | *P. falciparum* | Engineered mevalonate-dependent pathway in apicoplast-negative parasites |
| **GSE131722** — Mevalonate pathway deficient *S. aureus* | *S. aureus* | Reversion mechanisms from mevalonate auxotrophy |
| **GSE12984** — Mevalonate pathway inhibitors in yeast | *S. cerevisiae* | Lovastatin vs. zaragozic acid → opposite effects on FPP, identifying FPP-responsive genes |
| **GSE13424** — Mevalonate pathway downregulation in *S. aureus* | *S. aureus* | Microarray profiling of controlled pathway suppression; virulence factor upregulation |
| **GSE127536** — *R. toruloides* D-galacturonic acid metabolism | *R. toruloides* | Promising lipid/terpene host with broad substrate utilization |

### 4b. Plant Terpene Biosynthesis (Gene Parts Discovery)

| Dataset | Plant System | Terpene Target |
|---|---|---|
| **GSE102404** — *Artemisia argyi* transcriptome | *A. argyi* | HMGR, MVD, DXS, DXR, HDS, HDR identified for terpenoid synthesis |
| **GSE130386** — Muscat grape terpene biosynthesis | *V. vinifera* | Monoterpene pathway gene profiling |
| **GSE121523/GSE121831** — Taxol biosynthesis in Taxus | *Taxus* spp. | Diterpenoid (taxol) pathway gene expression |
| **GSE133168** — Slash pine resin tapping | *P. elliottii* | Commercial resinosis transcriptome (monoterpene/diterpene) |
| **GSE135444** — Dendrobine biosynthesis in *Dendrobium* | *D. nobile* | miRNAs controlling terpenoid backbone (AACT, MK, DXR, HDS) |

### 4c. Mevalonate Pathway in Disease Contexts (Translational Insights)

| Dataset | Context | Insight for Engineering |
|---|---|---|
| **GSE121558** — p53 represses mevalonate pathway | Hepatocellular carcinoma | ABCA1/SREBP2 regulatory axis controls pathway activity |
| **GSE124189** — Mevalonate pathway and pyrimidine synthesis | Colon cancer | Pathway required for ubiquinone → essential for TCA/respiration |
| **GSE132055** — Mevalonate in anti-HER2 resistance | Breast cancer | Restored MVA activity in resistant cells; FPP/GGPP rescue |
| **GSE135301** — Mevalonate and protein geranylgeranylation | Thymocyte biology | GGPP branch critical for protein prenylation |
| **GSE111853** — Cardiac organoids: mevalonate and proliferation | Cardiac | Mevalonate pathway required for cardiomyocyte proliferation |

---

## 5. Pathway Enrichment Analysis (g:Profiler)

The 25-gene mevalonate/cholesterol pathway gene set returned **84 significantly enriched terms** across four databases:

### 5a. KEGG Pathways

| KEGG Pathway | p-value | Genes | Recall |
|---|---|---|---|
| **Terpenoid backbone biosynthesis** | 8.9 × 10⁻²⁸ | 13/22 | 59% |
| **Steroid biosynthesis** | 1.5 × 10⁻²⁵ | 12/20 | 60% |
| **Metabolic pathways** | 1.8 × 10⁻¹⁵ | 24/1537 | — |
| **Butanoate metabolism** | 6.4 × 10⁻⁵ | 4/27 | 15% |
| **Valine/leucine/isoleucine degradation** | 6.9 × 10⁻⁴ | 4/48 | 8% |

### 5b. Reactome Pathways

| Reactome Pathway | p-value | Key Insight |
|---|---|---|
| **Cholesterol biosynthesis** | 2.1 × 10⁻⁵⁴ | 21/26 genes (81% of pathway) |
| **Activation by SREBF (SREBP)** | 8.4 × 10⁻²⁷ | 14/40 genes — master transcriptional regulator |
| **Regulation of cholesterol biosynthesis by SREBP** | 8.6 × 10⁻²⁵ | Confirms SREBP2 as the regulatory switch |
| **Synthesis of dolichyl-phosphate** | 0.027 | MVD, DHDDS — dolichol branch |
| **Synthesis of Ketone Bodies** | 0.050 | HMGCS2, ACAT1 — alternative carbon fate |

### 5c. GO Biological Process (Key Terms)

| GO Term | p-value | Genes |
|---|---|---|
| **Isoprenoid biosynthetic process** | 4.9 × 10⁻²⁶ | 12 genes |
| **Isopentenyl diphosphate biosynthetic process** | 2.7 × 10⁻¹² | MVK, PMVK, MVD, IDI1, IDI2 |
| **IPP biosynthesis, mevalonate pathway** | 2.6 × 10⁻⁶ | MVK, PMVK, MVD (100% recall) |
| **Terpenoid biosynthetic process** | 1.2 × 10⁻⁸ | HMGCS1/2, FDPS, GGPS1, LSS |
| **Farnesyl diphosphate biosynthetic process** | 2.7 × 10⁻⁹ | HMGCS1/2, FDPS, GGPS1 |
| **Dimethylallyl diphosphate biosynthesis** | 0.002 | IDI1, IDI2 |
| **Geranyl diphosphate biosynthesis** | 0.002 | FDPS, GGPS1 |

### 5d. GO Molecular Function (Enzyme Activities)

| Activity | Genes | Relevance |
|---|---|---|
| **Prenyl diphosphate synthase** | FDPS, GGPS1, FDFT1, DHDDS | Core terpene chain elongation |
| **HMG-CoA synthase activity** | HMGCS1, HMGCS2 | Pathway entry |
| **IPP delta-isomerase activity** | IDI1, IDI2 | IPP/DMAPP equilibrium |
| **FPP synthase activity** | FDPS, GGPS1 | Branch point to sesqui/diterpenes |
| **GGPP synthase activity** | GGPS1, FDFT1 | Diterpene precursor |

---

## 6. Key Engineering Recommendations

Based on this integrated multi-KG analysis:

### Priority Gene Parts for Microbial Terpene Chassis

1. **HMGCR** — Rate-limiting step; extensive expression data across 50+ conditions confirms tight SREBP2 regulation. Engineering strategies: feedback-resistant variants, codon-optimized heterologous expression
2. **FDPS** — Critical branch point (FPP → sesquiterpenes vs. GGPP); yeast ortholog ERG20 confirmed via Wikidata; expression modulated by statins, estradiol, growth conditions
3. **IDI1/IDI2** — IPP/DMAPP isomerization; 100% recall in GO enrichment; balancing this equilibrium is essential for terpene backbone extension
4. **MVK → PMVK → MVD** — The "lower mevalonate pathway" operates as a unit; GSE102672 shows PMK reduction as a natural IPP toxicity relief mechanism in *E. coli*
5. **GGPS1** — For diterpene production; expression in GeneLab spaceflight studies suggests environmental responsiveness

### Critical Engineering Considerations from KG Data

- **IPP toxicity** (GSE102672): Elevated IPP causes growth inhibition — balance flux with downstream consumption
- **Fe-S cluster vulnerability** (GSE125123): MEP pathway enzymes are O₂-sensitive — relevant for aerobic fermentation
- **SREBP2 feedback** (Reactome enrichment): The native mammalian regulatory circuit will attempt to downregulate overexpressed pathway genes — consider feedback-insensitive variants
- **Protein prenylation drain** (GSE135301): GGPP is consumed by protein geranylgeranylation — competing sink to manage
- **AOP 124** (AOP-Wiki): HMGCR perturbation has documented adverse outcome pathways — safety context for pathway modulation

---

## 7. Knowledge Graphs Queried — Summary

| Graph | Query Type | Result |
|---|---|---|
| **SPOKE-OKN** | Gene neighborhoods, compound-gene regulation | 15 entities for HMGCR including 9 diseases, 4 regulatory compounds |
| **Gene Expression Atlas OKN** | Differential expression for pathway genes | 200 assay-gene associations across HMGCR, FDPS, FDFT1, PMVK, SQLE |
| **NDE** | Dataset metadata search | 50 datasets spanning microbial engineering, plant terpenoids, pathway pharmacology |
| **SPOKE-GeneLab** | Cross-species orthologs, spaceflight expression | 15 entities for HMGCR; 10+ NASA OSDR assays |
| **AOP-Wiki** | Toxicology pathways | AOP 124 linked to HMGCR (KE 2269, KER 3367) |
| **Wikidata** | GO annotations, orthologs | FDPS→ERG20 ortholog; isoprenoid process annotations |
| **g:Profiler** | Pathway enrichment | 84 enriched terms; KEGG Terpenoid backbone (p=8.9×10⁻²⁸) |
| **Open Targets** | Gene ID resolution | 12/12 pathway genes resolved to Ensembl IDs |

---

*This analysis demonstrates how a federated query across Proto-OKN knowledge graphs can recapitulate and extend the WOBD scenario — surfacing gene-function relationships, linking them to experimental expression datasets, and providing the metadata context (organisms, technologies, experimental conditions) needed to prioritize genetic parts for terpene biomanufacturing.*
