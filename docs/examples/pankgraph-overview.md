# PanKgraph Knowledge Graph Exploration

👤 **User**
Give an overview of the @pankgraph KG

---

🧠 **Assistant**

Here's an overview of the **PanKgraph** knowledge graph:

**What it is:** PanKgraph is the knowledge graph component of [PanKbase](https://pankbase.org/), a centralized, open-source research hub for the human pancreas and type 1 diabetes (T1D), funded by the NSF and developed at the University of Michigan. It was built to connect previously fragmented biomedical data using large language models and diverse data types.

**Core focus:** The graph centers on mechanisms of diabetes pathogenesis — specifically how genes, genetic variants (SNPs/SNVs), regulatory regions, and expression data interact in pancreatic tissue.

**Scale:** The graph contains roughly 1.6M+ triples, with the most populous entity types being:
- ~1.4M RDF statements (reified edges carrying rich metadata)
- ~79K genes (Biolink-aligned)
- ~19K SNPs and SNVs
- ~18K open chromatin regions (OCRs)
- ~17K Gene Ontology terms
- ~957 scientific articles
- A small set of cell types, cell lines, and diseases (including T1D itself)

*(Interactive entity-relationship diagram rendered in chat)*

**Entity model (14 classes, 117 predicates):** The graph is aligned to the [Biolink Model](https://biolink.github.io/biolink-model/) and key ontologies, covering:

- **Genomic variation:** SNPs and SNVs (dbSNP, Sequence Ontology)
- **Regulatory genomics:** Open chromatin regions (OCRs) with Gene Activity Scores computed for T1D, non-diabetic, and AAB-positive donors
- **Gene expression:** eQTL evidence, slope, p-values, fine-mapping (PIP, LBF, credible sets)
- **Gene function:** GO term annotations, gene-gene interactions (BioGRID)
- **Literature:** PubMed-linked articles with provenance on associations
- **Omics metadata:** Datasets with tissue, donor, and version metadata

**Identifier namespaces:** Ensembl, NCBI Gene, HGNC, dbSNP, GO, PubMed, GEO, BioSample, and a PanKbase-native namespace.

**Key use cases:**
- Connecting T1D GWAS variants → eQTLs → pancreatic gene expression
- Exploring open chromatin accessibility differences between T1D and non-diabetic donors
- Tracing gene-condition associations with publication provenance
- Multi-omics integration across genomics, epigenomics, and transcriptomics

The SPARQL endpoint is at `https://apps.okn.us/pankgraph/sparql`.

---

👤 **User**
Visualize the schema using the visualize_schema tool

---

🧠 **Assistant**

Here's the cleaned PanKgraph schema diagram:

```mermaid
classDiagram
direction TB

class Gene {
    string gene_name
    string chr
    int start_loc
    int end_loc
    string strand
    float GC_percentage
    string gencode_annotation
    string id_version
    float All_expression_mean
    float All_expression_median
    float NonDiabetic_expression_mean
    float T1D_expression_mean
    string tissue_id
    string tissue_name
    float purity
}

class SNP {
    string chr
    int start_loc
    int end_loc
    string effect_allele
    string other_allele
    float pip
    float lbf
    string credible_set
    float slope
    float nominal_p
    int n_snp
}

class SNV {
    string chr
    int start_loc
    int end_loc
    float Log2FoldChange
    float SE_of_Log2FoldChange
    float Adjusted_P_value
    float P_value
    float slope
    float pip
    float lbf
    string credible_set
    string effect_allele
    string other_allele
}

class OpenChromatinRegion {
    string chr
    int start_loc
    int end_loc
    float OCR_GeneActivityScore_mean
    float OCR_GeneActivityScore_median
    float T1D_OCR_GeneActivityScore_mean
    float T1D_OCR_GeneActivityScore_median
    float NonDiabetic_OCR_GeneActivityScore_mean
    float NonDiabetic_OCR_GeneActivityScore_median
    float AABpos_OCR_GeneActivityScore_mean
    float AABpos_OCR_GeneActivityScore_median
    float T2D_OCR_GeneActivityScore_mean
    float T2D_OCR_GeneActivityScore_median
}

class Article {
    string title
    string abstract
    string author
    string pmcid
    string pubmedid
    string pubdate
    string publication_source
}

class Disease

class T1D

class Cell

class CellLine

class OntologyClass {
    string synonym
    string directly_related_term
    string type
}

class GeneOntologyTerm

class Dataset {
    string title
    string version
    string data_source_url
    string data_version
    string consortium
}

class Statement {
    uri subject
    uri predicate
    uri object
}

Gene --> Gene : interacts_with
Gene --> Cell : expressed_in
Gene --> Disease : gene_associated_with_condition
Gene --> OntologyClass : functional_association
SNV --> Gene : affects_expression_of
SNP --> T1D : associated_with
OpenChromatinRegion --> Cell : located_in
OntologyClass --> OntologyClass : related_to
T1D --|> Disease : subClassOf
GeneOntologyTerm --|> OntologyClass : subClassOf
```

A few things worth noting about the schema:

- **No edge properties** — all 117 predicates are node-level annotations rather than reified edge attributes, meaning metadata like `pip`, `slope`, and expression quantiles live directly on nodes, not on relationship edges.
- **`OpenChromatinRegion`** is the most property-rich class, carrying per-donor-group gene activity scores across four conditions (all donors, non-diabetic, T1D, T2D, and AAB-positive).
- **`SNP` vs `SNV`** are distinct classes: SNPs carry fine-mapping statistics (PIP, LBF, credible sets) and link to T1D; SNVs carry differential expression stats (log2FC, adjusted p-values) and link to genes via `affects_expression_of`.
- **`Statement`** (RDF reification) acts as the provenance backbone — capturing the subject/predicate/object of any asserted triple to enable evidence tracking across 1.4M annotated relationships.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-01*

*Model: claude-sonnet-4-6 (claude-sonnet-4-20250514)*
