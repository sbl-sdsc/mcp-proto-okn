# Spaceflight Gene Expression Analysis: From Mouse to Human Orthologs and Disease Associations

**Chat Transcript**  
*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on 2025-12-16*

---

## 👤 **User**

@spoke-genelab: describe the properties and relationships of the Assay entity

---

## 🧠 **Assistant**

Based on the SPOKE GeneLab knowledge graph schema and data, here's a comprehensive description of the **Assay** entity:

### **Definition**
The Assay entity (URI: `http://purl.obolibrary.org/obo/OBI_0000070`) represents a unique identifier for an assay instance in NASA's Open Science Data Repository (OSDR). Each assay corresponds to experimental measurements performed on biological samples from spaceflight experiments.

### **Properties**

The Assay entity has the following data properties:

1. **Experimental Factors:**
   - `factor_space_1` - Primary experimental grouping (e.g., "Space Flight")
   - `factor_space_2` - Secondary experimental grouping (e.g., "Ground Control", "Basal Control", "Vivarium Control")
   - `factors_1` - Array of primary experimental factors/independent variables
   - `factors_2` - Array of secondary experimental factors for comparative analysis

2. **Material/Sample Information:**
   - `material_1` - Biological material analyzed in first assay group (e.g., "left eye", tissue, cell type, organ)
   - `material_2` - Biological material analyzed in second assay group
   - `material_id_1` - Controlled ontology identifier for first material (e.g., UBERON code)
   - `material_id_2` - Controlled ontology identifier for second material
   - `material_name_1` - Preferred ontology-based name for first material
   - `material_name_2` - Preferred ontology-based name for second material

3. **Assay Methodology:**
   - `measurement` - Type of data produced (e.g., transcription profiling, DNA methylation profiling)
   - `technology` - Platform or method used (e.g., "RNA-Sequencing (RNA-Seq)", "DNA microarray", specific sequencing platforms like "Illumina HiSeq 4000")

### **Relationships**

The Assay entity connects to other entities through these relationships:

1. **INVESTIGATED_ASiA** - Links to **Anatomy** entities
   - Indicates which anatomical entities (UBERON ontology) were examined in the assay

2. **INVESTIGATED_ASiCT** - Links to **CellType** entities
   - Indicates which cell types (Cell Ontology) were examined in the assay

3. **MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG** - Links to **Gene** entities
   - Records differential expression measurements of model organism genes
   - This relationship has additional properties:
     - `log2fc` - Log2-transformed fold change in gene expression
     - `adj_p_value` - Multiple testing-corrected p-value for statistical significance

4. **MEASURED_DIFFERENTIAL_METHYLATION_ASmMR** - Links to **MethylationRegion** entities
   - Records differential methylation measurements in genomic regions
   - This relationship has properties like:
     - `methylation_diff` - Percent change in methylation
     - `q_value` - Adjusted p-value for false discovery rate control

5. **PERFORMED_SpAS** (inverse) - Connected from **Study** entities
   - Indicates which Study performed this assay

### **Example Usage**

A typical Assay instance might be:
- **Label**: `OSD-100_transcription-profiling_rna-sequencing-(rna-seq)`
- **Technology**: RNA-Sequencing
- **Materials**: Left eye tissue (UBERON ontology)
- **Comparison**: Space Flight vs. Ground Control
- **Measurements**: Differential expression of hundreds/thousands of genes with associated log2 fold changes and adjusted p-values

This structure enables the SPOKE GeneLab knowledge graph to systematically capture experimental results from spaceflight biology experiments and link them to broader biological knowledge through gene orthologs, anatomical structures, and cellular contexts.

---

## 👤 **User**

For the example assay, return the top 10 differentially expressed genes with abs(log2fc) > 1 and adj_p_values < 0.05.

---

## 🧠 **Assistant**

Here are the **top 10 differentially expressed genes** from the example assay (OSD-100 transcription profiling RNA-Seq) with |log2fc| > 1 and adj_p_value < 0.05:

