# Chemical Compound Identifiers in Knowledge Graphs - Chat Transcript

## Finding Knowledge Graphs with Chemical Compound Information

👤 **User**  
Find KGs that have information about chemical compounds, in particular look for common chemical identifiers. Create a table with the KG name, the URI, and the type of chemical identifier.

---

🧠 **Assistant**  
I'll search through the available knowledge graphs to find ones that contain information about chemical compounds and their identifiers.

After examining multiple knowledge graphs, I found several that contain chemical compound information:

| KG Name | URI | Chemical Identifiers |
|---------|-----|---------------------|
| **BioBricks ICE** | https://frink.apps.renci.org/biobricks-ice/sparql | **EPA DSSTox ID (DTXSID)**, UMLS Concept IDs, Entrez Gene IDs (for targets) |
| **BioBricks ToxCast** | https://frink.apps.renci.org/biobricks-toxcast/sparql | **EPA DSSTox ID (DTXSID)**, **InChIKey** |
| **BioBricks Tox21** | https://frink.apps.renci.org/biobricks-tox21/sparql | **CAS Registry Number** (via identifiers.org URIs) |
| **BioBricks PubChem Annotations** | https://frink.apps.renci.org/biobricks-pubchem-annotations/sparql | **PubChem Compound ID (CID)**, InChI, InChIKey, SMILES, Molecular Formula, Chemical Names |
| **BioBricks AOP-Wiki** | https://frink.apps.renci.org/biobricks-aopwiki/sparql | **CAS Registry Number**, **InChI**, **InChIKey**, **PubChem Compound ID**, **ChEBI ID**, **SMILES** (with cross-references to ChEMBL, KEGG, Wikidata) |
| **BioBricks MeSH** | https://frink.apps.renci.org/biobricks-mesh/sparql | MeSH Descriptor IDs for chemicals (Category D - Chemicals and Drugs), Supplementary Concept Records for specific substances |

**Key Chemical Identifier Types Found:**

1. **EPA DSSTox ID (DTXSID)** - EPA's standardized identifier for toxicity testing
2. **CAS Registry Number** - Chemical Abstracts Service registry numbers
3. **InChI/InChIKey** - International Chemical Identifier (textual and hashed versions)
4. **PubChem Compound ID (CID)** - NCBI PubChem database identifiers
5. **ChEBI ID** - Chemical Entities of Biological Interest identifiers
6. **SMILES** - Simplified Molecular Input Line Entry System
7. **MeSH Descriptors** - Medical Subject Headings for chemicals
8. **Molecular Formula** - Chemical formula notation

The BioBricks suite provides the most comprehensive chemical coverage, with ICE, ToxCast, and Tox21 focusing on toxicology data, PubChem Annotations providing broader chemical information, and AOP-Wiki connecting chemicals to adverse outcome pathways with extensive cross-referencing.

---

## Adding SPOKE-OKN and SAWGraph

👤 **User**  
@spoke-okn, @sawgraph have chemical entities. Add them to the table

---

🧠 **Assistant**  
After examining SPOKE-OKN and SAWGraph knowledge graphs, here's the updated comprehensive table:

| KG Name | URI | Chemical Identifiers |
|---------|-----|---------------------|
| **BioBricks ICE** | https://frink.apps.renci.org/biobricks-ice/sparql | **EPA DSSTox ID (DTXSID)**, UMLS Concept IDs, Entrez Gene IDs (for targets) |
| **BioBricks ToxCast** | https://frink.apps.renci.org/biobricks-toxcast/sparql | **EPA DSSTox ID (DTXSID)**, **InChIKey** |
| **BioBricks Tox21** | https://frink.apps.renci.org/biobricks-tox21/sparql | **CAS Registry Number** (via identifiers.org URIs) |
| **BioBricks PubChem Annotations** | https://frink.apps.renci.org/biobricks-pubchem-annotations/sparql | **PubChem Compound ID (CID)**, InChI, InChIKey, SMILES, Molecular Formula, Chemical Names |
| **BioBricks AOP-Wiki** | https://frink.apps.renci.org/biobricks-aopwiki/sparql | **CAS Registry Number**, **InChI**, **InChIKey**, **PubChem Compound ID**, **ChEBI ID**, **SMILES** (with cross-references to ChEMBL, KEGG, Wikidata) |
| **BioBricks MeSH** | https://frink.apps.renci.org/biobricks-mesh/sparql | MeSH Descriptor IDs for chemicals (Category D - Chemicals and Drugs), Supplementary Concept Records for specific substances |
| **SPOKE-OKN** | https://frink.apps.renci.org/spoke-okn/sparql | **ChEMBL Compound ID**, **ChEBI ID**, **DrugBank ID**, **SMILES** (standardized and regular), Synonyms |
| **SAWGraph** | https://frink.apps.renci.org/sawgraph/sparql | **CAS Registry Number**, Substance IDs (internal), PFAS-specific compound identifiers |

**Key Chemical Identifier Types Found:**

1. **EPA DSSTox ID (DTXSID)** - EPA's standardized identifier for toxicity testing
2. **CAS Registry Number** - Chemical Abstracts Service registry numbers
3. **InChI/InChIKey** - International Chemical Identifier (textual and hashed versions)
4. **PubChem Compound ID (CID)** - NCBI PubChem database identifiers
5. **ChEBI ID** - Chemical Entities of Biological Interest identifiers
6. **ChEMBL Compound ID** - European Bioinformatics Institute drug database identifiers
7. **DrugBank ID** - Drug and drug target database identifiers
8. **SMILES** - Simplified Molecular Input Line Entry System
9. **MeSH Descriptors** - Medical Subject Headings for chemicals
10. **Molecular Formula** - Chemical formula notation

