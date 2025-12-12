# Chat Transcript: SPOKE-GeneLab Assay Node Analysis

**Date**: December 11, 2025  
**Topic**: Understanding the Assay node structure in the SPOKE-GeneLab knowledge graph  
**User Request**: Describe the Assay node and its properties, with an example comparing ground control vs space flight

---

## User Query

> @spoke-genelab: Describe the Assay node and its properties in @genelab-remote-cypher, and include an example for a ground control vs space flight comparison.

---

## Analysis Process

### Step 1: Schema Discovery

First, I retrieved the complete schema from the SPOKE-GeneLab knowledge graph to understand the data model:

**Classes Found**:
- Assay (OBI_0000070)
- Anatomy (biolink:AnatomicalEntity)
- CellType (biolink:Cell)
- Gene (biolink:Gene)
- Study (biolink:Study)
- MethylationRegion
- Mission

**Key Predicates**:
- PERFORMED_SpAS (Study performs Assay)
- INVESTIGATED_ASiA (Assay investigated Anatomy)
- INVESTIGATED_ASiCT (Assay investigated CellType)
- MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG (Assay measured differential expression)
- MEASURED_DIFFERENTIAL_METHYLATION_ASmMR (Assay measured differential methylation)

### Step 2: Exploring Space Flight Conditions

Queried for distinct factor_space combinations and found 16 different comparison types:

```
Space Flight vs Ground Control
Ground Control vs Space Flight
Space Flight vs Basal Control
Space Flight vs Vivarium Control
(and 12 other combinations)
```

### Step 3: Identifying Example Assay

Found assay: `OSD-100-f1b7f0b93f8d28bc606c5c1127f2d7c9`

**Properties**:
- Measurement: transcription profiling
- Technology: RNA Sequencing (RNA-Seq)
- Tissue: left eye (UBERON:0004548)
- factor_space_1: "Space Flight"
- factor_space_2: "Ground Control"
- Part of Study: OSD-100 (Rodent Research 1)

### Step 4: Extracting Differential Expression Data

Retrieved gene-level differential expression measurements with associated statistics:

**Sample Results**:
| Gene | log2FC | adj_p_value | Direction |
|------|--------|-------------|-----------|
| Isg15 | +0.925 | 0.027 | Up in space |
| R3hdml | -1.143 | 0.002 | Down in space |
| Upb1 | -1.036 | 0.003 | Down in space |
| Tex15 | +0.421 | 0.006 | Up in space |

Total: 206 genes with differential expression measured in this assay

---

## Response Summary

# The Assay Node in SPOKE-GeneLab Knowledge Graph

## Overview

The **Assay** node (class URI: `http://purl.obolibrary.org/obo/OBI_0000070`) represents a unique assay instance from NASA's Open Science Data Repository (OSDR). Assays capture the experimental measurements and analyses performed on biological samples, comparing different experimental conditions such as Space Flight versus Ground Control.

## Key Properties

### Experimental Design Properties

- **measurement**: Type of data produced (e.g., "transcription profiling")
- **technology**: Platform or method used (e.g., "RNA Sequencing (RNA-Seq)")
- **organism**: Scientific organism name (stored separately on Study node, but assays examine specific organisms)

### Space Flight Comparison Properties

- **factor_space_1**: Primary experimental grouping - indicates whether samples were exposed to:
  - "Space Flight"
  - "Ground Control"
  - "Basal Control"
  - "Vivarium Control"

- **factor_space_2**: Secondary experimental grouping for comparison (same options as factor_space_1)

- **factors_1** / **factors_2**: Arrays of additional experimental factors beyond space conditions (e.g., dose, time point, sex, strain)

### Biological Material Properties

- **material_1** / **material_2**: Biological material analyzed in each group (e.g., "left eye", "liver", "muscle")
- **material_name_1** / **material_name_2**: Preferred ontology-based names
- **material_id_1** / **material_id_2**: Controlled ontology identifiers (e.g., UBERON codes)

## Relationships

### Connections to Other Nodes

1. **PERFORMED_SpAS**: Study → Assay (a Study performs an Assay)
2. **INVESTIGATED_ASiA**: Assay → Anatomy (Assay investigated anatomical entity)
3. **INVESTIGATED_ASiCT**: Assay → CellType (Assay investigated cell type)
4. **MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG**: Assay → Gene (Assay measured differential expression of model organism gene)
5. **MEASURED_DIFFERENTIAL_METHYLATION_ASmMR**: Assay → MethylationRegion (Assay measured differential methylation)

### Gene Expression Edge Properties

When an Assay measures differential gene expression, the relationship includes:

