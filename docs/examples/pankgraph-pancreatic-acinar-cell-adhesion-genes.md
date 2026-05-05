# PanKgraph: Genes Expressed in Pancreatic Acinar Cells Regulating Cell-Matrix Adhesion

👤 **User**
@pankgraph: Find genes expressed in pancreas acinar cells and regulating cell-matrix adhesion

---

🧠 **Assistant**

Queried the **PanKgraph** knowledge graph (PanKbase Knowledge Graph, focused on human pancreas and diabetes research) using the following approach:

1. **Ontology lookups** resolved:
   - *Pancreatic acinar cell* → `CL:0002064`
   - *Cell-matrix adhesion* → `GO:0007160` (with 9 ontological descendants expanded, including integrin activation `GO:0016340`, smooth muscle cell-matrix adhesion `GO:0061302`, and fibronectin-mediated adhesion `GO:0007161`)

2. **SPARQL query** on PanKgraph matched genes satisfying both:
   - `biolink:expressed_in` → `CL:0002064` (Acinar Cell, 11,590 genes total in graph)
   - `biolink:functional_association` → GO:0007160 or any descendant term

**Result: 45 genes** expressed in pancreatic acinar cells with GO annotations to cell-matrix adhesion.

---

### Results Table

| Gene | Ensembl ID | GO annotation |
|------|-----------|---------------|
| ADAM15 | ENSG00000143537 | cell-matrix adhesion |
| ADAM9 | ENSG00000168615 | cell-matrix adhesion |
| ANXA2 | ENSG00000182718 | cell-matrix adhesion |
| BCAM | ENSG00000187244 | cell-matrix adhesion |
| BCL2L11 | ENSG00000153094 | cell-matrix adhesion |
| BCL6 | ENSG00000113916 | cell-matrix adhesion |
| CCN2 | ENSG00000118523 | cell-matrix adhesion |
| CD44 | ENSG00000026508 | cell-matrix adhesion |
| CD63 | ENSG00000135404 | cell-matrix adhesion |
| CTNNB1 | ENSG00000168036 | cell-matrix adhesion |
| DAG1 | ENSG00000173402 | integrin activation |
| DDR1 | ENSG00000204580 | smooth muscle cell-matrix adhesion |
| EMP2 | ENSG00000213853 | cell-matrix adhesion |
| EPDR1 | ENSG00000086289 | cell-matrix adhesion |
| FBLN5 | ENSG00000140092 | cell-matrix adhesion |
| FERMT2 | ENSG00000073712 | cell-matrix adhesion |
| FGA | ENSG00000171560 | cell-matrix adhesion |
| FGG | ENSG00000171557 | cell-matrix adhesion |
| FGL1 | ENSG00000104760 | cell-matrix adhesion |
| FN1 | ENSG00000115414 | cell-matrix adhesion + fibronectin-mediated |
| ILK | ENSG00000166333 | cell-matrix adhesion |
| ITGA3 | ENSG00000005884 | cell-matrix adhesion |
| ITGA6 | ENSG00000091409 | cell-matrix adhesion |
| ITGAE | ENSG00000083457 | cell-matrix adhesion |
| ITGAV | ENSG00000138448 | cell-matrix adhesion |
| ITGB1 | ENSG00000150093 | cell-matrix adhesion + fibronectin-mediated |
| ITGB1BP1 | ENSG00000119185 | cell-matrix adhesion |
| ITGB4 | ENSG00000132470 | cell-matrix adhesion |
| ITGB5 | ENSG00000082781 | cell-matrix adhesion |
| ITGB6 | ENSG00000115221 | cell-matrix adhesion |
| LYVE1 | ENSG00000133800 | cell-matrix adhesion |
| NPNT | ENSG00000168743 | cell-matrix adhesion |
| PKD1 | ENSG00000008710 | cell-matrix adhesion + fibronectin-mediated |
| PPFIA1 | ENSG00000131626 | cell-matrix adhesion |
| RAC1 | ENSG00000136238 | cell-matrix adhesion |
| RHOA | ENSG00000067560 | cell-matrix adhesion |
| SNED1 | ENSG00000162804 | cell-matrix adhesion |
| SORBS1 | ENSG00000095637 | cell-matrix adhesion |
| THBS3 | ENSG00000169231 | cell-matrix adhesion |
| TIMM10B | ENSG00000132286 | cell-matrix adhesion |
| TRPM7 | ENSG00000092439 | integrin activation |
| TSC1 | ENSG00000165699 | cell-matrix adhesion |
| VCL | ENSG00000035403 | cell-matrix adhesion |
| VWA2 | ENSG00000165816 | fibronectin-mediated adhesion |
| ZYX | ENSG00000159840 | cell-matrix adhesion |

---

### Key biological findings

**Cell-matrix adhesion (GO:0007160) — 41 genes.** The list is dominated by integrin subunits: `ITGA3`, `ITGA6`, `ITGAE`, `ITGAV`, `ITGB1`, `ITGB4`, `ITGB5`, `ITGB6` (multiple α/β integrin chains), plus integrin regulators `ILK` (integrin-linked kinase), `FERMT2` (kindlin-2), `ITGB1BP1`, and `SORBS1`. Also notable are extracellular matrix components `FN1` (fibronectin-1), `FBLN5` (fibulin-5), `THBS3` (thrombospondin-3), and `NPNT` (nephronectin); signaling effectors `RHOA`, `RAC1`, `CTNNB1` (β-catenin), and `TSC1`; and cell-surface molecules `CD44`, `CD63`, `BCAM`, and `LYVE1`.

**Integrin activation (GO:0016340) — 2 additional genes:** `DAG1` (dystroglycan) and `TRPM7` (a channel-kinase involved in adhesion signaling).

**Fibronectin-mediated / smooth muscle cell-matrix adhesion — 3 additional genes:** `VWA2`, `DDR1` (discoidin domain receptor 1, a collagen receptor tyrosine kinase), and additional annotations on `FN1`, `ITGB1`, and `PKD1`.

The list is heavily enriched for integrin-mediated adhesion machinery, which makes biological sense — acinar cells sit within a basement membrane and rely on integrins and their co-regulators for structural integrity and polarity.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-05*

*Model: claude-sonnet-4-6*
