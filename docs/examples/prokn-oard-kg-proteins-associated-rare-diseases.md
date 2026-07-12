# Chat Transcript
Integrating ProKN and OARD-KG to Identify Human Proteins Associated with Rare Diseases

👤 **User**

Integrate prokn and oard-kg to identify human proteins that are associated with rare diseases. 1. Give me the count of diseases in oard-kg. 2. Map the diseases in oard-kg with prokn. 3. Give me the count of unique rare diseases in prokn that have at least one associated protein. 4. Retrieve gene symbols of the associated proteins. 5. In the final output, include the rare disease name, the disease identifier in oard-kg, the disease identifier in prokn, the uniprot accession of the associated proteins and the gene symbols of those proteins. Group the results by the disease id and save the results as a .csv file.

---

🧠 **Assistant**

I worked through the integration step by step.

**How the two graphs connect.** OARD-KG identifies its rare diseases with MONDO URIs (e.g., `http://purl.obolibrary.org/obo/MONDO_0007309`), typed via `biolink:category biolink:Disease`. ProKN identifies diseases with UniProt Disease nodes (`http://purl.uniprot.org/core/Disease`), keyed mostly to OMIM, and each ProKN Disease node carries `rdfs:seeAlso` cross-references — including MONDO. The two graphs share no namespace directly, so I bridged on MONDO via that `seeAlso` link. Proteins connect to diseases in ProKN through the Biolink `associated_with` predicate, with the UniProt accession on `obo:NCIT_C25402` and the gene symbol(s) on `obo:NCIT_C164806`; `upcore:organism "Homo sapiens"` restricts to human proteins. I ran the join as a federated SPARQL query (ProKN as base graph, with a `SERVICE` call to the OARD-KG endpoint) so the intersection was computed server-side.

The schema relationship used for the integration:

```mermaid
classDiagram
    class OARD_Disease {
        URI MONDO_xxxxxxx
        category = Disease
        label
    }
    class ProKN_Disease {
        URI OMIM / DOID
        a Disease
        seeAlso -> MONDO
    }
    class ProKN_Protein {
        a Protein
        organism = Homo sapiens
        NCIT_C25402 = UniProt accession
        NCIT_C164806 = gene symbol
    }
    ProKN_Protein --> ProKN_Disease : associated_with
    ProKN_Disease --> OARD_Disease : seeAlso MONDO
    ProKN_Protein ..> OARD_Disease : associated_with direct UNION branch
```

**Step 1 — Count of diseases in OARD-KG.** Counting distinct entities with `biolink:category biolink:Disease`:

> **2,297 diseases**

**Step 2 — Mapping OARD-KG diseases to ProKN.** ProKN disease nodes were matched to OARD-KG diseases via their MONDO `rdfs:seeAlso` cross-reference. Restricting to human UniProt proteins associated with those diseases, the mapping resolved to **277 OARD-KG rare diseases (MONDO IDs)**.

**Step 3 — Unique rare diseases in ProKN with at least one associated protein.**

> **275 distinct ProKN disease entities** (which correspond to the 277 MONDO IDs above — a few MONDO terms map to more than one ProKN disease node), spanning **325 distinct human proteins**.

**Step 4 — Gene symbols.** Retrieved from `obo:NCIT_C164806`. Where UniProt records more than one symbol/synonym for a protein, they are reported together (e.g., APP is recorded as `AD1; A4; APP`).

**Step 5 — Final output.** I produced a CSV with columns `rare_disease_name`, `oardkg_disease_id` (MONDO CURIE), `prokn_disease_id` (OMIM CURIE), `uniprot_accession`, and `gene_symbols`, sorted/grouped by the OARD-KG disease ID. At the protein level (one row per disease–protein–accession) the table has **353 rows** covering the 277 rare diseases.

The federated query used for the protein-level extraction:

