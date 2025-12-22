# Chat Transcript
## Climate Models Knowledge Graph Schema Visualization

---

👤 **User**  
@climatemodelskg

---

🧠 **Assistant**  
I'd be happy to help you explore the climate models knowledge graph. Let me first get information about this knowledge graph.

## Climate Models KG

Welcome! You've connected to the **Climate Models Knowledge Graph**, a resource designed to support evaluation and development of climate models. 

Here's what this knowledge graph contains:

- **1.4 million triples** describing **55,890 entities** across **48 classes**
- **394 climate model sources** (GCMs, RCMs) linked to **481 experiments**
- **132 research institutes** and **2,907 climate variables**
- Extensive geographic coverage: **30,062 cities**, **252 countries**, and **3,893 subdivisions**
- Regional climate models covering approximately **400,000 geographic locations**
- Support for **CMIP6-related research** and regional climate modeling studies

**Contact:** Aayush Acharya  
**Funding:** [NSF Award #2333789](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333789)

---

### What would you like to explore?

I can help you with queries such as:
- Finding climate models and their experiments
- Exploring variables and measurements
- Looking up geographic coverage
- Examining relationships between institutes, models, and experiments
- Visualizing the schema structure

Would you like me to show you the schema, run a specific query, or explore a particular aspect of climate modeling data?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
Here's the schema visualization for the **Climate Models Knowledge Graph**:

```mermaid
classDiagram
    direction TB

    class Source {
        name
        uuid
    }
    
    class RCM {
        name
        rcm_version
        clm
        clmid
    }
    
    class Experiment {
        experiment_title
        id
    }
    
    class ExperimentFamily {
        name
    }
    
    class SubExperiment {
        name
    }
    
    class Institute {
        name
    }
    
    class Variable {
        name
        cf_standard_name
        variable_long_name
        variable_units
    }
    
    class Domain {
        name
        north
        south
        east
        west
    }
    
    class Realm {
        name
    }
    
    class Forcing {
        name
    }
    
    class Frequency {
        name
    }
    
    class Resolution {
        name
    }
    
    class PhysicalScheme {
        name
    }
    
    class SourceComponent {
        name
    }
    
    class SourceType {
        name
    }
    
    class Model {
        name
    }
    
    class Method {
        name
    }
    
    class Metric {
        name
    }
    
    class Result {
        name
    }
    
    class Task {
        name
    }
    
    class Problem {
        name
    }
    
    class Innovation {
        name
    }
    
    class Paper {
        title
        paper_id
    }
    
    class Field {
        name
    }
    
    class Keyword {
        name
    }
    
    class ObservationalDataset {
        name
    }
    
    class Project {
        name
    }
    
    class Activity {
        name
    }
    
    class MIPEra {
        name
    }
    
    class Ensemble {
        name
    }
    
    class Member {
        name
    }
    
    class SimulationType {
        name
    }
    
    class GridLabel {
        name
    }
    
    class Country {
        name
        iso
        iso3
        continent
        capital
        population
    }
    
    class Country_Subdivision {
        name
        code
    }
    
    class City {
        name
        latitude
        longitude
        population
        elevation
    }
    
    class Continent {
        name
    }
    
    class PhysicalFeature {
        name
    }
    
    class Natural_Hazard {
        name
    }
    
    class NaturalHazardType {
        name
    }
    
    class Weather_Event {
        name
    }
    
    class Teleconnection {
        name
    }
    
    class Ocean_Circulation {
        name
    }
    
    class Water_Bodies {
        name
    }
    
    class Platform {
        name
    }
    
    class Instrument {
        name
    }
    
    class No_Country_Region {
        name
    }

    Source --> Experiment : USED_IN_EXPERIMENT
    Source --> Institute : PRODUCED_BY_INSTITUTE
    Source --> Variable : PRODUCES_VARIABLE
    Source --> SourceType : IS_OF_TYPE
    Source --> SourceComponent : HAS_SOURCE_COMPONENT
    Source --> Realm : FOCUSES_ON_REALM
    Source --> Source : HAS_SUBSEQUENT_VERSION
    
    RCM --> Domain : COVERS_DOMAIN
    RCM --> Source : DRIVEN_BY_SOURCE
    RCM --> PhysicalScheme : USES_PHYSICAL_SCHEME
    RCM --> Resolution : HAS_SPATIAL_RESOLUTION
    RCM --> Institute : PRODUCED_BY_INSTITUTE
    RCM --> Variable : PRODUCES_VARIABLE
    RCM --> Frequency : SAMPLED_AT_FREQUENCY
    RCM --> Forcing : USES_FORCING
    
    Experiment --> Institute : PERFORMED_BY_INSTITUTE
    Experiment --> ExperimentFamily : PART_OF_PROJECT
    Experiment --> SubExperiment : HAS_SUB_EXPERIMENT
    Experiment --> Activity : GENERATED_BY_ACTIVITY
    Experiment --> MIPEra : BELONGS_TO_MIP_ERA
    Experiment --> Realm : APPLIES_TO_REALM
    
    Variable --> Realm : APPLIES_TO_REALM
    Variable --> Frequency : SAMPLED_AT_FREQUENCY
    
    Domain --> Country : COVERS_REGION
    Domain --> City : COVERS_REGION
    
    Ensemble --> Member : INCLUDES_ENSEMBLE_MEMBER
    Ensemble --> Experiment : INCLUDES_EXPERIMENT
    
    Member --> Source : ASSOCIATED_WITH_MEMBER
    
    Paper --> Method : PAPER_APPLIES_METHOD
    Paper --> Model : PAPER_HAS_MODEL
    Paper --> Field : PAPER_BELONGS_TO_FIELD
    Paper --> Keyword : PAPER_HAS_KEYWORD
    Paper --> Result : PAPER_HAS_RESULT
    Paper --> Problem : PAPER_SOLVES_PROBLEM
    Paper --> Task : PAPER_WORKS_ON_TASK
    Paper --> Metric : PAPER_USES_METRIC
    Paper --> Innovation : PAPER_HAS_INNOVATION
    Paper --> ObservationalDataset : PAPER_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
    
    Method --> Model : METHOD_USES_MODEL
    Method --> Result : METHOD_HAS_RESULT
    Method --> Problem : METHOD_SOLVES_PROBLEM
    Method --> Task : METHOD_WORKS_ON_TASK
    Method --> Metric : METHOD_USES_METRIC
    Method --> Innovation : METHOD_HAS_INNOVATION
    Method --> ObservationalDataset : METHOD_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
    
    Model --> Result : MODEL_HAS_RESULT
    Model --> Problem : MODEL_SOLVES_PROBLEM
    Model --> Task : MODEL_WORKS_FOR_TASK
    Model --> Metric : MODEL_USES_METRIC
    Model --> ObservationalDataset : MODEL_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
    
    Task --> Problem : TASK_FACES_PROBLEM
    Task --> Metric : TASK_USES_METRIC
    Task --> ObservationalDataset : TASK_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
    
    Result --> Metric : RESULT_HAS_METRIC
    
    City --> Country : IN_COUNTRY
    City --> Country_Subdivision : IN_COUNTRY
    
    Country --> Continent : IN_CONTINENT
    
    Country_Subdivision --> Country : IN_COUNTRY
    
    Institute --> Country : IN_COUNTRY
    Institute --> Activity : PARTICIPATED_IN
    
    PhysicalScheme --> PhysicalFeature : HAS_PHYSICAL_FEATURE
    PhysicalScheme --> Metric : HAS_METRIC
    PhysicalScheme --> SimulationType : HAS_SIMULATION_TYPE
    PhysicalScheme --> PhysicalScheme : INHERITED_FROM
```

## Schema Overview

The Climate Models KG is organized around several key conceptual areas:

**Climate Modeling Core**
- **Source** (GCMs) and **RCM** (Regional Climate Models) are central entities that produce Variables and are used in Experiments
- **Experiment** links to Institutes, Activities, and MIP Eras (like CMIP6)
- **PhysicalScheme** captures the physical parameterizations used by models

**Research & Publications**
- **Paper** connects to Methods, Models, Tasks, Problems, and Results
- Supports tracking of research innovations and metrics

**Geographic Coverage**
- Hierarchical geography: **Continent** → **Country** → **Country_Subdivision** → **City**
- **Domain** defines spatial extents (north/south/east/west bounds)
- Natural features: hazards, weather events, teleconnections, ocean circulation

**Model Configuration**
- **Forcing**, **Frequency**, **Resolution**, **GridLabel** describe model setup
- **Ensemble** and **Member** track ensemble runs

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 for the Climate Models KG using claude-opus-4-5-20251101 on 2025-12-21*
