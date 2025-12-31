# SPOKE GeneLab Schema Visualization

👤 **User**  
@spoke-genelab

---

🧠 **Assistant**  
I'll help you explore the spoke-genelab knowledge graph. Let me first get some information about this resource.

Great! I'm now working with the **SPOKE GeneLab** knowledge graph. This is a specialized resource that integrates omics data from NASA's Open Science Data Repository (GeneLab), focusing on spaceflight experiments.

This knowledge graph includes:
- **Transcriptional profiling** data (RNA-Seq, DNA microarray)
- **Epigenomic profiling** data (DNA methylation)
- **Model organisms** flown in space or maintained as ground controls
- Pre-computed **differential expression and methylation signatures**
- **Cross-species mapping** to human orthologs
- Integration with **SPOKE's human biology network** (pathways, phenotypes, therapeutic targets)
- **Cell and tissue type mappings** to standard ontologies (CL and UBERON)

What would you like to explore? I can help you:
- Understand the structure of the data (view the schema)
- Search for specific genes, studies, or experimental conditions
- Analyze differential expression or methylation patterns
- Explore relationships between spaceflight conditions and biological responses
- Compare data across different organisms or tissue types

What are you interested in learning about?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
Let me visualize the SPOKE GeneLab schema for you. I'll start by retrieving the schema information.

Perfect! Now let me create the Mermaid class diagram:

Here's the SPOKE GeneLab schema visualization! The diagram shows:

**Core Entities:**
- **Mission** → **Study** → **Assay**: The organizational hierarchy of spaceflight experiments
- **Gene**: Genetic elements from model organisms, with ortholog mappings to human genes
- **Anatomy** & **CellType**: Biological contexts investigated in assays
- **MethylationRegion**: Genomic regions showing differential methylation

**Key Relationships with Quantitative Data** (shown as intermediary classes):
- **MEASURED_DIFFERENTIAL_EXPRESSION**: Links assays to genes with log2 fold change and adjusted p-values
- **MEASURED_DIFFERENTIAL_METHYLATION**: Links assays to methylation regions with methylation differences and q-values
- **METHYLATED_IN**: Connects genes to methylation regions with detailed genomic location data (chromosome, position, overlap with exons/introns/promoters)

This structure enables powerful queries to explore how spaceflight affects gene expression and DNA methylation across different organisms and tissue types!

```mermaid
classDiagram
direction TB

class Mission {
    date end_date
    string flight_program
    string space_program
    date start_date
}

class Study {
    string project_title
    string project_type
}

class Assay {
    string factor_space_1
    string factor_space_2
    string[] factors_1
    string[] factors_2
    string material_1
    string material_2
    string material_id_1
    string material_id_2
    string material_name_1
    string material_name_2
    string measurement
    string technology
}

class Anatomy

class CellType

class Gene {
    string organism
    string symbol
    string taxonomy
}

class MethylationRegion

class MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG {
    float adj_p_value
    float log2fc
}

class METHYLATED_IN_MGmMR {
    string chromosome
    int dist_to_feature
    int end
    boolean in_exon
    boolean in_intron
    boolean in_promoter
    int start
}

class MEASURED_DIFFERENTIAL_METHYLATION_ASmMR {
    float methylation_diff
    float q_value
}

Mission --> Study : CONDUCTED_MIcS
Study --> Assay : PERFORMED_SpAS
Assay --> Anatomy : INVESTIGATED_ASiA
Assay --> CellType : INVESTIGATED_ASiCT
Gene --> Gene : IS_ORTHOLOG_MGiG
Assay --> MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG
MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG --> Gene
Gene --> METHYLATED_IN_MGmMR
METHYLATED_IN_MGmMR --> MethylationRegion
Assay --> MEASURED_DIFFERENTIAL_METHYLATION_ASmMR
MEASURED_DIFFERENTIAL_METHYLATION_ASmMR --> MethylationRegion
```

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 on 2025-12-31*

Model: claude-sonnet-4-20250514
