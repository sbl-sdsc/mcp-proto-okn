# BioBricks Tox21 Knowledge Graph - Chat Transcript

**Date:** December 22, 2025

---

## User
@biobricks-tox21

## Claude
I'll help you explore the BioBricks Tox21 knowledge graph. Let me first get information about this resource.

[Retrieved knowledge graph description and schema]

Great! I now have access to the **BioBricks Tox21** knowledge graph. This is an open knowledge graph for Tox21 toxicology screening data, containing information about approximately 10,000 chemical compounds tested across 70+ distinct assays.

**About BioBricks Tox21:**
- Contains ~27,000 triples describing 8,947 chemical entities
- Data comes from the Tox21 quantitative high-throughput screening (qHTS) program
- Over 120 million chemical assay data points from toxicity testing
- Chemicals are identified using standardized CAS Registry Numbers
- Developed by Insilica LLC under NSF Award #2333728
- Released under CC0-1.0 (Public Domain) license

**What can I help you explore?**
- Chemical compounds and their identifiers (CAS numbers)
- Toxicology screening data
- Specific chemicals or assay results
- Statistics about the dataset

Would you like me to:
1. Show you some example chemicals in the dataset?
2. Search for specific compounds?
3. Visualize the knowledge graph structure?
4. Query specific toxicology information?

---

## User
Visualize the schema

## Claude
Here's the schema visualization for the BioBricks Tox21 knowledge graph!

**Key Schema Components:**

**Main Class:**
- **Chemical Identifier** (CHEMINF_000446) - Represents unique codes or numbers that identify specific chemical substances, such as CAS registry numbers

**Properties (Predicates):**
- **rdfs:label** - Human-readable name or title for a chemical compound
- **dc:source** - The origin or reference database for chemical information (links to Tox21 public data)
- **rdf:type** - Specifies the category or class a chemical entity belongs to

**Dataset Statistics:**
- ~8,947 chemical entities
- ~27,000 triples total
- Data from Tox21 qHTS 10K library

The schema is relatively simple but focused, using the Chemical Information Ontology (CHEMINF) to represent chemical identifiers and standard RDF/RDFS properties for labeling and typing. Each chemical is identified using standardized CAS Registry Numbers through identifiers.org URIs.

[Created Mermaid class diagram: biobricks-tox21-schema.mermaid]

Would you like me to run some example queries to show you what kind of data is actually stored in the knowledge graph?

---

## Knowledge Graph Information

**Knowledge Graph:** BioBricks Tox21  
**SPARQL Endpoint:** https://frink.apps.renci.org/biobricks-tox21/sparql  
**Homepage:** https://github.com/biobricks-ai/biobricks-okg  
**Funding:** NSF Award #2333728  
**Contact:** Tom Luechtefeld (tom@insilica.co)  
**License:** CC0-1.0 (Public Domain)

**Data Source:**
- Tox21 Public Data: https://tripod.nih.gov/pubdata/
- Public Domain (CC0-1.0)

**Description:**
BioBricks Tox21 is an open knowledge graph that transforms the Tox21 quantitative high-throughput screening (qHTS) 10K library data into structured, machine-readable RDF format. The source dataset contains over 120 million chemical assay data points across 70+ distinct assays for evaluating potential toxicity of approximately 10,000 diverse chemicals.

---

**End of Transcript**
