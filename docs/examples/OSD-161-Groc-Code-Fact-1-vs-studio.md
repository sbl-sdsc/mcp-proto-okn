## Chat Transcript
SPOKE GeneLab Spaceflight Analysis

👤 **User**  
Objective: Integrate GeneLab, SPOKE, and PubMed knowledge to characterize spaceflight-associated gene expression changes and their disease relevance.

@spoke-genelab
    1.    Retrieve study OSD-161 and summarize its experimental design (organism, mission, spaceflight vs. ground control).
    2.    List all assays associated with this study.
    3.    Extract the unique experimental factors across these assays (e.g., tissue, timepoint, platform).
    4.   Compare assay for spaceflight vs. ground control and return:
    •    Top 5 up-regulated genes
    •    Top 5 down-regulated genes
(include log fold change and adjusted p-value if available).
    5.    Map the resulting genes to their human orthologs
@spoke-okn
    6.   Map the human orthologs to associated diseases, indicating:
    •    Disease name
    •    Evidence type or source KG
    •    Number of supporting associations (if available).

Output format:
    •    Tables for assays, factors, gene lists, ortholog mappings, and disease associations
    •    A short narrative summary synthesizing biological and translational relevance

@spoke-genelab
   7. Create chat  transcript

---

🧠 **Assistant**  
### Study Summary
**Study OSD-161**: Rodent Research 3 (RR3), a spaceflight study conducted on missions SpaceX-8 (April 8 - May 11, 2016) and SpaceX-9 (July 18 - August 26, 2016) on the International Space Station. Organism: Rattus norvegicus (rats). Experimental design compares spaceflight vs. ground control conditions.

### Assays Table
| Assay ID | Factors 1 | Factors 2 | Material 1 | Material 2 | Technology | Measurement |
|----------|-----------|-----------|------------|------------|------------|-------------|
| OSD-161-18173e633772afbf947c2983352631b7 | Ground Control | Basal Control | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |
| OSD-161-26eaa8ce4a2f160a40fc459e1e2f1025 | Space Flight | Ground Control | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |
| OSD-161-2b7b773a167357b887a23caa67396da0 | Basal Control | Space Flight | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |
| OSD-161-707d5b3290fb1a3fe65101a6ad204184 | Space Flight | Basal Control | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |
| OSD-161-ab5155c2e9a78b47872d367fa8371808 | Ground Control | Space Flight | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |
| OSD-161-d57b39077cb0bacc4f2b603c23812f2f | Basal Control | Ground Control | Adrenal gland | Adrenal gland | RNA Sequencing (RNA-Seq) | transcription profiling |

### Experimental Factors
- Tissue: Adrenal gland
- Timepoint: Not specified
- Platform: RNA Sequencing (RNA-Seq)
- Conditions: Space Flight, Ground Control, Basal Control

### Gene Lists (Spaceflight vs. Ground Control)
**Top 5 Up-regulated Genes** (log2fc > 0, adj_p < 0.05):
| Gene ID | Symbol | Log2FC | Adj P-value |
|---------|--------|--------|-------------|
| 14281 | - | 1.95698 | 0.0243974 |
| 12227 | - | 1.36758 | 1.51299e-08 |
| 654820 | - | 0.965693 | 0.0495984 |
| 17684 | - | 0.917106 | 2.14688e-05 |
| 19252 | - | 0.757843 | 0.0170623 |

**Top 5 Down-regulated Genes** (log2fc < 0, adj_p < 0.05):
| Gene ID | Symbol | Log2FC | Adj P-value |
|---------|--------|--------|-------------|
| 110557 | - | -1.39209 | 0.0244232 |
| 15018 | - | -1.37279 | 0.0445936 |
| 110558 | - | -1.37279 | 0.0445936 |
| 14415 | - | -1.16381 | 0.0458033 |
| 12517 | - | -0.878764 | 0.0371471 |

