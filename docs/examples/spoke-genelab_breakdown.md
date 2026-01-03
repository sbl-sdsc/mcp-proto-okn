# Chat Transcript: SPOKE GeneLab Missions, Studies, and Technologies Breakdown

👤 **User**  
Give a breakdown of missions, studies, and the type of technologies used in the studies in @spoke-genelab

---

🧠 **Assistant**  
I'll help you explore the missions, studies, and technologies in the spoke-genelab knowledge graph. Let me start by getting the description and schema to understand what data is available.

**SPOKE GeneLab Knowledge Graph Description:**

The spoke-genelab KG complements the spoke-okn (SPOKE Open Knowledge Network) KG and is designed to integrate omics data from NASA's Open Science Data Repository (OSDR/GeneLab), which hosts results from spaceflight experiments. 

The current release includes transcriptional profiling (RNA-Seq, DNA microarray) and epigenomic profiling (DNA methylation) data from model organisms flown in space or maintained as ground controls. Differential expression and methylation signatures are pre-computed to facilitate comparisons between spaceflight and control conditions. Genes from model organisms are systematically mapped to their human orthologs, which allows integration with SPOKE's rich network of human biology, including pathways, phenotypes, and therapeutic targets. Cell and tissue types are mapped to the Cell (CL) and Uber Anatomy Ontology (UBERON) ontology, respectively.

---

## Breakdown of the SPOKE GeneLab Knowledge Graph

The **SPOKE GeneLab knowledge graph** integrates omics data from NASA's Open Science Data Repository (OSDR/GeneLab), focusing on spaceflight experiments and their biological effects. Here's a comprehensive breakdown:

### **Overview Statistics**
- **23 Missions** spanning from 1991 to 2021
- **140 Studies** (81 spaceflight, 52 ground studies, 4 high altitude studies)
- **6,467 Assays** across multiple biological samples
- **59,756 Genes** from three model organisms mapped to human orthologs

---

### **Missions**

The knowledge graph includes data from 23 space missions:

**Mission Programs:**
- **NASA missions** (majority): Space Shuttle missions (STS-40, STS-58, STS-131, STS-135) and ISS missions via SpaceX (SpaceX-4 through SpaceX-21)
- **International collaborations**: ESA, JAXA, Italian Space Agency (ASI)
- **Timeline**: From June 1991 (STS-40) to January 2021 (SpaceX-21)

**Notable missions by study count:**
- SpaceX-4 (Sept-Oct 2014): 13 studies
- SpaceX-12 (Aug-Sept 2017): 8 studies
- SpaceX-8 (Apr-May 2016): 8 studies

---

### **Study Types**

**Distribution by Type:**
- **Spaceflight Studies**: 81 studies (57.9%)
- **Ground Studies**: 52 studies (37.1%) - control experiments
- **High Altitude Studies**: 4 studies (2.9%)

**Top Studies by Assays:**
1. **OSD-455** (Ground Study): 650 assays
2. **Rodent Research-8** (OSD-379, Spaceflight): 480 assays
3. **Rodent Research-7** (OSD-253, Spaceflight): 364 assays
4. **P21/CDKN1a Pathway Study** (OSD-462, Spaceflight): 216 assays - investigating bone tissue regenerative arrest in microgravity

---

### **Technologies Used**

The knowledge graph contains data from three main omics technologies:

#### **1. RNA Sequencing (RNA-Seq)**
- **4,512 assays** (69.8% of all assays)
- Used for transcription profiling
- Measures differential gene expression
- **Edge properties**: `log2fc` (fold change) and `adj_p_value` (statistical significance)

#### **2. DNA Microarray**
- **1,944 assays** (30.0% of all assays)
- Used for transcription profiling
- Older technology for measuring gene expression

#### **3. Whole Genome Bisulfite Sequencing**
- **11 assays** (0.2% of all assays)
- Used for DNA methylation profiling
- Measures epigenetic modifications
- **Edge properties**: `methylation_diff` (percent change) and `q_value` (adjusted p-value)

---

### **Measurement Types**

- **Transcription profiling**: 6,456 assays (99.8%)
- **DNA methylation profiling**: 11 assays (0.2%)

---

### **Biological Samples Investigated**

**Top tissues/materials examined (by assay count):**
1. **Cell** (generic): 968 assays
2. **Liver left lateral lobe**: 764 assays
3. **Whole blood**: 708 assays
4. **Left kidney**: 608 assays
5. **Liver**: 467 assays
6. **Spleen**: 400 assays
7. **Skin**: 340 assays
8. **Mammary gland**: 194 assays
9. **Quadriceps femoris** (muscle): 177 assays
10. **Soleus** (muscle): 144 assays
11. **Retina**: 142 assays
12. **Thymus**: 140 assays

This demonstrates a focus on multiple organ systems including metabolic organs (liver, kidney), immune system (spleen, thymus, blood), musculoskeletal system, and specialized tissues.

---

### **Model Organisms**

The knowledge graph includes genes from three organisms, all mapped to human orthologs:

- **Human** (*Homo sapiens*): 27,740 genes
- **Mouse** (*Mus musculus*): 26,444 genes
- **Rat** (*Rattus norvegicus*): 4,465 genes

This cross-species mapping enables integration with the broader SPOKE network of human biology, pathways, phenotypes, and therapeutic targets.

---

### **Key Relationships and Data**

The knowledge graph captures:
- **Differential gene expression** from spaceflight vs. ground control conditions
- **Differential methylation** patterns in specific genomic regions
- **Gene-to-methylation region mappings** with genomic location details (chromosome, start/end positions, promoter/exon/intron locations)
- **Orthology relationships** between model organism genes and human genes

This rich dataset enables researchers to understand how spaceflight affects molecular biology across multiple tissues, organisms, and regulatory mechanisms.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 on 2026-01-03*

Model: claude-sonnet-4-20250514
