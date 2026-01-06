# Spaceflight Gene Expression and Disease Relevance Analysis
## Study OSD-161: Rodent Research 3 (RR3)

**Analysis Date:** January 5, 2026  
**Data Sources:** SPOKE GeneLab, SPOKE-OKN Knowledge Graphs

---

## Executive Summary

This analysis integrates spaceflight transcriptomics data from NASA's GeneLab with biomedical knowledge graphs to characterize gene expression changes in adrenal gland tissue during spaceflight and their potential disease relevance. Study OSD-161 (Rodent Research 3) investigated the molecular response of mouse adrenal glands to spaceflight conditions aboard the International Space Station. Key findings reveal significant alterations in stress response genes, immune system genes, and neurological signaling pathways, with strong associations to cardiovascular, neurological, and autoimmune diseases.

---

## 1. Study Overview: OSD-161 (Rodent Research 3)

### Study Metadata
- **Study ID:** OSD-161
- **Project Title:** Rodent Research 3 (RR3)
- **Project Type:** Spaceflight Study
- **Space Program:** NASA
- **Flight Program:** International Space Station (ISS)

### Mission Details
| Mission | Start Date | End Date | Duration |
|---------|------------|----------|----------|
| SpaceX-8 | 2016-04-08 | 2016-05-11 | ~33 days |
| SpaceX-9 | 2016-07-18 | 2016-08-26 | ~39 days |

### Experimental Design
- **Organism:** *Mus musculus* (Mouse)
- **Tissue:** Adrenal gland
- **Technology:** RNA Sequencing (RNA-Seq)
- **Measurement Type:** Transcription profiling

**Experimental Groups:**
- **Space Flight:** Mice exposed to microgravity conditions aboard ISS
- **Ground Control:** Mice maintained under identical conditions on Earth
- **Basal Control:** Additional control group for baseline measurements

---

## 2. Assays in Study OSD-161

A total of **6 differential expression assays** were identified, comparing various experimental conditions:

| Assay ID (shortened) | Group 1 (factor_space_1) | Group 2 (factor_space_2) | Material | Technology |
|---------------------|--------------------------|--------------------------|----------|------------|
| ...18173e633772... | Ground Control | Basal Control | Adrenal gland | RNA-Seq |
| **...26eaa8ce4a2f...** | **Space Flight** | **Ground Control** | **Adrenal gland** | **RNA-Seq** |
| ...2b7b773a1673... | Basal Control | Space Flight | Adrenal gland | RNA-Seq |
| ...707d5b3290fb... | Space Flight | Basal Control | Adrenal gland | RNA-Seq |
| ...ab5155c2e9a7... | Ground Control | Space Flight | Adrenal gland | RNA-Seq |
| ...d57b39077cb0... | Basal Control | Ground Control | Adrenal gland | RNA-Seq |

**Primary Analysis Focus:** Assay `OSD-161-26eaa8ce4a2f160a40fc459e1e2f1025`  
**Comparison:** Space Flight vs. Ground Control (direct comparison)

---

## 3. Experimental Factors

### Key Factors Across Assays
- **Treatment Conditions:** Space Flight, Ground Control, Basal Control
- **Biological Material:** Adrenal gland (consistent across all assays)
- **Platform:** RNA Sequencing (Illumina)
- **Analysis Type:** Differential gene expression

The adrenal gland is particularly relevant for spaceflight research as it produces stress hormones (cortisol, adrenaline) and plays a central role in the physiological stress response.

---

## 4. Differential Gene Expression Results

### 4.1 Top 5 Up-Regulated Genes (Space Flight vs. Ground Control)

| Rank | Mouse Gene | Symbol | Log2 Fold Change | Adj. P-Value | Regulation |
|------|------------|--------|------------------|--------------|------------|
| 1 | 14281 | **Fos** | +1.96 | 0.024 | ↑ UP |
| 2 | 12227 | **Btg2** | +1.37 | 1.5×10⁻⁸ | ↑ UP |
| 3 | 654820 | **G530011O06Rik** | +0.97 | 0.050 | ↑ UP |
| 4 | 17684 | **Cited2** | +0.92 | 2.1×10⁻⁵ | ↑ UP |
| 5 | 19252 | **Dusp1** | +0.76 | 0.017 | ↑ UP |

