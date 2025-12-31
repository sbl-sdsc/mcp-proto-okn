# SPOKE-OKN Schema Visualization

## Chat Transcript

👤 **User**  
@spoke-okn

---

🧠 **Assistant**  
I'll help you explore the SPOKE-OKN knowledge graph! Let me first get some information about this resource.

Great! I can help you work with the **SPOKE-OKN (SPOKE Open Knowledge Network)** knowledge graph. This is a comprehensive biomedical and environmental health knowledge graph that integrates diverse data across genomics, environmental science, and public health.

**Key features of SPOKE-OKN:**
- Integrates data on organisms, genes, diseases, chemical compounds, social determinants of health, and environmental contexts
- Includes detailed geographic information (countries down to ZIP codes)
- Supports spatial analyses of health outcomes, environmental exposures, and socioeconomic factors
- Maintained by the Baranzini Lab at UCSF

**What would you like to explore?** I can help you:
- Understand what types of data are available (genes, diseases, locations, environmental factors, etc.)
- Search for specific information (e.g., genes related to diseases, environmental exposures in certain areas)
- Analyze relationships between different entities
- Visualize the knowledge graph structure

Would you like me to show you the schema to see what kinds of data and relationships are available, or do you have a specific question you'd like to explore?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
I'll visualize the schema for you. Let me first get the schema information and then create a visual diagram.

```mermaid
classDiagram
direction TB

class SDoH {
    data_source
    domain
    mesh_ids
    topic
}

class AdministrativeArea {
    abbr
    city_fips
    code
    county_fips
    iso3
    latitude
    longitude
    state
    state_fips
    state_name
    zipcode_type
}

class ChemicalEntity {
    max_phase
    smiles
    standardized_smiles
    synonyms
}

class Disease {
    mesh_list
    omim_list
}

class EnvironmentalFeature {
    synonyms
}

class Gene {
    ensembl
}

class OrganismTaxon {
    antimicrobial_resistance
    biovar
    collection_date
    disease
    genbank_accessions
    genome_size
    gram_stain
    has_amr_phenotype
    host_age
    host_gender
    host_health
    host_is_human
    host_name
    is_resistant
    isolation_country
    isolation_source
    level
    motility
    oxygen_requirement
    pathovar
    salinity
    serovar
    sporulation
    strain
    temperature_range
    usa_isolation_country
}

class CONTRAINDICATES_CcD {
    Activity Sources
}

class TREATS_CtD {
    Activity Sources
    Phase
}

class ASSOCIATES_SaD {
    Co-occurrence
    Enrichment
    Fisher's Test
    Odds Ratio
}

class RESEMBLES_DrD {
    Co-occurrence
    Enrichment
    Fisher's Test
    Odds Ratio
}

class PREVALENCE_DpL {
    Data Value
    Data Value Type
    Data Value Unit
    Location Name
    Lower Bound
    Metric Name
    Short Question Text
    State Abbreviation
    State Description
    Total Population
    Upper Bound
    Value
    Year
}

class FOUNDIN_CfL {
    Date
    Date Type
    Media
    Metrics
    Unit
    Value
    Year
}

class INTERACTS_CiC {
    Drug-Drug Interaction Risk
}

class MORTALITY_DmL {
    Global Health Estimate Code
    Mortality Per 100k
    Population
    Usability
    Value
}

class RESPONDS_TO_OrC {
    Laboratory Typing Method
    Laboratory Typing Platform
    Measurement Sign
    Measurement Unit
    Measurement Value
    Resistant Phenotype
    Testing Standard Year
    Vendor
}

class PREVALENCEIN_SpL {
    Method
    Value
    Variable
    Year
}

class FOUNDIN_EfL {
    Metrics
    Unit
    Value
    Year
}

class PARTOF_LpL {
    Percent of Place Area in ZIP
    Percent of ZIP Area in Place
}

SDoH --> SDoH : ISA_SiS
Disease --> Disease : ISA_DiD
ChemicalEntity --> ChemicalEntity : ISA_CiC
EnvironmentalFeature --> EnvironmentalFeature : ISA_EiE
AdministrativeArea --> AdministrativeArea : PARTOF_LpL_simple
ChemicalEntity --> ChemicalEntity : PARTOF_CpC

ChemicalEntity --> FOUNDIN_CfL
FOUNDIN_CfL --> AdministrativeArea

EnvironmentalFeature --> FOUNDIN_EfL
FOUNDIN_EfL --> AdministrativeArea

OrganismTaxon --> AdministrativeArea : ISOLATEDIN_OiL

Disease --> PREVALENCE_DpL
PREVALENCE_DpL --> AdministrativeArea

SDoH --> PREVALENCEIN_SpL
PREVALENCEIN_SpL --> AdministrativeArea

Disease --> MORTALITY_DmL
MORTALITY_DmL --> AdministrativeArea

Disease --> Gene : ASSOCIATES_DaG

SDoH --> ASSOCIATES_SaD
ASSOCIATES_SaD --> Disease

ChemicalEntity --> TREATS_CtD
TREATS_CtD --> Disease

ChemicalEntity --> CONTRAINDICATES_CcD
CONTRAINDICATES_CcD --> Disease

ChemicalEntity --> INTERACTS_CiC
INTERACTS_CiC --> ChemicalEntity

ChemicalEntity --> Gene : UPREGULATES_CuG
ChemicalEntity --> Gene : DOWNREGULATES_CdG

Gene --> Disease : EXPRESSEDIN_GeiD

OrganismTaxon --> RESPONDS_TO_OrC
RESPONDS_TO_OrC --> ChemicalEntity

Gene --> ChemicalEntity : RESISTANT_TO_mGrC
Gene --> ChemicalEntity : RESPONSE_TO_mGrC
Gene --> ChemicalEntity : ADVRESPONSE_TO_mGarC

Gene --> Disease : MARKER_POS_GmpD
Gene --> Disease : MARKER_NEG_GmnD

Disease --> RESEMBLES_DrD
RESEMBLES_DrD --> Disease

ChemicalEntity --> ChemicalEntity : HASROLE_ChC

AdministrativeArea --> PARTOF_LpL
PARTOF_LpL --> AdministrativeArea
```

Here's a visual representation of the SPOKE-OKN knowledge graph schema! 

**Key Components:**

**7 Main Entity Types:**
- **SDoH** (Social Determinants of Health) - social and economic factors affecting health
- **AdministrativeArea** - geographic locations (countries, states, counties, ZIP codes)
- **ChemicalEntity** - drugs and chemical compounds
- **Disease** - disorders and illnesses
- **EnvironmentalFeature** - environmental quality entities
- **Gene** - units of heredity
- **OrganismTaxon** - bacterial strains and organisms

**Relationship Types:**
- **Simple arrows** show direct relationships (e.g., Gene → Disease, Chemical → Gene)
- **Box-shaped relationships** contain edge properties - these store quantitative data on the relationships themselves (like disease prevalence values, drug interaction risk levels, mortality rates, etc.)

The diagram shows how SPOKE-OKN integrates biomedical, environmental, and geographic data to support research on health outcomes, environmental exposures, and social determinants of health.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 on 2025-12-31*

Model: claude-sonnet-4-20250514