### Top 10 Differentially Expressed Genes in Assay OSD-100

**Assay Details:** Left eye tissue, Space Flight vs. Ground Control comparison in *Mus musculus* (mouse)

| Rank | Gene Symbol | Gene Name | log2FC | Adj P-value | Direction |
|------|-------------|-----------|---------|-------------|-----------|
| 1 | **Apol9b** | apolipoprotein L 9b | +1.83 | 0.011 | Up-regulated |
| 2 | **Apol9a** | apolipoprotein L 9a | +1.79 | 0.0022 | Up-regulated |
| 3 | **Oas2** | 2'-5' oligoadenylate synthetase 2 | +1.74 | 0.0016 | Up-regulated |
| 4 | **Oas3** | 2'-5' oligoadenylate synthetase 3 | +1.56 | 0.0058 | Up-regulated |
| 5 | **Sst** | somatostatin | +1.52 | 2.3×10⁻⁶ | Up-regulated |
| 6 | **Oas1a** | 2'-5' oligoadenylate synthetase 1A | +1.52 | 0.00061 | Up-regulated |
| 7 | **Fbp2** | fructose bisphosphatase 2 | -1.30 | 0.039 | Down-regulated |
| 8 | **Spink7** | serine peptidase inhibitor, Kazal type 7 | +1.26 | 0.012 | Up-regulated |
| 9 | **Pln** | phospholamban | -1.16 | 0.0026 | Down-regulated |
| 10 | **Colq** | collagen-like tail subunit of acetylcholinesterase | -1.15 | 0.039 | Down-regulated |

### Key Observations:

- **7 genes up-regulated** and **3 genes down-regulated** in spaceflight conditions
- Strong immune/defense response signature (OAS family genes, APOL genes)
- The **OAS (oligoadenylate synthetase)** genes are particularly notable - these are involved in antiviral immune responses
- **Sst (somatostatin)** shows the most statistically significant change (p = 2.3×10⁻⁶)
- All genes are from *Mus musculus* (mouse) and have human orthologs in the knowledge graph

---

## 👤 **User**

Map the mouse genes to the human orthologs

---

## 🧠 **Assistant**

### Mouse to Human Ortholog Mapping for Top Differentially Expressed Genes

**From Assay OSD-100** (Left eye, Space Flight vs. Ground Control)

| Rank | Mouse Gene | Mouse Gene Name | log2FC | Adj P-value | Human Ortholog(s) | Human Gene Name |
|------|------------|-----------------|--------|-------------|-------------------|-----------------|
| 1 | **Apol9b** | apolipoprotein L 9b | +1.83 | 0.011 | **APOL1, APOL2, APOL3, APOL4** | apolipoprotein L family (1-4) |
| 2 | **Apol9a** | apolipoprotein L 9a | +1.79 | 0.0022 | **APOL1, APOL2, APOL3, APOL4** | apolipoprotein L family (1-4) |
| 3 | **Oas2** | 2'-5' oligoadenylate synthetase 2 | +1.74 | 0.0016 | **OAS2** | 2'-5'-oligoadenylate synthetase 2 |
| 4 | **Oas3** | 2'-5' oligoadenylate synthetase 3 | +1.56 | 0.0058 | **OAS3** | 2'-5'-oligoadenylate synthetase 3 |
| 5 | **Sst** | somatostatin | +1.52 | 2.3×10⁻⁶ | **SST** | somatostatin |
| 6 | **Oas1a** | 2'-5' oligoadenylate synthetase 1A | +1.52 | 0.00061 | **OAS1** | 2'-5'-oligoadenylate synthetase 1 |
| 7 | **Fbp2** | fructose bisphosphatase 2 | -1.30 | 0.039 | **FBP2** | fructose-bisphosphatase 2 |
| 8 | **Spink7** | serine peptidase inhibitor, Kazal type 7 | +1.26 | 0.012 | **SPINK7** | serine peptidase inhibitor Kazal type 7 |
| 9 | **Pln** | phospholamban | -1.16 | 0.0026 | **PLN** | phospholamban |
| 10 | **Colq** | collagen-like tail subunit | -1.15 | 0.039 | **COLQ** | collagen like tail subunit |
| 11 | **R3hdml** | R3H domain containing-like | -1.14 | 0.0020 | **R3HDML** | R3H domain containing like |
| 12 | **Sftpd** | surfactant associated protein D | -1.09 | 0.018 | **SFTPD** | surfactant protein D |
| 13 | **Upb1** | ureidopropionase, beta | -1.04 | 0.0029 | **UPB1** | beta-ureidopropionase 1 |
| 14 | **Sln** | sarcolipin | -1.02 | 0.027 | **SLN** | sarcolipin |

