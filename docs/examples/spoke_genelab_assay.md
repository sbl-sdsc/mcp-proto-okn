# GeneLab Knowledge Graph: Assay Node Exploration
## Chat Transcript

**Date:** December 11, 2025  
**Topic:** Understanding the Assay node structure in the GeneLab SPARQL endpoint  
**Focus:** Space flight vs ground control comparisons

---

### User Query
> Describe the Assay node and its properties in @genelab-remote-cypher, and include an example for a space flight vs ground control comparison.

---

### Claude's Investigation Process

#### Step 1: Schema Discovery
First, I retrieved the complete schema to understand the GeneLab knowledge graph structure.

**Key Findings:**
- **7 Classes** including Assay, Gene, Study, Mission, Anatomy, CellType, and MethylationRegion
- **40 Predicates** defining relationships and properties
- Assay class URI: `http://purl.obolibrary.org/obo/OBI_0000070`

#### Step 2: Understanding Assay Properties
The Assay node has the following property categories:

**Experimental Design Properties:**
- `factor_space_1`: Primary experimental grouping (e.g., "Space Flight")
- `factor_space_2`: Secondary experimental grouping (e.g., "Ground Control")
- `factors_1`: Primary experimental factors (array)
- `factors_2`: Secondary experimental factors (array)

**Biological Material Properties:**
- `material_1` / `material_2`: Biological material names
- `material_name_1` / `material_name_2`: Ontology-based material names
- `material_id_1` / `material_id_2`: Controlled ontology identifiers (UBERON codes)

**Methodology Properties:**
- `measurement`: Type of data produced (e.g., "transcription profiling")
- `technology`: Platform/method used (e.g., "RNA Sequencing (RNA-Seq)")

**Organism Information:**
- `organism`: NCBI scientific organism name
- `taxonomy`: NCBI taxonomy ID

#### Step 3: Exploring Relationships
The Assay node connects to other entities through:

1. **INVESTIGATED_ASiA** → Anatomical entities
2. **INVESTIGATED_ASiCT** → Cell types
3. **MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG** → Genes (with edge properties)
4. **MEASURED_DIFFERENTIAL_METHYLATION_ASmMR** → Methylation regions
5. **PERFORMED_SpAS** ← Studies (inverse relationship)

#### Step 4: Finding Real Data
I queried for actual space flight vs ground control comparisons and found multiple assays.

---

### Example Analysis: Space Flight Effects on Mouse Eye

**Assay Details:**
- **ID:** OSD-100-f1b7f0b93f8d28bc606c5c1127f2d7c9
- **Study:** OSD-100
- **Label:** OSD-100_transcription-profiling_rna-sequencing-(rna-seq)

**Experimental Parameters:**
```
Organism:          Mus musculus (mouse)
Tissue:            Left eye (UBERON:0004548)
Technology:        RNA Sequencing (RNA-Seq)
Measurement Type:  Transcription profiling
Comparison:        Space Flight vs Ground Control
```

**Differential Expression Results:**

| Gene Symbol | Gene Name | Log2FC | Adj. P-value | Regulation |
|-------------|-----------|--------|--------------|------------|
| Apol9b | Apolipoprotein L9b | +1.83 | 0.011 | ↑ Up in space |
| Apol9a | Apolipoprotein L9a | +1.79 | 0.002 | ↑ Up in space |
| Oas2 | 2'-5'-oligoadenylate synthetase 2 | +1.74 | 0.002 | ↑ Up in space |
| Oas3 | 2'-5'-oligoadenylate synthetase 3 | +1.56 | 0.006 | ↑ Up in space |
| Sst | Somatostatin | +1.52 | 2.3×10⁻⁶ | ↑ Up in space |
| Oas1a | 2'-5'-oligoadenylate synthetase 1A | +1.52 | 0.0006 | ↑ Up in space |
| Fbp2 | Fructose-bisphosphatase 2 | -1.30 | 0.039 | ↓ Down in space |
| Spink7 | Serine peptidase inhibitor, Kazal type 7 | +1.26 | 0.012 | ↑ Up in space |
| Pln | Phospholamban | -1.16 | 0.003 | ↓ Down in space |
| Colq | Collagen-like tail subunit | -1.15 | 0.039 | ↓ Down in space |

**Biological Interpretation:**

The differential expression pattern reveals several key responses to spaceflight in mouse eye tissue:

1. **Immune/Stress Response Activation:**
   - Multiple oligoadenylate synthetases (Oas1a, Oas2, Oas3) are significantly up-regulated
   - These enzymes are part of the interferon-mediated antiviral response
   - Suggests activation of innate immune pathways

2. **Lipid Metabolism Changes:**
   - Apolipoprotein L family members (Apol9a, Apol9b) show strong up-regulation
   - May indicate alterations in lipid transport or cellular stress responses

3. **Metabolic Adjustments:**
   - Fbp2 (gluconeogenesis enzyme) is down-regulated
   - Could reflect changes in energy metabolism under microgravity

4. **Regulatory Changes:**
   - Somatostatin (Sst) up-regulation suggests neuroendocrine signaling changes
   - Phospholamban (Pln) down-regulation may affect calcium handling

---

### Additional Example Assays Found

The knowledge graph contains multiple comparative assays:

1. **OSD-100** (Eye tissue, RNA-Seq)
   - Space Flight vs Ground Control comparison
   - Ground Control vs Space Flight comparison (reciprocal)

2. **OSD-101** (Gastrocnemius muscle, RNA-Seq)
   - Multiple assays comparing Space Flight and Ground Control
   - Different tissues allow cross-tissue comparison of spaceflight effects

---

### Technical Notes on Data Structure

**Edge Properties:**
The differential expression data uses RDF reification, where properties like `log2fc` and `adj_p_value` are attached to the relationship (edge) between the Assay and Gene, not to the Gene node itself.

**SPARQL Pattern for Querying Differential Expression:**
```sparql
SELECT ?gene ?symbol ?log2fc ?adj_p_value
WHERE {
  ?stmt a rdf:Statement .
  ?stmt rdf:subject <ASSAY_URI> .
  ?stmt rdf:predicate schema:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG .
  ?stmt rdf:object ?gene .
  ?stmt schema:log2fc ?log2fc .
  ?stmt schema:adj_p_value ?adj_p_value .
  ?gene schema:symbol ?symbol .
}
```

---

### Summary

The GeneLab knowledge graph provides a rich, interconnected dataset for studying molecular responses to spaceflight. The Assay node serves as the central hub connecting:
- Experimental design metadata
- Biological samples and anatomical context
- Molecular measurements (gene expression, methylation)
- Statistical results (fold changes, significance values)
- Study and mission context

This structure enables systematic cross-study comparisons and meta-analyses of spaceflight biology.

---

**End of Transcript**