### Ortholog Mappings
| Rat Gene ID | Human Gene ID | Human Symbol |
|-------------|---------------|--------------|
| 14281 | 2353 | FOS |
| 12227 | 7832 | BTG2 |
| 654820 | - | - |
| 17684 | 10370 | - |
| 19252 | 1843 | DUSP1 |
| 110557 | 3105,3106,3107,3133,3134,3135,3136 | HLA-A,B,C,E,F,G |
| 15018 | 3105,3106,3107,3133,3134,3135,3136 | HLA-A,B,C,E,F,G |
| 110558 | 3105,3106,3107,3133,3134,3135,3136 | HLA-A,B,C,E,F,G |
| 14415 | 2571 | GAD1 |
| 12517 | 971 | CD72 |

### Disease Associations
| Human Gene | Disease Name | Evidence Type/Source KG | Number of Supporting Associations |
|------------|--------------|--------------------------|-----------------------------------|
| 2353 (FOS) | inflammatory bowel disease | SPOKE-OKN KG | 1 |
| 2353 (FOS) | cardiomyopathy | SPOKE-OKN KG | 1 |
| 2353 (FOS) | polycystic ovary syndrome | SPOKE-OKN KG | 1 |
| 2353 (FOS) | depressive disorder | SPOKE-OKN KG | 1 |
| 2353 (FOS) | anxiety disorder | SPOKE-OKN KG | 1 |
| 2353 (FOS) | liver disease | SPOKE-OKN KG | 1 |
| 2353 (FOS) | nervous system disease | SPOKE-OKN KG | 1 |
| 2353 (FOS) | diabetes mellitus | SPOKE-OKN KG | 1 |
| 7832 (BTG2) | - | - | 0 |
| 10370 | - | - | 0 |
| 1843 (DUSP1) | - | - | 0 |
| 3105 (HLA-A) | rheumatoid arthritis | SPOKE-OKN KG | 1 |
| 3105 (HLA-A) | nervous system disease | SPOKE-OKN KG | 1 |
| 3105 (HLA-A) | viral infectious disease | SPOKE-OKN KG | 1 |
| 3105 (HLA-A) | alopecia areata | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | inflammatory bowel disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | cardiomyopathy | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | endocarditis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | hypertension | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | major depressive disorder | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | depressive disorder | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | epilepsy | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | dermatitis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | asthma | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | skin benign neoplasm | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | bipolar disorder | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | liver disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | pancreatitis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | human immunodeficiency virus infectious disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | migraine | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | rheumatoid arthritis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | gastroesophageal reflux disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | nervous system disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | psoriasis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | viral infectious disease | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | meningitis | SPOKE-OKN KG | 1 |
| 3106 (HLA-B) | encephalitis | SPOKE-OKN KG | 1 |
| 3107 (HLA-C) | dermatitis | SPOKE-OKN KG | 1 |
| 3107 (HLA-C) | psoriasis | SPOKE-OKN KG | 1 |
| 3107 (HLA-C) | alopecia areata | SPOKE-OKN KG | 1 |
| 3134 (HLA-F) | multiple sclerosis | SPOKE-OKN KG | 1 |
| 3135 (HLA-G) | asthma | SPOKE-OKN KG | 1 |
| 3135 (HLA-G) | rheumatoid arthritis | SPOKE-OKN KG | 1 |
| 2571 (GAD1) | autism spectrum disorder | SPOKE-OKN KG | 1 |
| 2571 (GAD1) | depressive disorder | SPOKE-OKN KG | 1 |
| 2571 (GAD1) | epilepsy | SPOKE-OKN KG | 1 |
| 2571 (GAD1) | schizophrenia | SPOKE-OKN KG | 1 |
| 2571 (GAD1) | nervous system disease | SPOKE-OKN KG | 1 |
| 971 (CD72) | - | - | 0 |

### Narrative Summary
Spaceflight exposure in rats induces significant transcriptional changes in the adrenal gland, with up-regulation of genes like FOS (involved in stress response) and down-regulation of HLA genes (immune-related). Human orthologs link to diseases including inflammatory bowel disease, cardiomyopathy, rheumatoid arthritis, and neurological disorders like epilepsy and schizophrenia. This suggests spaceflight may exacerbate immune and neurological vulnerabilities, with translational relevance for astronaut health and terrestrial disease models. Integration with SPOKE-OKN highlights potential disease connections via gene associations, warranting further validation.

Chat transcript created at ~/Downloads/spoke-genelab-spaceflight-analysis-2026-01-05.md.

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 on 2026-01-05*

Grok Code Fast 1