# BioBricks PubChem Annotations Knowledge Graph Exploration

## Chat Transcript

👤 **User**  
@biobricks-pubchem-annotations

---

🧠 **Assistant**  
I'll help you explore the biobricks-pubchem-annotations knowledge graph. Let me start by getting its schema and probing the live endpoint for the actual structure.

The **BioBricks PubChem Annotations** knowledge graph provides structured access to PubChem's *Annotations* subset using the W3C Web Annotation Data Model. It is deliberately simple in shape: a single annotation class connects PubChem chemical records to free-text annotation content drawn from many heterogeneous sources (regulatory limits, physical/chemical properties, toxicology and hazard information, handling and disposal guidance, synonyms, and update history).

The graph contains:
- **~10.7 million annotations** (`oa:Annotation` instances) — the only class in the graph
- Each annotation targets one or more **PubChem compound / substance** URIs (external `rdf.ncbi.nlm.nih.gov` references, not classes defined here)
- Each annotation carries a **body node** holding the annotation's format and its literal text value

**The single class:**
- `oa:Annotation` — a connection between a PubChem compound/substance and a piece of textual content that annotates it

**Main predicates:**
- `oa:hasTarget` — links an annotation to the PubChem compound/substance it describes
- `dc:subject` — the PubChem compound/substance the annotation is about (used alongside `hasTarget`)
- `oa:hasBody` — links an annotation to its body node
- `dc:format` — the media type of the body content (e.g. `text/plain`)
- `rdf:value` — the literal annotation text (the actual regulatory limit, property value, hazard note, synonym, etc.)

Note: the annotation *topics* (toxicology, physical properties, regulatory data, synonyms, …) are **not** separate classes — they are conveyed as the free-text `rdf:value` of the body, so they are discovered by reading the text rather than by class membership.

Would you like me to:
1. Show some example annotations for a compound?
2. Visualize the schema structure?
3. Retrieve all annotation text for a specific PubChem CID?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
Here's the live schema of the BioBricks PubChem Annotations knowledge graph. It is intentionally minimal — one class plus a body node and external PubChem targets:

```mermaid
classDiagram
    class Annotation {
        oa:Annotation
    }
    class Body {
        +dc:format
        +rdf:value
    }
    class PubChemCompound
    class PubChemSubstance

    Annotation --> PubChemCompound : hasTarget / dc:subject
    Annotation --> PubChemSubstance : hasTarget / dc:subject
    Annotation --> Body : hasBody
```

**Key insights from the schema:**

1. **Single hub class.** Every one of the ~10.7 million records is an `oa:Annotation`. There are no specialized annotation subclasses (no ChemicalProperty, Toxicology, Synonym, etc. classes) — those categories live in the annotation text itself.

2. **Targets are external PubChem URIs.** `hasTarget` and `dc:subject` point at `pubchem/compound/CID…` and `pubchem/substance/…` identifiers hosted by NCBI, enabling federation with the wider PubChem RDF ecosystem rather than redefining compounds locally.

3. **Content lives on the body node.** `hasBody` reaches a node whose `dc:format` gives the media type (typically `text/plain`) and whose `rdf:value` holds the literal annotation — for example a state drinking-water limit ("(FL) FLORIDA 4,200 ug/l /Strontium/"), a physical property, a hazard/first-aid note, or a synonym.

4. **Query pattern.** To read everything known about a compound: match `?ann oa:hasTarget <compound> ; oa:hasBody ?b . ?b rdf:value ?text` and scan the returned text.

This makes the graph a large, uniformly-structured bridge from PubChem chemical identifiers to curated free-text knowledge, well suited to text retrieval and to joins with other chemistry/toxicology graphs on PubChem CIDs.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 using claude-opus-4-8 on 2026-07-12*
