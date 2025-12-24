## Chat Transcript
Exploring the Soil Organic Carbon Knowledge Graph (SOCKG)

👤 **User**  
@sockg

---

🧠 **Assistant**  
I'll help you explore the sockg knowledge graph. Let me start by getting information about this knowledge graph and its schema.

Great! I can now help you explore the **Soil Organic Carbon Knowledge Graph (SOCKG)**. This knowledge graph contains detailed agricultural experimental data focused on soil organic carbon, which is crucial for understanding carbon sequestration and climate-friendly farming practices.

## What's in SOCKG?

The knowledge graph includes:

- **Agricultural experiments**: Tillage events, crop rotations, fertilizer applications, soil measurements
- **Environmental data**: Weather observations, greenhouse gas flux measurements
- **Management practices**: Planting, grazing, irrigation, residue management
- **Soil samples**: Chemical, biological, and physical analyses of soil
- **Geographic coverage**: Sites across multiple locations with spatial data
- **Publications**: Research papers, reports, and bibliographic information

## Key Classes (105 total)

The schema includes classes for:
- Experimental units, treatments, and sites
- Soil samples (chemical, biological, physical)
- Agricultural management (tillage, planting, grazing, irrigation)
- Crops, cultivars, and cover crops
- Measurements (biomass, GHG flux, erosion, water quality)
- Weather observations
- Publications and research projects

## What would you like to explore?

I can help you:
- Find specific data about soil organic carbon measurements
- Explore relationships between management practices and outcomes
- Query experimental treatments and their effects
- Analyze spatial patterns across different sites
- Search for publications and research projects
- Examine specific crops, tillage methods, or amendments

What aspect of soil carbon research interests you?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
```mermaid
classDiagram
direction TB

class ExperimentalUnit {
  +unitUrl: string
  +startDate: date
  +endDate: date
  +organicManagement: boolean
  +tileDrainage: boolean
}

class Treatment {
  +hasRotation
  +usesTreatment
}

class Site {
  +hasGeometry
  +sfWithin
  +weatherAt
}

class Location {
  +hasGeometry
}

class Project {
  +fundedBy
  +hasProjectScenario
  +fromProject
}

class SoilSample {
  +upperDepth: float
  +lowerDepth: float
  +hasMeasurement
}

class SoilChemicalSample

class SoilBiologicalSample

class SoilPhysicalSample

class Measurement {
  +quantityValue
  +badValueFlag: boolean
  +inferred: boolean
  +isInterpolated: boolean
}

class WeatherObservation {
  +hasMeasurement
  +of
}

class GHGFlux {
  +hasChamberPlacement
  +hasMeasurement
}

class Tillage {
  +usesTillageMethod
  +usesEquipment
}

class TillageEvent {
  +startDate: date
  +endDate: date
}

class TillageManagement {
  +hasTillageEvent
  +hasTillage
}

class Amendment {
  +hasAmendmentType
  +withPlacement
}

class FertilizerAmendment

class PlantingManagement {
  +usesPlantingMethod
  +hasCrop
  +hasCultivar
  +usesCoverCrop
}

class GrazingManagement {
  +hasAnimalSpecies
  +hasAnimalClass
  +hasGrazingRate
}

class ResidueManagement {
  +usesResidueRemoval
}

class Rotation {
  +hasGrowthStage
}

class Cultivar {
  +hasBroadleafOrGrass
}

class CoverCrop

class JournalArticle {
  +title: string
  +identifier: string
  +date: date
  +creator
  +cites
}

class Person {
  +givenName: string
  +familyName: string
  +email: string
  +affiliation
}

class Organization {
  +label: string
}

class AdministrativeRegion

class AdministrativeRegion_0

class AdministrativeRegion_1

class AdministrativeRegion_2

class S2Cell_Level13

class QuantityValue {
  +numericValue: float
  +hasUnit
  +standardUncertainty: float
}

ExperimentalUnit --> Treatment : usesTreatment
ExperimentalUnit --> Site : sfWithin
ExperimentalUnit --> SoilSample : fromUnit
ExperimentalUnit --> Measurement : hasMeasurement
ExperimentalUnit --> TillageManagement : unitHasTillageManagement
ExperimentalUnit --> PlantingManagement : unitHasPlantingManagement
ExperimentalUnit --> GrazingManagement : unitHasGrazingManagement
ExperimentalUnit --> ResidueManagement : unitHasResidueManagement
ExperimentalUnit --> Amendment : unitHasAmendment

Treatment --> Rotation : hasRotation
Treatment --> TillageManagement : treatmentHasTillageManagement
Treatment --> PlantingManagement : treatmentHasPlantingManagement
Treatment --> GrazingManagement : treatmentHasGrazingManagement
Treatment --> ResidueManagement : treatmentHasResidueManagement
Treatment --> Amendment : treatmentHasAmendment

Site --> Location : hasGeometry
Site --> WeatherObservation : weatherAt
Site --> AdministrativeRegion : sfWithin
Site --> Project : fromProject

SoilSample --|> SoilChemicalSample
SoilSample --|> SoilBiologicalSample
SoilSample --|> SoilPhysicalSample
SoilSample --> Measurement : hasMeasurement

Measurement --> QuantityValue : quantityValue

TillageManagement --> Tillage : hasTillage
TillageManagement --> TillageEvent : hasTillageEvent

Amendment --|> FertilizerAmendment

PlantingManagement --> Cultivar : hasCultivar
PlantingManagement --> CoverCrop : usesCoverCrop

Rotation --> Cultivar : hasCrop

JournalArticle --> Person : creator
JournalArticle --> Person : correspondingAuthor

Person --> Organization : affiliation

AdministrativeRegion --|> AdministrativeRegion_0
AdministrativeRegion --|> AdministrativeRegion_1
AdministrativeRegion --|> AdministrativeRegion_2

Location --> AdministrativeRegion : sfWithin
Location --> S2Cell_Level13 : sfWithin

GHGFlux --> Measurement : hasMeasurement

WeatherObservation --> Measurement : hasMeasurement
```

Here's a visualization of the SOCKG schema showing the main classes and their relationships!

## Key Components:

**Core Experimental Structure:**
- **ExperimentalUnit** - The central entity containing treatments, measurements, and management practices
- **Treatment** - Experimental treatments applied to units
- **Site** - Physical locations where experiments are conducted

**Management Practices:**
- **TillageManagement** - Soil cultivation practices
- **PlantingManagement** - Crop planting details
- **GrazingManagement** - Livestock grazing activities
- **ResidueManagement** - Crop residue handling
- **Amendment** - Fertilizers and other soil amendments

**Data Collection:**
- **SoilSample** - Subdivided into chemical, biological, and physical samples
- **Measurement** - Quantitative observations with units
- **WeatherObservation** - Meteorological data
- **GHGFlux** - Greenhouse gas emissions

**Geographic Context:**
- **Location** - Spatial coordinates
- **AdministrativeRegion** - Countries, states, counties
- **S2Cell** - Geometric grid cells

**Publications:**
- **JournalArticle** - Research papers
- **Person** - Authors and researchers
- **Organization** - Affiliated institutions

The diagram shows how experimental units connect to sites, treatments, and various measurements, creating a comprehensive framework for tracking soil carbon research data!

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 for sockg on 2025-12-24*

claude-sonnet-4-20250514
