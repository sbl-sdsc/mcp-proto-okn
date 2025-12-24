# Chat Transcript
## Exploring the Climate Models Knowledge Graph

👤 **User**  
@climatemodelskg

---

🧠 **Assistant**  
I'll help you explore the Climate Models Knowledge Graph. Let me first get some information about this knowledge graph.

Great! I now have access to the **Climate Models Knowledge Graph**, which integrates structured information about climate models, experiments, and research outputs to support climate science evaluation and development.

## Overview

The Climate Models KG contains:
- **1.4 million triples** describing 55,890 entities across 48 classes
- **394 Sources** (GCMs, RCMs) linked to **481 Experiments**
- **132 Institutes** producing **2,907 climate Variables**
- Extensive geographic coverage: **30,062 Cities**, **252 Countries**, and **3,893 subdivisions**
- Approximately **400,000 geographic locations** for regional climate models
- GeoNames integration for geospatial data
- Custom ontology structuring relationships between models, physical schemes, metrics, and results

## What I Can Help You With

I can query this knowledge graph to help you:

1. **Explore Climate Models**: Find information about specific GCMs (Global Climate Models) or RCMs (Regional Climate Models), their versions, components, and institutes
2. **Discover Experiments**: Search for climate experiments, their parameters, realms, and associated activities
3. **Analyze Variables**: Look up climate variables, their units, frequencies, and which models produce them
4. **Geographic Information**: Query cities, countries, regions with climate data
5. **Research Context**: Find papers, methods, tasks, problems, and innovations in climate science
6. **Relationships**: Understand connections between models, experiments, institutes, and geographic locations

## Example Queries

You could ask me things like:
- "What climate models were developed by a specific institute?"
- "Which experiments focus on ocean realms?"
- "Show me variables related to temperature or precipitation"
- "What are the most common physical schemes used in climate models?"
- "Which cities in a specific country have climate data?"

How would you like to explore the Climate Models Knowledge Graph?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
I'll visualize the schema of the Climate Models Knowledge Graph for you.

Perfect! I've created a visual representation of the Climate Models Knowledge Graph schema. The diagram shows the 47 main classes and their relationships through 134 predicates.