```sparql
SELECT ?mondo ?dname ?disease ?acc
       (GROUP_CONCAT(DISTINCT ?sym; SEPARATOR="; ") AS ?symbols)
WHERE {
  ?protein a <http://purl.uniprot.org/core/Protein> .
  ?protein <http://purl.uniprot.org/core/organism> "Homo sapiens" .
  ?protein <http://purl.obolibrary.org/obo/NCIT_C25402> ?acc .
  ?protein <https://biolink.github.io/biolink-model/associated_with> ?disease .
  ?disease a <http://purl.uniprot.org/core/Disease> .
  ?disease <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?mondo .
  FILTER(STRSTARTS(STR(?mondo), "http://purl.obolibrary.org/obo/MONDO_"))
  OPTIONAL { ?protein <http://purl.obolibrary.org/obo/NCIT_C164806> ?sym . }
  SERVICE <https://apps.okn.us/oard-kg/sparql> {
    ?mondo <https://w3id.org/biolink/vocab/category> <https://w3id.org/biolink/vocab/Disease> .
    ?mondo <http://www.w3.org/2000/01/rdf-schema#label> ?dname .
  }
}
GROUP BY ?mondo ?dname ?disease ?acc
ORDER BY ?mondo ?acc
```

A sample of the resulting CSV:

| rare_disease_name | oardkg_disease_id | prokn_disease_id | uniprot_accession | gene_symbols |
|---|---|---|---|---|
| muscular dystrophy-dystroglycanopathy, type A | MONDO:0000171 | OMIM:236670 | Q9Y6A1 | POMT1 |
| familial juvenile hyperuricemic nephropathy | MONDO:0000608 | OMIM:613092 | P00797 | REN |
| glycogen storage disease I | MONDO:0002413 | OMIM:232200 | P35575 | G6PC1 |
| Jervell and Lange-Nielsen syndrome | MONDO:0002441 | OMIM:220400 | P51787 | KCNQ1 |
| amyotrophic lateral sclerosis | MONDO:0004976 | OMIM:105500 | Q96QT4 | TRPM7 |
| … (353 rows total) | | | | |

**Caveats.** The `gene_symbols` field reflects what UniProt stores, so it can include legacy synonyms. The counts are sensitive to how "associated protein" is defined — I used human UniProt proteins associated with a disease that carries a MONDO mapping into OARD-KG. Broadening to gene-level (Ensembl/HGNC) associations, or to OMIM-only disease nodes without a MONDO link, would change the totals.

Output file: [rare_disease_proteins_prokn_oardkg.csv](docs/examples/rare_disease_proteins_prokn_oardkg.csv)

---

👤 **User**

Run the following ground-truth query: *(federated query against ProKN with a `SERVICE` call to OARD-KG, selecting `?rareDisease`, `?rareDiseaseLabelStr`, and a `GROUP_CONCAT` of `accession(geneName)` as `?assocProteins`, grouped by disease, with a UNION over the `seeAlso`-bridged path and the direct `associated_with` path).*

---

🧠 **Assistant**

The ground-truth query ran successfully (after fixing two parse-level typos — `REFIX` → `PREFIX` on the first line, and a missing space before `(GROUP_CONCAT...` in the SELECT — while preserving the logic, including the UNION). It returned:

> **277 rows** — one per rare disease, with associated proteins grouped into the `accession(geneName)` format.

This reconciles cleanly with the earlier deliverable. My CSV was structured at the **protein level** (one row per disease–protein–accession pair = 353 rows), whereas the ground-truth query is grouped at the **disease level** (277 rows). The set of diseases is identical — the earlier file already contained exactly the same **277 distinct rare diseases**. Notably, the `UNION` branch for proteins associated directly with the MONDO URI added no diseases beyond the `seeAlso` bridge — both paths converge on the same 277 diseases.

I saved the ground-truth result as `rare_disease_proteins_groundtruth.csv` (columns: `rareDisease`, `rareDiseaseLabelStr`, `assocProteins`).

Summary of the two deliverables:

- `rare_disease_proteins_groundtruth.csv` — 277 rows, grouped by disease, proteins concatenated as `accession(geneName)`.
- `rare_disease_proteins_prokn_oardkg.csv` — 353 rows, the same 277 diseases expanded so each disease–protein–accession pair is its own row.

Both cover the identical set of 277 rare diseases; they differ only in row granularity and protein-column formatting.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-29*

Model: claude-opus-4-8