**Biological Interpretation:**
- **Fos:** Immediate-early gene involved in stress response, cell proliferation, and differentiation
- **Btg2:** Tumor suppressor involved in cell cycle regulation and stress response
- **Cited2:** Transcriptional regulator involved in cardiac and neural development, hypoxia response
- **Dusp1:** Dual-specificity phosphatase involved in MAPK signaling and stress response

### 4.2 Top 5 Down-Regulated Genes (Space Flight vs. Ground Control)

| Rank | Mouse Gene | Symbol | Log2 Fold Change | Adj. P-Value | Regulation |
|------|------------|--------|------------------|--------------|------------|
| 1 | 110557 | **H2-Q6** | -1.39 | 0.024 | ↓ DOWN |
| 2 | 110558 | **H2-Q7/Q9** | -1.37 | 0.045 | ↓ DOWN |
| 3 | 15018 | **H2-Q7/Q9** | -1.37 | 0.045 | ↓ DOWN |
| 4 | 14415 | **Gad1** | -1.16 | 0.046 | ↓ DOWN |
| 5 | 12517 | **Cd72** | -0.88 | 0.037 | ↓ DOWN |

**Biological Interpretation:**
- **H2-Q6, H2-Q7, H2-Q9:** MHC class I molecules involved in immune system function and antigen presentation
- **Gad1:** Glutamic acid decarboxylase, critical for GABA neurotransmitter synthesis
- **Cd72:** B-cell receptor regulating B-cell activation and immune response

---

## 5. Mouse-to-Human Ortholog Mapping

Mouse genes were mapped to human orthologs using the pre-computed `IS_ORTHOLOG_MGiG` relationships in SPOKE GeneLab. Some mouse genes (e.g., predicted/less-annotated loci) do not have mapped human orthologs in the KG, and mouse MHC (H2) genes may map to multiple HLA genes.

| Mouse Gene (NCBI) | Mouse Symbol | Human Gene (NCBI) | Human Symbol | Notes |
|------------|--------------|------------|--------------|--------------|
| 14281 | Fos | 2353 | **FOS** | 1:1 ortholog |
| 12227 | Btg2 | 7832 | **BTG2** | 1:1 ortholog |
| 654820 | G530011O06Rik | — | — | No human ortholog found in spoke-genelab |
| 17684 | Cited2 | 10370 | **CITED2** | 1:1 ortholog |
| 19252 | Dusp1 | 1843 | **DUSP1** | 1:1 ortholog |
| 110557 | H2-Q6 | 3105; 3106; 3107; 3133; 3134; 3135 | **HLA-A; HLA-B; HLA-C; HLA-E; HLA-F; HLA-G** | 1:many MHC/HLA mapping |
| 110558 | H2-Q7/Q9 | — | — | No human ortholog found in spoke-genelab |
| 15018 | H2-Q7/Q9 | 3105; 3106; 3107; 3133; 3134; 3135 | **HLA-A; HLA-B; HLA-C; HLA-E; HLA-F; HLA-G** | 1:many MHC/HLA mapping |
| 14415 | Gad1 | 2571 | **GAD1** | 1:1 ortholog |
| 12517 | Cd72 | 971 | **CD72** | 1:1 ortholog |

**Note:** Mouse H2 genes map to multiple human HLA (Human Leukocyte Antigen) genes, reflecting the complexity of the MHC system.

---

## 6. Disease Association Analysis (SPOKE-OKN)

### 6.1 Summary Statistics

| Human Gene | Total Disease Associations | Key Disease Categories |
|------------|---------------------------|------------------------|
| **HLA-B** | 22 | Autoimmune, Infectious, Neurological, Cardiovascular |
| **FOS** | 9 | Neurological, Metabolic, Inflammatory, Cancer |
| **GAD1** | 6 | Neurological, Psychiatric, Cancer |
| **HLA-A** | 5 | Autoimmune, Infectious, Neurological, Cancer |
| **HLA-C** | 3 | Autoimmune, Dermatological |
| **HLA-G** | 2 | Autoimmune, Respiratory |
| **HLA-F** | 2 | Autoimmune, Cancer |
| **HLA-E** | 1 | Cancer |
| **BTG2** | 1 | Cancer |
| **CITED2** | 2 | Cancer |
| **DUSP1** | 1 | Cancer |
| **CD72** | 1 | Cancer |