### Key Findings:

1. **Many-to-Many Mapping**: The mouse **Apol9a** and **Apol9b** genes map to **four human APOL genes** (APOL1-4), reflecting gene family expansion differences between species.

2. **One-to-One Conservation**: Most genes show direct 1:1 orthology:
   - OAS family genes (OAS1, OAS2, OAS3) - highly conserved antiviral response genes
   - SST (somatostatin) - neuroendocrine signaling
   - Metabolic enzymes (FBP2, UPB1)
   - Cardiac/muscle proteins (PLN, SLN)

3. **Functional Categories**:
   - **Up-regulated in spaceflight**: Immune/antiviral (OAS genes, APOL genes), neuropeptide (SST)
   - **Down-regulated in spaceflight**: Metabolism (FBP2), muscle function (PLN, SLN), surfactant protein (SFTPD)

4. **Clinical Relevance**: Several human orthologs have known disease associations:
   - **APOL1**: Kidney disease susceptibility
   - **OAS genes**: Antiviral immunity, interferon response
   - **PLN**: Cardiomyopathy mutations

This mapping enables translation of spaceflight biology findings from mouse models to potential human health implications.

---

## 👤 **User**

@spoke-okn: are there any diseases related to these human genes?

---

## 🧠 **Assistant**

### Disease Associations for Human Genes from Spaceflight Study

Based on the SPOKE-OKN knowledge graph, here are the diseases associated with the human ortholog genes identified in the spaceflight differential expression analysis:

#### **Immune/Antiviral Response Genes**

**OAS1** (2'-5'-oligoadenylate synthetase 1) - *Up-regulated in spaceflight*
- **COVID-19** - Antiviral response
- **Viral infectious disease** - Innate immunity
- **Diabetes mellitus** - Metabolic disease
- **Hypertension** - Cardiovascular disease

**OAS2** (2'-5'-oligoadenylate synthetase 2) - *Up-regulated in spaceflight*
- **Viral infectious disease** - Antiviral defense

**OAS3** (2'-5'-oligoadenylate synthetase 3) - *Up-regulated in spaceflight*
- **Hypertension** - Cardiovascular disease

#### **Apolipoprotein Genes**

**APOL1** (apolipoprotein L1) - *Up-regulated in spaceflight*
- **Chronic kidney disease** - Major renal disease risk factor
- **Glomerulonephritis** - Kidney inflammation
- **Sleeping sickness** (African trypanosomiasis) - Protective against parasitic infection

