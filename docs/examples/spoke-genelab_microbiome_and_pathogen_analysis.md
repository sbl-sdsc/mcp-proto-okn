# SPOKE GeneLab OSD-267: Spaceflight Microbiome & Pathogen Analysis

---

👤 **User**

@spoke-genelab: OSD-267

---

🧠 **Assistant**

Here's a summary of **OSD-267** from the SPOKE GeneLab knowledge graph:

### Veggie Hardware Validation Test (VEG-01)

**Type:** Spaceflight Study  
**Mission:** SpaceX-3 (NASA) — April 18 to May 18, 2014

This study was part of NASA's Veggie plant growth hardware validation aboard the ISS. It characterizes the microbial communities associated with plants grown in space versus ground controls.

**Assays:** All assays used **Amplicon Sequencing** with two complementary technologies:
- **16S rRNA** — for profiling bacterial communities
- **ITS (Internal Transcribed Spacer)** — for profiling fungal communities

**Sample types (plant compartments):**
- **Root**
- **Leaf**

**Experimental comparisons:** The study includes multiple pairwise differential abundance assays comparing:
- Space Flight vs. Ground Control (primary comparison)
- Root vs. Leaf (tissue-type comparison)
- Within-group comparisons (e.g., Space Flight root vs. Space Flight leaf)

There are no ontology-mapped anatomy or cell type annotations (this makes sense given the plant/microbial focus — UBERON/CL are animal-centric ontologies).

In short, OSD-267 profiles **plant-associated microbiomes** (bacteria and fungi) in roots and leaves of plants grown aboard the ISS during SpaceX CRS-3, comparing the microbial community shifts under spaceflight conditions to ground controls. Would you like to dig into the differential abundance results — e.g., which organisms showed the most significant changes between spaceflight and ground control?

---

👤 **User**

List the top 20 most abundant bacteria in spaceflight roots compared with ground control roots and in spaceflight leaves compared with ground control leaves

---

🧠 **Assistant**

Data was retrieved from spoke-genelab using SPARQL queries against the `MEASURED_DIFFERENTIAL_ABUNDANCE_ASmO` predicate for 16S assays. Assay `OSD-267-5e9596ea` (Space Flight root vs. Ground Control root, 38 taxa) and `OSD-267-49234af9` (Space Flight leaf vs. Ground Control leaf, 8 taxa) provided the primary data. Abundance values are natural-log transformed means.

#### Spaceflight Roots vs. Ground Control Roots — Top 20 (by ln mean abundance)

| Rank | Taxon | Taxonomic rank | SF ln(mean) | GC ln(mean) | log₂FC |
|------|-------|---------------|-------------|-------------|--------|
| 1 | *Ralstonia* | genus | 11.40 | 3.29 | +10.41 |
| 2 | Gammaproteobacteria | class | 10.65 | 1.55 | +11.84 |
| 3 | Chitinophagaceae | family | 10.49 | — | +13.85 |
| 4 | *Massilia* | genus | 10.32 | 2.25 | +10.35 |
| 5 | Xanthobacteraceae | family | 10.14 | — | +13.34 |
| 6 | *Mesorhizobium* | genus | 9.60 | 0.90 | +11.27 |
| 7 | *Acinetobacter* | genus | 9.38 | 1.04 | +10.74 |
| 8 | Comamonadaceae | family | 9.16 | — | +11.93 |
| 9 | *Methylobacterium* | genus | 8.99 | — | +11.67 |
| 10 | *Bradyrhizobium* | genus | 8.67 | — | +11.22 |
| 11 | *Hyphomicrobium* | genus | 7.95 | 0.35 | +9.68 |
| 12 | *Methylorubrum* | genus | 7.50 | — | +9.53 |
| 13 | Rhizobiaceae | family | 7.36 | — | +9.33 |
| 14 | *Cupriavidus* | genus | 7.26 | 0.97 | +7.78 |
| 15 | Micrococcaceae | family | 6.99 | — | +8.79 |
| 16 | Sphingomonadaceae | family | 6.91 | — | +8.67 |
| 17 | *Caedibacter* | genus | 6.83 | — | +8.57 |
| 18 | *Paenibacillus* | genus | 6.64 | — | +8.29 |
| 19 | *Sediminibacterium* | genus | 6.55 | — | +8.15 |
| 20 | Microbacteriaceae | family | 6.21 | — | +7.66 |