**Notes:**
- **SPOKE-OKN** focuses on biomedical compounds including drugs with ChEMBL and DrugBank identifiers
- **SAWGraph** specializes in PFAS contamination monitoring with CAS numbers for environmental contaminants
- The BioBricks suite provides comprehensive toxicology-focused chemical data
- Cross-referencing between KGs is possible via shared identifiers like CAS numbers, ChEBI IDs, and InChI/InChIKeys

---

## Detailed Schema Verification

👤 **User**  
Check the schemas you retrieved for any compounds or chemical entities or CAS numbers

---

🧠 **Assistant**  
After detailed examination of the actual data and schemas in each knowledge graph, here's the verified and comprehensive table:

| KG Name | URI | Chemical Identifier Types (Verified in Data) |
|---------|-----|---------------------------------------------|
| **BioBricks ICE** | https://frink.apps.renci.org/biobricks-ice/sparql | **EPA DSSTox ID (DTXSID)** - used as URI in chemical entities<br>CHEMINF classes: Chemical Identifier (000446), Chemical Structure Descriptor (000568), Chemical Information (000000) |
| **BioBricks ToxCast** | https://frink.apps.renci.org/biobricks-toxcast/sparql | **EPA DSSTox ID (DTXSID)** - used as URI in chemical structure descriptors<br>**CAS Registry Number** - via identifiers.org/cas URIs<br>CHEMINF classes: Chemical Identifier (000446), Chemical Structure Descriptor (000568) |
| **BioBricks Tox21** | https://frink.apps.renci.org/biobricks-tox21/sparql | **CAS Registry Number** - via identifiers.org/cas URIs (primary identifier)<br>CHEMINF class: Chemical Identifier (000446) |
| **BioBricks PubChem Annotations** | https://frink.apps.renci.org/biobricks-pubchem-annotations/sparql | **PubChem Compound ID (CID)** - in compound URIs<br>Annotations link to PubChem compounds; specific chemical properties in annotation bodies |
| **BioBricks AOP-Wiki** | https://frink.apps.renci.org/biobricks-aopwiki/sparql | *Currently empty/no data available*<br>Schema indicates support for: CAS, InChI, InChIKey, PubChem CID, ChEBI ID, SMILES |
| **BioBricks MeSH** | https://frink.apps.renci.org/biobricks-mesh/sparql | **MeSH Descriptor IDs** for chemicals (Category D)<br>**Supplementary Concept Records** for specific chemical substances<br>Tree numbers for hierarchical classification |
| **SPOKE-OKN** | https://frink.apps.renci.org/spoke-okn/sparql | **InChIKey** - primary URI format for chemical entities<br>**ChEMBL Compound ID** - via hasDbXref cross-references<br>**DrugBank ID** - via hasDbXref cross-references<br>**PubChem Compound ID** - via hasDbXref<br>**KEGG Compound ID** - via hasDbXref<br>**KEGG Drug ID** - via hasDbXref<br>**BioCyc ID** - via hasDbXref<br>**PDB Ligand ID** - via hasDbXref<br>**SMILES** - as property values (smiles, standardized_smiles) |
| **SAWGraph** | https://frink.apps.renci.org/sawgraph/sparql | **CAS Registry Number** - via coso:casNumber property<br>**Substance ID** - via coso:substanceID property<br>Focuses on PFAS compounds and environmental contaminants |

**Key Findings:**

1. **CAS Registry Numbers** are used across multiple KGs (ToxCast, Tox21, SAWGraph) as a common identifier
2. **EPA DSSTox IDs (DTXSID)** are the primary identifier in toxicology-focused KGs (ICE, ToxCast)
3. **SPOKE-OKN uses InChIKey as the primary URI** with extensive cross-references to other databases
4. **PubChem Compound IDs** appear in multiple KGs as cross-references
5. **CHEMINF ontology classes** (000446, 000568, 000000) are used in BioBricks toxicology KGs
6. **identifiers.org** is commonly used as a namespace for chemical identifiers
7. **BioBricks AOP-Wiki** endpoint appears to be empty despite having a comprehensive schema

**Cross-referencing potential:** CAS numbers, PubChem CIDs, ChEBI IDs, and InChIKeys can enable federation between these knowledge graphs.

**Example Data Patterns Found:**

**BioBricks ToxCast - CAS Numbers:**
```
http://identifiers.org/cas/100-00-5
http://identifiers.org/cas/100-01-6
```

**BioBricks ICE - DTXSID:**
```
https://comptox.epa.gov/dashboard/chemical/details/DTXSID80875834
https://comptox.epa.gov/dashboard/chemical/details/DTXSID6064084
```

**SPOKE-OKN - InChIKey with cross-references:**
```
Subject: http://rdf.ncbi.nlm.nih.gov/pubchem/inchikey/CXOFVDLJLONNDW-UHFFFAOYSA-N
Cross-reference: http://identifiers.org/drugbank/DB00252
Cross-reference: http://identifiers.org/chembl.compound/CHEMBL496
Cross-reference: http://identifiers.org/pubchem.compound/3598
```

**SAWGraph - CAS Numbers for PFAS:**
```
PFHXS: CAS 108427538
PFDS: CAS 126105348
```

---

👤 **User**  
create a transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on 2025-12-16*
