# BioBricks MeSH Knowledge Graph Exploration

👤 **User**  
@biobricks-mesh

---

🧠 **Assistant**  
I'll help you explore the BioBricks MeSH knowledge graph! Let me start by getting information about this knowledge graph.

**BioBricks MeSH** is an open knowledge graph containing Medical Subject Headings (MeSH) from the U.S. National Library of Medicine.

## What's in BioBricks MeSH?

This knowledge graph contains:
- **18.1 million triples** representing 2.4 million biomedical entities
- **862,579 terms** with rich labels and descriptions
- **464,362 concepts** organized hierarchically
- **249,243 chemical substance records**
- **66,110 organisms**
- **29,940 topical descriptors**
- **6,750 diseases**

## Main Categories

The data is organized into major branches:
- **[A] Anatomy** - body structures, organs, tissues, cells
- **[B] Organisms** - bacteria, viruses, fungi, plants, animals
- **[C] Diseases** - pathological conditions, syndromes, symptoms
- **[D] Chemicals and Drugs** - compounds, pharmaceuticals, biological substances
- **[E] Techniques and Equipment** - medical procedures, diagnostics, treatments
- **[F] Psychiatry and Psychology** - mental processes, behavioral sciences
- **[G] Phenomena and Processes** - biological, chemical, physical processes
- **[H] Disciplines and Occupations** - fields of study, professions
- **[I-N, V, Z]** - Social sciences, technology, humanities, information science, healthcare, publications, and geography

## What can you do with it?

You can query this knowledge graph to:
- Explore hierarchical relationships between medical terms
- Find related diseases, drugs, and treatments
- Discover pharmacological actions and drug effects
- Navigate the taxonomy of organisms and anatomy
- Search for diagnostic and therapeutic procedures
- Access comprehensive scope notes and definitions

Would you like to explore any specific aspect of this biomedical vocabulary? For example, I can help you find information about specific diseases, drugs, medical procedures, or explore relationships within the MeSH hierarchy.

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  

```mermaid
classDiagram
    class Descriptor {
        +rdfs:label
        +vocab:scopeNote
        +vocab:treeNumber
    }
    
    class TopicalDescriptor {
        Categories A-N
    }
    
    class PublicationType {
        Category V
    }
    
    class GeographicalDescriptor {
        Category Z
    }
    
    class Qualifier {
        +rdfs:label
        Subheadings
    }
    
    class SupplementaryConcept {
        +rdfs:label
        Substances, protocols, rare diseases
    }
    
    class Concept {
        +rdfs:label
        Specific meanings
    }
    
    class Term {
        +rdfs:label
        Names and phrases
    }
    
    class Anatomy_A {
        Body structures
    }
    
    class Organisms_B {
        Bacteria, viruses, fungi
    }
    
    class Diseases_C {
        Pathological conditions
    }
    
    class Chemicals_D {
        Compounds, drugs
    }
    
    class Techniques_E {
        Procedures, equipment
    }
    
    class Psychiatry_F {
        Mental processes
    }
    
    class Phenomena_G {
        Biological processes
    }
    
    class Disciplines_H {
        Fields of study
    }
    
    class Social_I {
        Social sciences
    }
    
    class Technology_J {
        Industry, agriculture
    }
    
    class Humanities_K {
        Arts, history
    }
    
    class Information_L {
        Communication, IT
    }
    
    class NamedGroups_M {
        Demographics
    }
    
    class HealthCare_N {
        Health services
    }
    
    Descriptor <|-- TopicalDescriptor
    Descriptor <|-- PublicationType
    Descriptor <|-- GeographicalDescriptor
    
    TopicalDescriptor <|-- Anatomy_A
    TopicalDescriptor <|-- Organisms_B
    TopicalDescriptor <|-- Diseases_C
    TopicalDescriptor <|-- Chemicals_D
    TopicalDescriptor <|-- Techniques_E
    TopicalDescriptor <|-- Psychiatry_F
    TopicalDescriptor <|-- Phenomena_G
    TopicalDescriptor <|-- Disciplines_H
    TopicalDescriptor <|-- Social_I
    TopicalDescriptor <|-- Technology_J
    TopicalDescriptor <|-- Humanities_K
    TopicalDescriptor <|-- Information_L
    TopicalDescriptor <|-- NamedGroups_M
    TopicalDescriptor <|-- HealthCare_N
    
    Descriptor "1" --> "*" Concept : vocab:concept
    Descriptor "1" --> "1" Concept : vocab:preferredConcept
    Descriptor "*" --> "*" Qualifier : vocab:allowableQualifier
    Descriptor "*" --> "*" Descriptor : vocab:broaderDescriptor
    Descriptor "*" --> "*" Descriptor : vocab:narrowerDescriptor
    Descriptor "*" --> "*" Descriptor : vocab:pharmacologicalAction
    
    Concept "1" --> "*" Term : vocab:term
    Concept "1" --> "1" Term : vocab:preferredTerm
    
    SupplementaryConcept "*" --> "*" Descriptor : vocab:pharmacologicalAction
```

## Schema Overview

This diagram shows the BioBricks MeSH knowledge graph structure:

**Core Structure:**
- **Descriptor** is the main class, with three specialized types: TopicalDescriptor, PublicationType, and GeographicalDescriptor
- **TopicalDescriptor** branches into 14 subject categories (A-N), each representing a major domain of biomedical knowledge
- **Descriptors** connect to **Concepts** (specific meanings), which in turn connect to **Terms** (actual words/phrases)
- **Qualifiers** are subheadings that can modify descriptors to specify aspects like diagnosis, therapy, or adverse effects
- **SupplementaryConcept** records cover specific substances, protocols, and rare diseases

**Key Relationships:**
- Hierarchical navigation through `broaderDescriptor` and `narrowerDescriptor`
- Concept mappings through `preferredConcept` and `concept`
- Term variations through `preferredTerm` and `term`
- Pharmacological actions linking substances to their effects
- Allowable qualifiers specifying which subheadings can be used with each descriptor

This hierarchical structure enables sophisticated queries about medical terminology, drug interactions, disease classifications, and biomedical relationships.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 using claude-sonnet-4-20250514 on 2025-12-22*