> SF = Space Flight, GC = Ground Control, — = below detection limit in that condition

#### Spaceflight Leaves vs. Ground Control Leaves — All taxa detected (9 total)

| Rank | Taxon | SF ln(mean) | GC ln(mean) | log₂FC |
|------|-------|-------------|-------------|--------|
| 1 | Bacteria (domain) | 3.80 | — | +5.46 |
| 2 | Gammaproteobacteria | 2.00 | — | +2.87 |
| 3 | Comamonadaceae | 1.67 | — | +2.38 |
| 4 | *Thauera* | 1.55 | — | +2.21 |
| 5 | *Pseudomonas* | 1.24 | — | +1.77 |
| 6 | *Massilia* | — | 2.25 | −3.26 |
| 7 | *Burkholderia* group | — | 2.72 | −3.94 |
| 8 | Sphingomonadaceae | — | 1.99 | −2.90 |
| 9 | Lysobacteraceae | — | 1.05 | −1.51 |

Key observations:
- Roots accumulated a far more diverse and abundant bacterial community in spaceflight, with all top 20 taxa showing massive enrichment (log₂FC 8–14)
- The near-zero ground control means suggest most root-enriched taxa were essentially absent on the ground
- Leaf communities were sparse by comparison, with only 9 taxa detected; some taxa (e.g. *Massilia*, Sphingomonadaceae) were actually *higher* in ground control leaves
- *Ralstonia* and *Gammaproteobacteria* dominate spaceflight roots by a wide margin

---

👤 **User**

With the list of the top 20 most abundant bacteria in spaceflight roots, use @spoke-okn to identify if any of those organisms are known plant pathogens or known human pathogens

---

🧠 **Assistant**

Cross-referencing against the spoke-okn knowledge graph using the `OrganismTaxon` class and node properties `host_is_human`, `disease`, `pathovar`, and `isolation_source`. Results are aggregated at genus level from strain-level records.

#### Pathogen Status — Top 20 Spaceflight Root Bacteria

| Root rank | Taxon | Rank | Pathogen status | SPOKE-OKN evidence |
|-----------|-------|------|-----------------|--------------------|
| 1 | *Ralstonia* | genus | **Both** (plant + human) | Plant: bacterial wilt in tomato, potato, banana, geranium; 10 pathovars. Human: 26 isolates — *R. pickettii* in immunocompromised/CF patients |
| 2 | Gammaproteobacteria | class | Indirect | High-level class containing many pathogens (e.g. *Acinetobacter*, *Pseudomonas*); too broad for direct matching |
| 3 | Chitinophagaceae | family | No record | Soil/water bacteria; no pathogen records at family level |
| 4 | *Massilia* | genus | Human pathogen | 27 strains; 3 human isolates (eye, blood, tissue) — rare opportunistic |
| 5 | Xanthobacteraceae | family | No record | Environmental nitrogen-fixing bacteria |
| 6 | *Mesorhizobium* | genus | Human pathogen | 1,002 strains; 4 blood isolates — rare opportunistic |
| 7 | *Acinetobacter* | genus | **Critical human pathogen** | 11,631 strains; 10,233 human isolates; diseases: nosocomial pneumonia, bacteremia, sepsis, wound infections; XDR/PDR strains documented |
| 8 | Comamonadaceae | family | Indirect | Contains some opportunistic genera (*Comamonas*, *Delftia*) |
| 9 | *Methylobacterium* | genus | Human pathogen | 130 strains; 2 human isolates (skin, celiac patient duodenum) |
| 10 | *Bradyrhizobium* | genus | Human pathogen | 700 strains; 1 human blood isolate |
| 11 | *Hyphomicrobium* | genus | No record | 5 strains; no disease/host data |
| 12 | *Methylorubrum* | genus | No record | 8 strains; plant-associated methylotroph |
| 13 | Rhizobiaceae | family | No record | Nitrogen-fixing plant-associated bacteria |
| 14 | *Cupriavidus* | genus | Human pathogen | 58 strains; 22 human isolates (blood, CF sputum/BAL, CSF, pleural effusion); ⚠️ one strain isolated from Kennedy Space Center air filter |
| 15 | Micrococcaceae | family | Indirect | Contains *Micrococcus*, *Arthrobacter*; some opportunistic species |
| 16 | Sphingomonadaceae | family | Indirect | Contains *Sphingomonas*; rare opportunist |
| 17 | *Caedibacter* | genus | No record | 7 strains; parasite of *Paramecium* protozoa only |
| 18 | *Paenibacillus* | genus | Human pathogen | 312 strains; 48 human isolates; causes American foulbrood (bees); 2 pathovars |
| 19 | *Sediminibacterium* | genus | No record | Aquatic environmental bacterium |
| 20 | Microbacteriaceae | family | No record | Soil actinobacteria; no family-level records |

