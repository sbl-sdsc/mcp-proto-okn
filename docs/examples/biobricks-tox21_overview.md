# Chat Transcript: BioBricks Tox21 Knowledge Graph Exploration

👤 **User**  
@biobricks-tox21

---

🧠 **Assistant**  
I'll get information about this knowledge graph for you.

Great! This is the **BioBricks Tox21** knowledge graph - an open knowledge graph that contains Tox21 toxicology screening data. 

Here's what it contains:

**Overview:**
- Transforms Tox21 quantitative high-throughput screening (qHTS) data into structured RDF format
- Contains over 120 million chemical assay data points across 70+ distinct assays
- Evaluates potential toxicity of approximately 10,000 diverse chemicals
- Represents 8,947 chemical entities with ~27,000 triples

**Key Features:**
- Uses Chemical Information Ontology (CHEMINF) classes to describe compounds
- Each chemical is identified using standardized CAS Registry Numbers
- Links to Tox21 source data via identifiers.org URIs
- Public Domain license (CC0-1.0)

**Purpose:**
Developed by Insilica LLC as part of an NSF-funded project to harmonize chemical safety data for researchers, regulatory agencies, and pharmaceutical companies.

**Access:**
- SPARQL endpoint: https://frink.apps.renci.org/biobricks-tox21/sparql
- Contact: Tom Luechtefeld (tom@insilica.co)

Would you like me to explore the schema to see what kinds of queries you can run, or would you like to search for specific toxicology information?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
I'll visualize the schema for you. Let me first get the schema details and then create a cleaned diagram.

Here's the schema visualization for the BioBricks Tox21 knowledge graph:

```mermaid
classDiagram
    class ChemicalIdentifier["Chemical Identifier"] {
        +label: String
        +source: URI
    }
    
    ChemicalIdentifier : CHEMINF_000446
    ChemicalIdentifier --|> type : rdf:type
    ChemicalIdentifier --|> label : rdfs:label
    ChemicalIdentifier --|> source : dc:source
```

The schema is relatively simple and focused:

**Main Class:**
- **Chemical Identifier** (CHEMINF_000446): Represents unique codes or numbers that identify specific chemical substances (like CAS registry numbers)

**Properties:**
- **label** (rdfs:label): Human-readable name or title for the chemical compound
- **source** (dc:source): The origin or reference database for chemical information
- **type** (rdf:type): Specifies the category or class the chemical entity belongs to

This streamlined schema makes sense for the Tox21 data - it's primarily focused on identifying and cataloging chemicals with their standardized identifiers and linking them to their source data. Would you like to explore what kinds of chemicals are in the dataset or run some queries?

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 using claude-sonnet-4-5-20250929 on 2025-12-22*