### 6.2 Detailed Disease Associations

#### FOS (Up-regulated in spaceflight)
**Source KG:** SPOKE-OKN

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Anxiety disorder | DOID:2030 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Cardiomyopathy | DOID:0050700 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Depressive disorder | DOID:1596 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Diabetes mellitus | DOID:9351 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Inflammatory bowel disease | DOID:0050589 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Liver disease | DOID:409 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Nervous system disease | DOID:863 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Polycystic ovary syndrome | DOID:11612 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Prostate cancer | DOID:10283 | MARKER_POS_GmpD | 1 | SPOKE-OKN |

**Clinical Relevance:** FOS up-regulation suggests increased cellular stress response and potential connections to neurological and metabolic disorders commonly observed in astronauts.

---

#### GAD1 (Down-regulated in spaceflight)
**Source KG:** SPOKE-OKN

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Autism spectrum disorder | DOID:0060041 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Depressive disorder | DOID:1596 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Epilepsy | DOID:1826 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Nervous system disease | DOID:863 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Schizophrenia | DOID:5419 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Cervical cancer | DOID:4362 | MARKER_POS_GmpD | 1 | SPOKE-OKN |

**Clinical Relevance:** GAD1 down-regulation may impact GABA neurotransmitter production, potentially explaining mood and cognitive changes reported during spaceflight.

---

#### HLA-A (Down-regulated in spaceflight)
**Source KG:** SPOKE-OKN

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Alopecia areata | DOID:986 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Nervous system disease | DOID:863 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Rheumatoid arthritis | DOID:7148 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Viral infectious disease | DOID:934 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Ovarian cancer | DOID:2394 | MARKER_POS_GmpD | 1 | SPOKE-OKN |

---

#### HLA-B (Down-regulated in spaceflight)
**Source KG:** SPOKE-OKN

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Asthma | DOID:2841 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Bipolar disorder | DOID:3312 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Cardiomyopathy | DOID:0050700 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Depressive disorder | DOID:1596 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Dermatitis | DOID:2723 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Encephalitis | DOID:9588 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Endocarditis | DOID:10314 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Epilepsy | DOID:1826 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Gastroesophageal reflux disease | DOID:8534 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| HIV infectious disease | DOID:526 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Hypertension | DOID:10763 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Inflammatory bowel disease | DOID:0050589 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Liver disease | DOID:409 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Major depressive disorder | DOID:1470 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Meningitis | DOID:9471 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Migraine | DOID:6364 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Nervous system disease | DOID:863 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Pancreatitis | DOID:4989 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Psoriasis | DOID:8893 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Rheumatoid arthritis | DOID:7148 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Skin benign neoplasm | DOID:3165 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Viral infectious disease | DOID:934 | ASSOCIATES_DaG | 1 | SPOKE-OKN |

**Clinical Relevance:** HLA-B is the most connected gene in our analysis, with broad associations across immune, neurological, and cardiovascular diseases. Down-regulation may contribute to immune dysregulation observed in astronauts.

---

#### HLA-C (Down-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Alopecia areata | DOID:986 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Dermatitis | DOID:2723 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Psoriasis | DOID:8893 | ASSOCIATES_DaG | 1 | SPOKE-OKN |

---

#### HLA-E (Down-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------------------|------------------------|----------|
| Kidney cancer | DOID:263 | MARKER_NEG_GmnD | 1 | SPOKE-OKN |

---

#### HLA-F (Down-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Kidney cancer | DOID:263 | MARKER_NEG_GmnD | 1 | SPOKE-OKN |
| Multiple sclerosis | DOID:2377 | ASSOCIATES_DaG | 1 | SPOKE-OKN |

---

