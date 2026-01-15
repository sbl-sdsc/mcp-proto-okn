# Prompt: Cross-Study Disease Gene Expression Meta-Analysis

## Objective
Identify consistently dysregulated genes across multiple independent studies of a specific disease to discover robust biomarkers or therapeutic targets.

## Background
The Gene Expression Atlas Knowledge Graph integrates 243 studies with 797 assays profiling 152,879 genes. This resource enables meta-analysis across independent experiments to identify genes with reproducible differential expression patterns. Genes showing consistent dysregulation across multiple studies represent more robust candidates for further investigation than single-study findings.

## Task Description
Perform a cross-study meta-analysis to identify genes that are consistently differentially expressed in [DISEASE OF INTEREST] across multiple independent studies in the Gene Expression Atlas Knowledge Graph.

### Specific Steps:

1. **Identify Relevant Studies**
   - Query the knowledge graph to find all studies examining [DISEASE OF INTEREST]
   - Filter studies by relevant experimental factors (e.g., specific tissue types, cell types, developmental stages)
   - Document the number of studies and assays available for analysis

2. **Extract Differential Expression Data**
   - For each relevant study/assay, retrieve genes showing differential expression
   - Collect quantitative metrics including:
     - Effect sizes (log2 fold changes)
     - Statistical significance (p-values, adjusted p-values)
     - Direction of change (up-regulated vs. down-regulated)
   - Note the experimental context (test vs. reference groups)

3. **Cross-Study Consistency Analysis**
   - Identify genes appearing in multiple studies
   - Assess consistency of:
     - Direction of differential expression (consistently up or down)
     - Effect size magnitude
     - Statistical significance across studies
   - Rank genes by:
     - Number of studies showing differential expression
     - Consistency of direction
     - Average effect size

4. **Biological Context Integration**
   - Link identified genes to:
     - Biological processes (GO terms)
     - Molecular pathways
     - Protein domains
     - Known disease associations
   - Examine anatomical and cellular contexts where genes show consistent patterns

5. **Generate Insights**
   - Identify top candidate biomarker genes (high consistency, large effect sizes)
   - Highlight novel candidates not previously associated with the disease
   - Compare findings across different tissues/cell types if applicable
   - Suggest potential mechanisms based on pathway connections

## Example Queries

### Find Studies on a Specific Disease
```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX genelab: <https://spoke.ucsf.edu/genelab/>

SELECT DISTINCT ?study ?title ?pubmed
WHERE {
  ?study a biolink:Study ;
         genelab:project_title ?title .
  OPTIONAL { ?study genelab:pubmed_id ?pubmed . }
  FILTER(CONTAINS(LCASE(?title), "your_disease_keyword"))
}
```

### Get Differential Expression Data for Studies
```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX genelab: <https://spoke.ucsf.edu/genelab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?study_id ?gene ?gene_label ?effect_size ?p_value
WHERE {
  ?study a biolink:Study ;
         genelab:study_id ?study_id ;
         biolink:has_output ?assay .
  
  ?expr a biolink:GeneExpressionMixin ;
        biolink:subject ?assay ;
        biolink:object ?gene .
  
  ?gene rdfs:label ?gene_label .
  
  OPTIONAL { ?expr genelab:effect_size ?effect_size . }
  OPTIONAL { ?expr genelab:p_value ?p_value . }
  
  FILTER(CONTAINS(LCASE(?study_title), "your_disease_keyword"))
}
```

## Success Criteria

The analysis should produce:

1. **Ranked Gene List**: Genes ordered by cross-study consistency and effect size
2. **Study Coverage Matrix**: Which genes appear in which studies with their expression patterns
3. **Biological Context**: Pathways and processes enriched in consistently dysregulated genes
4. **Novel Discoveries**: Genes not previously well-characterized in the disease context
5. **Validation Recommendations**: Suggestions for experimental validation based on reproducibility

## Example Diseases to Explore

- **Diabetic nephropathy**: Multiple studies examining kidney tissue in diabetes
- **Breast cancer**: Studies across different subtypes and stages
- **Inflammatory bowel disease**: Colon tissue samples from IBD patients
- **Alzheimer's disease**: Brain tissue from affected patients
- **Cardiovascular disease**: Heart and vascular tissue studies

## Expected Outputs

1. **Summary Report**: 
   - Number of studies analyzed
   - Total genes with differential expression
   - Top 20-50 genes with consistent patterns
   - Statistical summaries of reproducibility

2. **Visualization Suggestions**:
   - Heatmap of gene expression across studies
   - Volcano plots for individual studies
   - Network diagram of gene-pathway connections
   - Venn diagrams of overlapping gene sets

3. **Biological Interpretation**:
   - Functional enrichment analysis results
   - Known vs. novel disease gene associations
   - Tissue/cell-type specific patterns
   - Potential therapeutic implications

## Tips for Success

- Start with diseases that have 3+ studies for meaningful meta-analysis
- Consider tissue specificity - compare studies from the same anatomical context
- Look for both highly significant genes AND genes with large effect sizes
- Don't ignore genes that are consistently changed but with modest effect sizes
- Consider experimental platform differences when interpreting results
- Use PubMed IDs to review original study designs and validate findings

## Next Steps After Analysis

1. Cross-reference findings with external databases (GeneCards, DisGeNET, OMIM)
2. Design validation experiments for top candidates
3. Explore therapeutic potential using drug-gene interaction databases
4. Consider single-cell or spatial transcriptomics follow-up for tissue-specific findings
5. Publish meta-analysis findings to contribute to the field