- **log2fc**: Log2-transformed fold change in gene expression (positive = up-regulation, negative = down-regulation)
- **adj_p_value**: Multiple testing-corrected p-value (FDR-adjusted, smaller values indicate statistical significance)

## Example: Ground Control vs Space Flight Comparison

### Study Context: Rodent Research 1 (OSD-100)

**Project**: NASA's first Rodent Research spaceflight experiment assessed viability of multi-omics analyses on archived tissue samples from mice aboard the International Space Station.

**Organism**: *Mus musculus* (house mouse)

**Study Description**: 
NASA's Rodent Research (RR) project is playing a critical role in advancing biomedical research on the physiological effects of space environments. This investigation assessed viability of RNA, DNA, and protein extracted from archived RR-1 tissue samples for epigenomic, transcriptomic, and proteomic assays. Tissues were harvested from subjects, snap-frozen or RNAlater-preserved, and then stored at least a year at -80°C after return to Earth.

### Assay Details

**Assay ID**: `OSD-100-f1b7f0b93f8d28bc606c5c1127f2d7c9`

**Experimental Design**:
- **Measurement Type**: Transcription profiling
- **Technology**: RNA Sequencing (RNA-Seq)
- **Tissue**: Left eye (UBERON:0004548)
- **Comparison**: Space Flight vs Ground Control
  - factor_space_1: "Space Flight"
  - factor_space_2: "Ground Control"

### Sample Differential Expression Results

This assay measured differential gene expression in 206 genes comparing space flight to ground control conditions. Here are representative findings:

| Gene Symbol | log2 Fold Change | Adjusted p-value | Interpretation |
|-------------|------------------|------------------|----------------|
| Isg15 | +0.925 | 0.027 | Up-regulated in space flight |
| R3hdml | -1.143 | 0.002 | Down-regulated in space flight (highly significant) |
| Upb1 | -1.036 | 0.003 | Down-regulated in space flight (highly significant) |
| Colq/LOC102639719 | -1.154 | 0.039 | Down-regulated in space flight |
| Kcnj13 | +0.383 | 0.016 | Up-regulated in space flight |
| Tex15 | +0.421 | 0.006 | Up-regulated in space flight |
| Gm2000 | -0.192 | 0.035 | Down-regulated in space flight |
| Upk3b | -0.683 | 0.028 | Down-regulated in space flight |
| Ndufb1 | -0.204 | 0.021 | Down-regulated in space flight |
| 3425401B19Rik | -0.806 | 0.034 | Down-regulated in space flight |

**Key Findings**:
- Genes with positive log2fc values (e.g., Isg15, Kcnj13, Tex15) show increased expression during space flight compared to ground control
- Genes with negative log2fc values (e.g., R3hdml, Upb1, Colq) show decreased expression in space flight
- Statistical significance is indicated by adj_p_value < 0.05
- The magnitude of log2fc indicates the strength of the effect (values > 1 or < -1 represent more than 2-fold changes)

### Biological Interpretation

This example demonstrates how the Assay node connects:
- **Experimental conditions** (space flight vs ground control)
- **Molecular changes** (gene expression alterations)
- **Specific tissues** (left eye)

This enables researchers to understand the biological impacts of spaceflight at the molecular level. The left eye tissue shows significant transcriptional changes in response to microgravity and the space environment, with multiple genes involved in cellular processes being differentially regulated.

---

## Technical Notes

### SPARQL Query Examples Used

1. **Retrieve schema**:
```sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX spoke: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>

SELECT DISTINCT ?factor_space_1 ?factor_space_2
WHERE {
  ?assay a obo:OBI_0000070 .
  ?assay spoke:factor_space_1 ?factor_space_1 .
  ?assay spoke:factor_space_2 ?factor_space_2 .
}
```

2. **Retrieve differential expression data**:
```sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX spoke: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?study ?gene_symbol ?log2fc ?adj_p_value
WHERE {
  ?study spoke:PERFORMED_SpAS <assay_uri> .
  <assay_uri> spoke:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG ?gene .
  ?gene spoke:symbol ?gene_symbol .
  
  ?edge a rdf:Statement ;
        rdf:subject <assay_uri> ;
        rdf:predicate spoke:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG ;
        rdf:object ?gene ;
        spoke:log2fc ?log2fc ;
        spoke:adj_p_value ?adj_p_value .
}
```

---

## Conclusion

The Assay node in SPOKE-GeneLab serves as a central hub connecting:
- Studies (experimental context)
- Biological materials (tissues, cell types)
- Molecular measurements (genes, methylation regions)
- Experimental conditions (space flight vs various controls)
- Statistical evidence (fold changes, p-values)

This rich data model enables complex queries across NASA's spaceflight biology datasets, facilitating systems-level understanding of how organisms respond to space environments.