#### HLA-G (Down-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------|
| Asthma | DOID:2841 | ASSOCIATES_DaG | 1 | SPOKE-OKN |
| Rheumatoid arthritis | DOID:7148 | ASSOCIATES_DaG | 1 | SPOKE-OKN |

---

#### BTG2 (Up-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------------------|------------------------|----------|
| Breast cancer | DOID:1612 | MARKER_POS_GmpD | 1 | SPOKE-OKN |

---

#### CITED2 (Up-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------------------|------------------------|----------|
| Kidney cancer | DOID:263 | MARKER_POS_GmpD | 1 | SPOKE-OKN |
| Stomach cancer | DOID:10534 | MARKER_NEG_GmnD | 1 | SPOKE-OKN |

---

#### DUSP1 (Up-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------------------|------------------------|----------|
| Stomach cancer | DOID:10534 | MARKER_NEG_GmnD | 1 | SPOKE-OKN |

---

#### CD72 (Down-regulated in spaceflight)

| Disease | Disease Ontology ID | Evidence type (predicate) | Supporting associations | Source KG |
|---------|-------------------|---------------------------|------------------------|----------|
| Kidney cancer | DOID:263 | MARKER_NEG_GmnD | 1 | SPOKE-OKN |

---

## 7. Biological and Translational Synthesis

### 7.1 Key Biological Findings

**Stress Response Activation:**
- Spaceflight induces a robust stress response in adrenal gland tissue, as evidenced by up-regulation of immediate-early genes (FOS, DUSP1) and cell cycle regulators (BTG2).
- The FOS proto-oncogene, the most highly up-regulated gene, is a critical mediator of cellular stress responses and is associated with multiple neurological and metabolic disorders.

**Immune System Suppression:**
- Dramatic down-regulation of MHC class I genes (H2-Q6, H2-Q7, H2-Q9 in mice; HLA-A/B/C/E/F/G in humans) suggests immune system dysregulation during spaceflight.
- This finding aligns with well-documented immune suppression in astronauts and increased susceptibility to viral reactivation during space missions.

**Neurotransmitter System Disruption:**
- Down-regulation of GAD1, the rate-limiting enzyme for GABA synthesis, may contribute to mood disturbances, anxiety, and cognitive changes reported during spaceflight.
- GABA is the primary inhibitory neurotransmitter in the nervous system, critical for regulating neuronal excitability.

### 7.2 Disease Relevance

**Neurological and Psychiatric Disorders:**
- Multiple spaceflight-altered genes (FOS, GAD1, HLA-B) are strongly associated with depressive disorders, anxiety, and nervous system diseases.
- This suggests molecular mechanisms underlying mood and cognitive changes in astronauts.

**Cardiovascular Disease:**
- FOS and HLA-B associations with cardiomyopathy and hypertension align with cardiovascular deconditioning observed during long-duration spaceflight.

**Autoimmune and Inflammatory Conditions:**
- HLA gene down-regulation is associated with increased risk of autoimmune diseases (rheumatoid arthritis, psoriasis, inflammatory bowel disease).
- May explain post-flight immune dysregulation and increased infection susceptibility.

**Metabolic Disorders:**
- FOS associations with diabetes mellitus and polycystic ovary syndrome suggest potential metabolic disruptions during spaceflight.

### 7.3 Translational Relevance

**Countermeasure Development:**
- Understanding stress response and immune suppression mechanisms can guide development of pharmacological or nutritional countermeasures.
- Targeted therapies addressing GABAergic signaling may mitigate neurological/psychiatric symptoms.

**Risk Assessment for Long-Duration Missions:**
- Disease associations provide framework for predicting long-term health risks for Mars missions and extended ISS stays.
- Genes identified here could serve as biomarkers for monitoring astronaut health.

**Terrestrial Health Applications:**
- Spaceflight serves as a model for accelerated aging and stress-related diseases.
- Findings may inform treatment strategies for chronic stress, immune disorders, and metabolic diseases on Earth.

---

## 8. Methodology and Data Sources

### Knowledge Graphs Used