**APOL2** (apolipoprotein L2) - *Up-regulated in spaceflight*
- **Schizophrenia** ([OMIM: 181500](https://omim.org/entry/181500))

**APOL4** (apolipoprotein L4) - *Up-regulated in spaceflight*
- **Schizophrenia** ([OMIM: 181500](https://omim.org/entry/181500))

#### **Cardiac/Muscle Genes**

**PLN** (phospholamban) - *Down-regulated in spaceflight*
- **Cardiomyopathy** - Heart muscle disease (PLN mutations are well-known causes of dilated and hypertrophic cardiomyopathy)

**SLN** (sarcolipin) - *Down-regulated in spaceflight*
- No disease associations found in SPOKE-OKN

#### **Respiratory/Pulmonary Genes**

**SFTPD** (surfactant protein D) - *Down-regulated in spaceflight*
- **Chronic obstructive pulmonary disease (COPD)** ([OMIM: 606963](https://omim.org/entry/606963))
- **COVID-19** - Respiratory infection susceptibility
- **Rheumatoid arthritis** ([OMIM: 180300](https://omim.org/entry/180300))

#### **Neurological/Metabolic Genes**

**SST** (somatostatin) - *Up-regulated in spaceflight*
- **Diabetes mellitus** - Glucose regulation
- **Nervous system disease** - Neuroendocrine function

**FBP2** (fructose-bisphosphatase 2) - *Down-regulated in spaceflight*
- **Epilepsy** - Neurological disorder
- **Nervous system disease** - Metabolic-neurological link

**UPB1** (beta-ureidopropionase 1) - *Down-regulated in spaceflight*
- **Acne** ([OMIM: 604324](https://omim.org/entry/604324))
- **Epilepsy** - Neurological disorder

**COLQ** (collagen-like tail subunit) - *Down-regulated in spaceflight*
- **Nervous system disease** - Neuromuscular junction disorders

#### **Clinical Implications for Spaceflight**

1. **Cardiovascular Risk**: Down-regulation of PLN (associated with cardiomyopathy) suggests potential cardiac remodeling concerns during spaceflight.

2. **Immune Activation**: Strong up-regulation of OAS genes (antiviral immunity) indicates heightened immune surveillance, potentially related to:
   - Viral reactivation in spaceflight (known phenomenon)
   - Stress-induced immune changes

3. **Kidney Disease Risk**: APOL1 up-regulation is particularly notable given its strong association with chronic kidney disease - relevant for long-duration missions.

4. **Respiratory Vulnerability**: SFTPD down-regulation could indicate compromised pulmonary surfactant function and increased respiratory infection susceptibility.

5. **Metabolic-Neurological Changes**: Multiple genes link to both metabolic and neurological diseases, suggesting systemic stress responses.

---

## 👤 **User**

Create a volcano diagram for the genes in this assay

---

## 🧠 **Assistant**

![Volcano Plot: OSD-100 Assay](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/volcano_plot_OSD100.png)

### Volcano Plot Analysis

**Statistical Overview:**
- **Total genes analyzed:** 191
- **Up-regulated genes (red):** 7 genes with log2FC > 1 and adj.p < 0.05
- **Down-regulated genes (blue):** 8 genes with log2FC < -1 and adj.p < 0.05  
- **Not significant (gray):** 176 genes

**Key Features:**

1. **Axes:**
   - X-axis: log₂(Fold Change) - magnitude of gene expression change
   - Y-axis: -log₁₀(Adjusted P-value) - statistical significance

2. **Significance Thresholds:**
   - Vertical dashed lines at log2FC = ±1 (2-fold change)
   - Horizontal dashed line at -log₁₀(0.05) ≈ 1.3 (p-value threshold)

3. **Top Differentially Expressed Genes (labeled):**
   
   **Up-regulated (right side):**
   - **Sst** (somatostatin) - Most statistically significant
   - **Oas1a, Oas2, Oas3** - Antiviral response genes cluster
   - **Apol9a, Apol9b** - Apolipoprotein genes
   - **Spink7** - Serine peptidase inhibitor
   
   **Down-regulated (left side):**
   - **Pln** (phospholamban) - Cardiac calcium regulation
   - **R3hdml** - RNA binding protein
   - **Upb1** - Beta-ureidopropionase

4. **Biological Interpretation:**
   - Clear immune response activation pattern (upper right quadrant)
   - Metabolic and cardiac gene suppression (left side)
   - Most genes show modest changes (central gray cluster)
   - OAS gene family shows coordinated up-regulation

The volcano plot visually confirms the immune activation and metabolic suppression patterns observed in spaceflight conditions, with the antiviral OAS genes showing both high statistical significance and substantial fold changes.

---

*Generated using SPOKE GeneLab and SPOKE-OKN knowledge graphs*  
*Analysis Date: December 16, 2025*
