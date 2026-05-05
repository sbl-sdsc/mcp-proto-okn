# BiomarkerKG — Prostate Cancer Biomarkers

👤 **User**
@biomarkerkg: Show me biomarkers related to prostate cancer

---

🧠 **Assistant**

Here's a summary of what BiomarkerKG returned for prostate cancer (DOID:10283):

**2,402 biomarkers total** are linked to prostate cancer. The vast majority (2,379) are **genetic SNP biomarkers** — single nucleotide polymorphisms identified by dbSNP `rs` IDs — predominantly with a **diagnostic** role. These represent genome-wide association study (GWAS) hits cataloged across multiple sources (BiomarkerKB's BB, BA, AQ, AO, AV prefix datasets).

Only two entries have protein component information:
- **BB1495-1** → UniProt Q9UBX7 (measured in **blood**)
- **AN6612-1** → UniProt Q9UHK6 (measured in **urine**)

### Summary Statistics

| Metric | Count |
|---|---|
| Total biomarkers | 2,402 |
| Genetic SNPs | 2,379 |
| Protein biomarkers | 2 |
| Other/untyped | 21 |

### Biomarker Roles

| Role ID | Role | Count |
|---|---|---|
| OBCI:0000008 | Diagnostic | 2,399 |
| OBCI:0000006 | Prognostic | 3 |

### Protein Biomarkers (with specimen info)

**BB1495-1**
- Component: [UniProt Q9UBX7](https://www.uniprot.org/uniprot/Q9UBX7)
- Specimen: Blood (UBERON:0000178)
- Role: Diagnostic
- Source: [BiomarkerKB BB1495-1](https://biomarkerkb.org/biomarker/BB1495-1)

**AN6612-1**
- Component: [UniProt Q9UHK6](https://www.uniprot.org/uniprot/Q9UHK6)
- Specimen: Urine (UBERON:0001088)
- Role: Diagnostic
- Source: [BiomarkerKB AN6612-1](https://biomarkerkb.org/biomarker/AN6612-1)

### Sample — Genetic SNP Biomarkers

2,379 total SNP biomarkers; a representative sample (all diagnostic role):

| Biomarker ID | SNP |
|---|---|
| BB1037-1 | [rs10021065](https://www.ncbi.nlm.nih.gov/snp/rs10021065) |
| BB1065-1 | [rs10025078](https://www.ncbi.nlm.nih.gov/snp/rs10025078) |
| BB1029-1 | [rs10043416](https://www.ncbi.nlm.nih.gov/snp/rs10043416) |
| BB0535-1 | [rs10177414](https://www.ncbi.nlm.nih.gov/snp/rs10177414) |
| BB0919-1 | [rs10188360](https://www.ncbi.nlm.nih.gov/snp/rs10188360) |
| BB0980-1 | [rs1023529](https://www.ncbi.nlm.nih.gov/snp/rs1023529) |
| AO1365-1 | [rs4792311](https://www.ncbi.nlm.nih.gov/snp/rs4792311) |
| BB0892-1 | [rs10499188](https://www.ncbi.nlm.nih.gov/snp/rs10499188) |
| BB0534-1 | [rs10502901](https://www.ncbi.nlm.nih.gov/snp/rs10502901) |
| BB0270-1 | [rs1052375](https://www.ncbi.nlm.nih.gov/snp/rs1052375) |

+ 2,369 more SNP biomarkers — browse the full set at [biomarkerkb.org](https://biomarkerkb.org)

A note on data depth: the KG stores structured identifiers (DOID disease IDs, UniProt accessions, dbSNP rs IDs, UBERON tissue codes) but most entries lack human-readable names within the graph itself. Following the links to [biomarkerkb.org](https://biomarkerkb.org) or [NCBI dbSNP](https://www.ncbi.nlm.nih.gov/snp/) gives the full gene/protein names and biological context for each entry.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-04*

*Model: claude-sonnet-4-6*