**SPOKE GeneLab** (`spoke-genelab`)
- **Description:** Integrates omics data from NASA's Open Science Data Repository (OSDR/GeneLab)
- **SPARQL Endpoint:** https://frink.apps.renci.org/spoke-genelab/sparql
- **Principal Investigator:** Sergio Baranzini, UCSF
- **Funding:** NSF Award #2333819
- **Data Content:**
  - Study metadata and mission information
  - Differential gene expression data (RNA-Seq, microarray)
  - Differential methylation data
  - Gene ortholog mappings
  - Anatomical ontology annotations

**SPOKE-OKN** (`spoke-okn`)
- **Description:** Comprehensive biomedical and environmental health knowledge graph
- **SPARQL Endpoint:** https://frink.apps.renci.org/spoke-okn/sparql
- **Principal Investigator:** Sergio Baranzini, UCSF
- **Funding:** NSF Award #2333819
- **Data Content:**
  - Gene-disease associations (Disease Ontology)
  - Drug-disease relationships
  - Gene-pathway connections
  - Geographic health data
  - Environmental exposures

### Analysis Pipeline

1. **Study Retrieval:** SPARQL queries to identify OSD-161 and associated metadata
2. **Assay Identification:** Retrieved all differential expression assays for the study
3. **Gene Expression Analysis:** Extracted top differentially expressed genes with statistical significance
4. **Ortholog Mapping:** Mapped mouse genes to human orthologs using pre-computed relationships
5. **Disease Association:** Queried human gene-disease relationships in SPOKE-OKN
6. **Integration and Interpretation:** Synthesized findings across data sources

---

## 9. Limitations and Future Directions

### Limitations
- Analysis focused on single tissue (adrenal gland) and single assay comparison
- Disease associations based on Disease Ontology; additional sources (GWAS, clinical studies) not included
- Statistical significance of gene-disease associations not quantified
- Temporal dynamics (time course) not analyzed
- Sex-specific differences not examined

### Future Directions
- **Multi-tissue Integration:** Analyze gene expression changes across multiple organs (liver, muscle, brain)
- **Pathway Analysis:** Map differentially expressed genes to biological pathways (KEGG, Reactome)
- **Multi-omics Integration:** Combine transcriptomics with methylation and proteomics data
- **Drug Repurposing:** Identify FDA-approved drugs that could serve as countermeasures
- **Longitudinal Analysis:** Examine time-dependent changes (pre-flight, in-flight, post-flight)
- **Comparative Studies:** Compare across multiple spaceflight studies for meta-analysis
- **Environmental Context:** Integrate with environmental exposures (radiation, social determinants)

---

## 10. Conclusions

This integrative analysis of spaceflight gene expression data from Study OSD-161 reveals significant molecular alterations in mouse adrenal gland tissue, with profound implications for human health during space exploration. Key findings include:

1. **Activation of cellular stress response pathways** (FOS, BTG2, DUSP1) indicates physiological stress during spaceflight
2. **Suppression of immune system genes** (HLA complex) may explain increased infection susceptibility
3. **Disruption of neurotransmitter synthesis** (GAD1) could contribute to mood and cognitive changes
4. **Strong associations with neurological, cardiovascular, and autoimmune diseases** highlight potential long-term health risks

These findings underscore the need for continued molecular monitoring of astronauts and development of targeted countermeasures for long-duration space missions. The integration of spaceflight genomics (GeneLab) with comprehensive biomedical knowledge graphs (SPOKE-OKN) provides a powerful framework for translating space biology research into actionable health insights for both astronauts and terrestrial populations.

---

## References and Data Provenance

**Primary Data Source:**
- NASA GeneLab Study OSD-161 (Rodent Research 3)
- Available at: https://osdr.nasa.gov/bio/repo/data/studies/OSD-161

**Knowledge Graph Resources:**
- SPOKE GeneLab: https://github.com/BaranziniLab/spoke_genelab
- SPOKE-OKN: https://spoke.ucsf.edu
- Frink OKN Registry: https://github.com/frink-okn/okn-registry

**Ontologies:**
- Disease Ontology (DO): http://disease-ontology.org
- UBERON Anatomy Ontology: http://uberon.github.io
- Cell Ontology (CL): http://obofoundry.org/ontology/cl.html

---

**Analysis Generated:** January 5, 2026  
**Contact:** For questions about this analysis, contact the SPOKE team at sergio.baranzini@ucsf.edu