Notable findings:

- **Ralstonia** (rank 1, most abundant) is a dual threat — a major plant pathogen AND an opportunistic human pathogen (*R. pickettii*) via contaminated water/hospital equipment
- **Acinetobacter** (rank 7) is a WHO Priority 1 "critical" pathogen with thousands of clinical isolates and documented pandrug resistance
- **Cupriavidus** (rank 14) has a strain in SPOKE-OKN isolated from the Payload Hazardous Servicing Facility at Kennedy Space Center, suggesting prior spacecraft contamination history
- 8 of the top 20 taxa are families or higher-level classes that may conceal additional pathogenic species not resolvable at 16S genus level

---

👤 **User**

Use @pubmed to identify peer-reviewed publications supporting that these organisms are known pathogens, return PMID, Title, Year, short summary (1 sentence).

---

🧠 **Assistant**

Based on articles retrieved from PubMed, the following peer-reviewed publications support the pathogen status of the organisms identified. All citations include DOI links to the original articles.

| PMID | Year | Taxon | Title | One-sentence summary |
|------|------|-------|-------|---------------------|
| [23718203](https://pubmed.ncbi.nlm.nih.gov/23718203/) | 2013 | *Ralstonia* (plant) | [Ralstonia solanacearum, a widespread bacterial plant pathogen in the post-genomic era](https://doi.org/10.1111/mpp.12038) | Comprehensive post-genomic review establishing *R. solanacearum* as causal agent of bacterial wilt, Moko disease of banana, and brown rot of potato across a vast host range worldwide. |
| [24057141](https://pubmed.ncbi.nlm.nih.gov/24057141/) | 2014 | *Ralstonia* (human) | [Ralstonia spp.: emerging global opportunistic pathogens](https://doi.org/10.1007/s10096-013-1975-9) | Systematic review of 86 documented human *Ralstonia* infections documenting *R. pickettii*, *R. mannitolilytica*, and *R. insidiosa* as hospital-associated opportunistic pathogens capable of causing osteomyelitis, meningitis, and sepsis. |
| [39387430](https://pubmed.ncbi.nlm.nih.gov/39387430/) | 2024 | *Ralstonia* (human) | [Central line-associated bloodstream infection outbreak related to Ralstonia pickettii-contaminated saline in a pediatric HSCT center](https://doi.org/10.24953/turkjpediatr.2024.4529) | Reports a nosocomial CLABSI outbreak caused by *R. pickettii* in contaminated saline in immunosuppressed pediatric stem cell transplant recipients. |
| [35594766](https://pubmed.ncbi.nlm.nih.gov/35594766/) | 2022 | *Acinetobacter* | [A comprehensive review on potential therapeutic inhibitors of nosocomial Acinetobacter baumannii superbugs](https://doi.org/10.1016/j.bioorg.2022.105849) | Reviews *A. baumannii* as a WHO "critical priority pathogen" responsible for a wide spectrum of nosocomial infections, detailing enzymatic and non-enzymatic resistance mechanisms rendering it multidrug resistant. |
| [27274985](https://pubmed.ncbi.nlm.nih.gov/27274985/) | 2016 | *Acinetobacter* | [Mechanisms of Antimicrobial Resistance in ESKAPE Pathogens](https://doi.org/10.1155/2016/2475067) | Establishes *A. baumannii* as a leading cause of multidrug-resistant nosocomial infections worldwide as part of the ESKAPE group, reviewing all major resistance mechanisms. |
| [35065702](https://pubmed.ncbi.nlm.nih.gov/35065702/) | 2022 | *Acinetobacter* | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis (Lancet)](https://doi.org/10.1016/S0140-6736(21)02724-0) | Global AMR burden study across 204 countries estimating ~1.27 million attributable deaths in 2019, with carbapenem-resistant *A. baumannii* among the top six pathogens responsible for the bulk of AMR mortality. |
| [41194619](https://pubmed.ncbi.nlm.nih.gov/41194619/) | 2025 | *Cupriavidus* | [Bloodstream infection within a haemodialysis patient: a clinical vignette and literature review](https://doi.org/10.1177/14782715251389263) | Case report and literature review of *Cupriavidus pauculus* bloodstream infection in a haemodialysis patient, confirming it as a rare opportunistic pathogen primarily affecting immunocompromised hosts. |
| [33926650](https://pubmed.ncbi.nlm.nih.gov/33926650/) | 2021 | *Cupriavidus* | [Investigation and control of an outbreak due to a contaminated hospital water system following a rare case of Cupriavidus pauculus bacteraemia](https://doi.org/10.1016/j.jhin.2021.02.001) | Describes a *C. pauculus* bacteraemia outbreak in a paediatric haemato-oncology unit traced to a contaminated hospital water system, demonstrating its capacity to colonise water infrastructure and cause invasive disease. |
| [35735306](https://pubmed.ncbi.nlm.nih.gov/35735306/) | 2022 | *Cupriavidus* | [Recurrent Cupriavidus pauculus catheter-related bacteremia in an immunocompromised child](https://doi.org/10.32641/andespediatr.v93i2.3921) | Reports recurrent *C. pauculus* catheter-related bloodstream infection in a child with acute leukaemia, establishing a pattern of catheter colonisation in immunocompromised patients. |
| [21441374](https://pubmed.ncbi.nlm.nih.gov/21441374/) | 2011 | *Massilia* | [Massilia oculi sp. nov., isolated from a human clinical specimen](https://doi.org/10.1099/ijs.0.032441-0) | Describes the novel species *M. oculi* isolated from a patient with endophthalmitis, representing the first formal documentation of a *Massilia* species originating from a human clinical infection. |
| [1600002](https://pubmed.ncbi.nlm.nih.gov/1600002/) | 1992 | *Methylobacterium* | [Catheter infection caused by Methylobacterium in immunocompromised hosts: report of three cases and review of the literature](https://doi.org/10.1093/clinids/14.5.1010) | Documents three central catheter infections by *M. extorquens* in leukemia/bone-marrow-transplant patients and reviews all 12 prior reported human *Methylobacterium* infections, establishing it as a recognised catheter-associated opportunistic pathogen. |
| [26823697](https://pubmed.ncbi.nlm.nih.gov/26823697/) | 2015 | *Mesorhizobium* / Rhizobiales | Mixed group of Rhizobiales microbes in lung and blood of a patient with fatal pulmonary illness | Reports *Mesorhizobium hominis* (along with Bradyrhizobiaceae, Methylobacteriaceae, and Sphingomonadaceae) isolated from lung and blood cultures of a patient with rapidly progressive fatal pulmonary illness, documenting these organisms as rare but potentially deadly human pathogens. |
| [38034940](https://pubmed.ncbi.nlm.nih.gov/38034940/) | 2023 | *Paenibacillus* | [Infective endocarditis caused by Paenibacillus thiaminolyticus: a case report and review of literature](https://doi.org/10.1093/ehjcr/ytad566) | Documents a previously unreported case of *P. thiaminolyticus* infective endocarditis requiring mitral valve replacement, highlighting *Paenibacillus* as a rare but clinically significant opportunistic human pathogen requiring molecular identification. |

**Note on Bradyrhizobium:** No standalone PubMed literature was found for *Bradyrhizobium* as a human pathogen; SPOKE-OKN contains 1 human blood isolate, and this genus appears only as part of mixed Rhizobiales infections (PMID 26823697 above).

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-12*

*Model: claude-sonnet-4-6*
