## Chat Transcript
SPOKE GeneLab + SPOKE-OKN: OSD-161 (Rodent Research 3) Spaceflight Transcriptomics and Disease Relevance (2026-01-05)

👤 **User**  
Objective: Integrate GeneLab and SPOKE knowledge to characterize spaceflight-associated gene expression changes and their disease relevance.

@spoke-genelab
1. Retrieve study OSD-161 and summarize its experimental design (organism, mission, spaceflight vs. ground control).
2. List all assays associated with this study.
3. Extract the unique experimental factors across these assays (e.g., tissue, timepoint, platform).
4. Compare assay for spaceflight vs. ground control and return:
   - Top 5 up-regulated genes
   - Top 5 down-regulated genes
   (include log fold change and adjusted p-value if available).
5. Map the resulting genes to their human orthologs.

@spoke-okn
6. Map the human orthologs to associated diseases, indicating:
   - Disease name
   - Evidence type or source KG
   - Number of supporting associations (if available).

Output format:
- Tables for assays, factors, gene lists, ortholog mappings, and disease associations
- A short narrative summary synthesizing biological and translational relevance

@spoke-genelab
7. Create chat transcript

---

🧠 **Assistant**  
I queried the SPOKE GeneLab (spoke-genelab) and SPOKE-OKN (spoke-okn) SPARQL endpoints to extract OSD-161 metadata, associated assays, differential-expression results, mouse-to-human ortholog mappings, and gene–disease links.

Key results extracted from the KGs:
- **Study:** OSD-161 (Rodent Research 3, RR3), a NASA ISS spaceflight study linked to **SpaceX-8** (2016-04-08 → 2016-05-11) and **SpaceX-9** (2016-07-18 → 2016-08-26).
- **Assays:** 6 transcription-profiling RNA-Seq assays on **mouse adrenal gland**, spanning pairwise contrasts among **Space Flight**, **Ground Control**, and **Basal Control**.
- **Primary contrast used for DE gene ranking:** Space Flight vs Ground Control.
- **Top up-regulated mouse genes:** Fos, Btg2, G530011O06Rik, Cited2, Dusp1 (with log2fc and adjusted p-values).
- **Top down-regulated mouse genes:** H2-Q6, H2-Q7/Q9, Gad1, Cd72 (with log2fc and adjusted p-values).
- **Human orthologs:** 1:1 mappings for FOS, BTG2, CITED2, DUSP1, GAD1, CD72; 1:many MHC mapping from mouse H2 genes to multiple HLA genes (HLA-A/B/C/E/F/G). Some mouse genes did not have a mapped human ortholog in the KG.
- **Disease associations (SPOKE-OKN):** diseases were linked via SPOKE-OKN gene–disease predicates such as `ASSOCIATES_DaG`, `MARKER_POS_GmpD`, and `MARKER_NEG_GmnD`.

[Full report with the requested tables and narrative synthesis](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/OSD-161_GPT-5.2-report-vs-studio.md)

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 on 2026-01-05*
Model: GPT-5.2