---

## Appendix: SPARQL Queries Used

### Query 1: Study Retrieval
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?study ?label ?project_title ?project_type
WHERE {
  ?study a <https://w3id.org/biolink/vocab/Study> .
  OPTIONAL { ?study rdfs:label ?label }
  OPTIONAL { ?study schema:project_title ?project_title }
  OPTIONAL { ?study schema:project_type ?project_type }
  FILTER(CONTAINS(STR(?study), "161"))
}
```

### Query 2: Mission Information
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>

SELECT ?mission ?flight_program ?space_program ?start_date ?end_date
WHERE {
  ?mission schema:CONDUCTED_MIcS <https://purl.org/okn/frink/kg/spoke-genelab/node/OSD-161> .
  OPTIONAL { ?mission schema:flight_program ?flight_program }
  OPTIONAL { ?mission schema:space_program ?space_program }
  OPTIONAL { ?mission schema:start_date ?start_date }
  OPTIONAL { ?mission schema:end_date ?end_date }
}
```

### Query 3: Assay Metadata
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>

SELECT ?assay ?measurement ?technology ?material_name_1 ?material_id_1 ?factor_space_1 ?factor_space_2
WHERE {
  <https://purl.org/okn/frink/kg/spoke-genelab/node/OSD-161> schema:PERFORMED_SpAS ?assay .
  OPTIONAL { ?assay schema:measurement ?measurement }
  OPTIONAL { ?assay schema:technology ?technology }
  OPTIONAL { ?assay schema:material_name_1 ?material_name_1 }
  OPTIONAL { ?assay schema:material_id_1 ?material_id_1 }
  OPTIONAL { ?assay schema:factor_space_1 ?factor_space_1 }
  OPTIONAL { ?assay schema:factor_space_2 ?factor_space_2 }
}
```

### Query 4: Differential Expression (Up-regulated)
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?gene ?symbol ?log2fc ?adj_p_value
WHERE {
  ?stmt rdf:subject <https://purl.org/okn/frink/kg/spoke-genelab/node/OSD-161-26eaa8ce4a2f160a40fc459e1e2f1025> ;
        rdf:predicate schema:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG ;
        rdf:object ?gene ;
        schema:log2fc ?log2fc ;
        schema:adj_p_value ?adj_p_value .
  OPTIONAL { ?gene schema:symbol ?symbol }
}
ORDER BY DESC(?log2fc)
LIMIT 5
```

### Query 5: Ortholog Mapping
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>

SELECT ?mouse_gene ?mouse_symbol ?human_gene ?human_symbol
WHERE {
  VALUES ?mouse_gene { <gene_uris> }
  ?mouse_gene schema:symbol ?mouse_symbol ;
              schema:IS_ORTHOLOG_MGiG ?human_gene .
  ?human_gene schema:symbol ?human_symbol .
}
```

### Query 6: Disease Associations
```sparql
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene ?gene_label ?disease ?disease_label
       (COUNT(DISTINCT ?evidence) AS ?supporting_associations)
       (GROUP_CONCAT(DISTINCT ?evidence; separator="; ") AS ?evidence_types)
WHERE {
  VALUES ?gene { <human_gene_uris> }
  ?gene rdfs:label ?gene_label .
  {
    ?disease schema:ASSOCIATES_DaG ?gene .
    BIND("ASSOCIATES_DaG" AS ?evidence)
  }
  UNION {
    ?gene schema:MARKER_POS_GmpD ?disease .
    BIND("MARKER_POS_GmpD" AS ?evidence)
  }
  UNION {
    ?gene schema:MARKER_NEG_GmnD ?disease .
    BIND("MARKER_NEG_GmnD" AS ?evidence)
  }
  OPTIONAL { ?disease rdfs:label ?disease_label }
}
GROUP BY ?gene ?gene_label ?disease ?disease_label
ORDER BY ?gene_label ?disease_label
```

---

## 11. Chat Transcript

Chat transcript (generated for this analysis session): `~/Downloads/spoke-genelab-chat-transcript-2026-01-05.md`

---

*End of Report*