```mermaid
classDiagram
direction TB

class Activity
class City {
  +geonameid
  +name
  +asciiname
  +alternatenames
  +latitude
  +longitude
  +feature_class
  +feature_code
  +country_code
  +admin1_code
  +admin2_code
  +admin3_code
  +admin4_code
  +population
  +elevation
  +dem
  +timezone
  +modification_date
}
class Continent {
  +code
  +name
}
class Country_Subdivision {
  +geonameid
  +name
  +asciiname
  +alternatenames
  +latitude
  +longitude
  +feature_class
  +feature_code
  +country_code
  +admin1_code
  +admin2_code
  +population
  +elevation
  +dem
  +timezone
  +modification_date
}
class Country {
  +iso
  +iso3
  +isonumeric
  +fips
  +name
  +capital
  +area_sqkm
  +population
  +continent
  +tld
  +currencycode
  +currencyname
  +phone
  +postal_code_format
  +postal_code_regex
  +languages
  +geonameid
  +neighbours
  +equivalent_fips_code
}
class Domain
class Ensemble
class Experiment {
  +experiment_title
}
class ExperimentFamily
class Field
class Forcing
class Frequency
class GridLabel
class Innovation
class Institute
class Instrument
class Keyword
class Member
class Method
class Metric
class MIPEra
class Model
class Natural_Hazard
class NaturalHazardType
class No_Country_Region {
  +geonameid
  +name
  +asciiname
  +alternatenames
  +latitude
  +longitude
  +feature_class
  +feature_code
  +population
  +elevation
  +dem
  +timezone
  +modification_date
}
class ObservationalDataset
class Ocean_Circulation
class Paper {
  +paper_id
  +title
}
class PhysicalFeature
class PhysicalScheme
class Platform
class Problem
class Project
class RCM {
  +rcm_version
}
class Realm
class Resolution
class Result
class SimulationType
class Source
class SourceComponent
class SourceType
class SubExperiment
class Task
class Teleconnection
class Variable {
  +variable_long_name
  +variable_units
  +cf_standard_name
}
class Water_Bodies
class Weather_Event

Source --> Realm : APPLIES_TO_REALM
Source --> Member : ASSOCIATED_WITH_MEMBER
Experiment --> MIPEra : BELONGS_TO_MIP_ERA
Source --> Source : CORRESPONDS_TO
Experiment --> Domain : COVERS_DOMAIN
Experiment --> City : COVERS_REGION
Experiment --> Country : COVERS_REGION
Experiment --> Country_Subdivision : COVERS_REGION
Experiment --> No_Country_Region : COVERS_REGION
RCM --> Source : DRIVEN_BY_SOURCE
Experiment --> Realm : FOCUSES_ON_REALM
Variable --> Activity : GENERATED_BY_ACTIVITY
Source --> Metric : HAS_METRIC
Source --> PhysicalFeature : HAS_PHYSICAL_FEATURE
Source --> SimulationType : HAS_SIMULATION_TYPE
Source --> SourceComponent : HAS_SOURCE_COMPONENT
Source --> Resolution : HAS_SPATIAL_RESOLUTION
Experiment --> SubExperiment : HAS_SUB_EXPERIMENT
Source --> Source : HAS_SUBSEQUENT_VERSION
City --> Continent : IN_CONTINENT
City --> Country : IN_COUNTRY
Country_Subdivision --> Country : IN_COUNTRY
No_Country_Region --> Country : IN_COUNTRY
Ensemble --> Member : INCLUDES_ENSEMBLE_MEMBER
ExperimentFamily --> Experiment : INCLUDES_EXPERIMENT
Source --> Source : INHERITED_FROM
Natural_Hazard --> NaturalHazardType : IS_OF_TYPE
Source --> SourceType : IS_OF_TYPE
Method --> ObservationalDataset : METHOD_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
Method --> Innovation : METHOD_HAS_INNOVATION
Method --> Result : METHOD_HAS_RESULT
Method --> Problem : METHOD_SOLVES_PROBLEM
Method --> Metric : METHOD_USES_METRIC
Method --> Model : METHOD_USES_MODEL
Method --> Task : METHOD_WORKS_ON_TASK
Model --> ObservationalDataset : MODEL_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
Model --> Result : MODEL_HAS_RESULT
Model --> Problem : MODEL_SOLVES_PROBLEM
Model --> Metric : MODEL_USES_METRIC
Model --> Task : MODEL_WORKS_FOR_TASK
Paper --> Method : PAPER_APPLIES_METHOD
Paper --> Field : PAPER_BELONGS_TO_FIELD
Paper --> ObservationalDataset : PAPER_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
Paper --> Innovation : PAPER_HAS_INNOVATION
Paper --> Keyword : PAPER_HAS_KEYWORD
Paper --> Model : PAPER_HAS_MODEL
Paper --> Result : PAPER_HAS_RESULT
Paper --> City : PAPER_MENTIONS
Paper --> Country : PAPER_MENTIONS
Paper --> Country_Subdivision : PAPER_MENTIONS
Paper --> Experiment : PAPER_MENTIONS
Paper --> Natural_Hazard : PAPER_MENTIONS
Paper --> No_Country_Region : PAPER_MENTIONS
Paper --> Ocean_Circulation : PAPER_MENTIONS
Paper --> PhysicalFeature : PAPER_MENTIONS
Paper --> Teleconnection : PAPER_MENTIONS
Paper --> Water_Bodies : PAPER_MENTIONS
Paper --> Weather_Event : PAPER_MENTIONS
Paper --> Problem : PAPER_SOLVES_PROBLEM
Paper --> Metric : PAPER_USES_METRIC
Paper --> Task : PAPER_WORKS_ON_TASK
Member --> Ensemble : PART_OF_ENSEMBLE
Experiment --> Project : PART_OF_PROJECT
Institute --> Experiment : PARTICIPATED_IN
Experiment --> Institute : PERFORMED_BY_INSTITUTE
Source --> Institute : PRODUCED_BY_INSTITUTE
Experiment --> Variable : PRODUCES_VARIABLE
Result --> Metric : RESULT_HAS_METRIC
Variable --> Frequency : SAMPLED_AT_FREQUENCY
Task --> ObservationalDataset : TASK_EXPERIMENTS_ON_OBSERVATIONAL_DATASET
Task --> Problem : TASK_FACES_PROBLEM
Task --> Metric : TASK_USES_METRIC
Source --> Experiment : USED_IN_EXPERIMENT
Source --> Forcing : USES_FORCING
Source --> PhysicalScheme : USES_PHYSICAL_SCHEME
```

## Key Schema Highlights:

**Core Climate Modeling Entities:**
- **Source** (climate models): Central hub connecting to experiments, institutes, realms, metrics, physical schemes, and more
- **Experiment**: Links to projects, institutes, variables, domains, and geographic regions
- **Variable**: Climate variables with metadata (units, standard names) produced by experiments

**Geographic Structure:**
- **City, Country, Country_Subdivision**: Rich geographic data with GeoNames integration
- All geographic entities connect to continents and countries

**Research Context:**
- **Paper**: Connects to methods, models, tasks, problems, innovations, and mentions various climate phenomena
- **Method/Model**: Link to tasks, metrics, problems, and results
- **Institute**: Produces sources and performs experiments

**Climate Science Specifics:**
- **RCM** (Regional Climate Models): Driven by other sources
- **Physical schemes, forcing, realms**: Describe model physics
- **Natural hazards, weather events, ocean circulation**: Climate phenomena

The diagram is now available for you to view and explore interactively!

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 for climatemodelskg on 2025-12-24*

claude-sonnet-4-20250514
