# SOCKG Knowledge Graph Exploration

## Chat Transcript

👤 **User**  
@sockg

---

🧠 **Assistant**  
I'll help you explore this knowledge graph! Let me start by getting information about what this knowledge graph contains.

Perfect! Now I have all the information about the **Soil Organic Carbon Knowledge Graph (SOCKG)**. Let me give you an overview:

## Overview

The Soil Organic Carbon Knowledge Graph (SOCKG) is a comprehensive knowledge graph designed to enhance soil carbon modeling for voluntary carbon markets. It consolidates fragmented agricultural experimental data into a unified semantic framework.

## What's Inside

SOCKG contains detailed agricultural data including:

- **Agricultural Management Practices**: Tillage events, planting methods, crop rotations, fertilizer amendments, grazing management, irrigation, and residue management
- **Soil Measurements**: Chemical, biological, and physical soil samples with depth information
- **Environmental Data**: Weather observations and greenhouse gas flux measurements
- **Crop Information**: Cultivars, growth stages, biomass analysis, yield data
- **Experimental Structure**: Sites, treatments, experimental units, and rotations

## Key Features

The knowledge graph includes **105 classes** and **106 predicates** organized around:

1. **Experimental organization** - Projects, sites, treatments, and experimental units
2. **Management practices** - Detailed tracking of agricultural interventions
3. **Measurements** - Soil samples (chemical/biological/physical), crop measurements, weather, GHG flux
4. **Spatial data** - Geographic locations linked to administrative regions (GADM) and S2 cells
5. **Bibliographic information** - Publications, funding sources, authors

## What Can You Do?

You can query this knowledge graph to:
- Explore soil organic carbon measurements across different management practices
- Analyze the impact of tillage, amendments, and crop rotations on soil carbon
- Investigate relationships between weather patterns and agricultural outcomes
- Find experimental data from specific locations or treatments
- Explore greenhouse gas emissions under different farming practices

Would you like to explore any specific aspect of the data, such as finding sites with certain management practices, analyzing soil carbon trends, or examining specific crops or regions?

---

👤 **User**  
Visualize a detailed schema

---

🧠 **Assistant**  
I'll create a detailed visual schema of the SOCKG knowledge graph using a Mermaid class diagram.

```mermaid
classDiagram
    %% Core Experimental Structure
    class Project {
        +hasProjectScenario
        +fundedBy
    }
    class ProjectScenario
    class Site {
        +hasGeometry
        +sfWithin
        +weatherAt
    }
    class ExperimentalUnit {
        +usesTreatment
        +hasTreatment
        +fromProject
        +hasMeasurement
        +unitHasAmendment
        +unitHasGrazingManagement
        +unitHasPlantingManagement
        +unitHasResidueManagement
        +unitHasTillageManagement
        +unitHasGrowthStageManagement
        +hasRotation
    }
    class Treatment {
        +treatmentHasAmendment
        +treatmentHasGrazingManagement
        +treatmentHasPlantingManagement
        +treatmentHasResidueManagement
        +treatmentHasTillageManagement
        +treatmentHasGrowthStageManagement
    }
    class Rotation {
        +hasCrop
    }

    %% Management Practices
    class Amendment {
        +hasAmendmentType
        +withPlacement
        +hasTiming
    }
    class FertilizerAmendment
    class AmendmentType
    class AmendmentPlacement
    class TillageManagement {
        +hasTillage
        +hasTillageEvent
        +usesTillageMethod
        +usesEquipment
    }
    class Tillage
    class TillageEvent
    class TillageMethod
    class PlantingManagement {
        +hasCrop
        +hasCultivar
        +usesPlantingMethod
        +hasTiming
    }
    class PlantingMethod
    class ResidueManagement {
        +usesResidueRemoval
    }
    class ResidueRemoval
    class GrazingManagement {
        +hasAnimalClass
        +hasAnimalSpecies
        +hasGrazingRate
    }
    class GrowthStageManagement {
        +hasGrowthStage
    }
    class Irrigation

    %% Crop and Plant Information
    class Cultivar {
        +of
        +hasBroadleafOrGrass
    }
    class CoverCrop
    class GrowthStage
    class PlantFraction
    class SpeciesMix
    class BroadleafOrGrass

    %% Measurements
    class Measurement {
        +fromUnit
        +quantityValue
        +badValueFlag
        +inferred
        +isInterpolated
    }
    class SoilSample {
        +upperDepth
        +lowerDepth
    }
    class SoilChemicalSample
    class SoilBiologicalSample
    class SoilPhysicalSample
    class WeatherObservation
    class GHGFlux {
        +hasChamberPlacement
    }
    class CropRelatedMeasurement {
        +hasCrop
        +hasGrowthStage
    }
    class BiomassAnalysis
    class YieldNutrientUptake
    class ResidueMeasurement
    class ErosionMeasurement
    class QualityMeasurement

    %% Geographic and Spatial
    class Location {
        +hasGeometry
        +sfWithin
    }
    class AdministrativeRegion
    class AdministrativeRegion_0
    class AdministrativeRegion_1
    class AdministrativeRegion_2
    class S2Cell_Level13
    class Geometry {
        +asWKT
    }

    %% Bibliographic
    class BibliographicResource {
        +creator
        +title
        +date
        +identifier
        +bibliographicCitation
    }
    class JournalArticle
    class BookChapter
    class Report
    class Thesis
    class Person {
        +givenName
        +familyName
        +email
        +affiliation
        +hasOccupation
    }
    class Organization
    class FundingSource

    %% Measurement Support
    class QuantityValue {
        +numericValue
        +hasUnit
        +standardUncertainty
    }
    class Unit
    class Timing
    class StartStopInterval {
        +startDate
        +endDate
    }

    %% Key Relationships - Experimental Structure
    Project --> ProjectScenario : hasProjectScenario
    Project --> FundingSource : fundedBy
    Site --> Location : weatherAt
    Site --> Geometry : hasGeometry
    ExperimentalUnit --> Treatment : usesTreatment
    ExperimentalUnit --> Project : fromProject
    ExperimentalUnit --> Rotation : hasRotation
    ExperimentalUnit --> Measurement : hasMeasurement
    Treatment --> Amendment : treatmentHasAmendment
    Treatment --> TillageManagement : treatmentHasTillageManagement
    Treatment --> PlantingManagement : treatmentHasPlantingManagement
    Treatment --> ResidueManagement : treatmentHasResidueManagement
    Treatment --> GrazingManagement : treatmentHasGrazingManagement
    Treatment --> GrowthStageManagement : treatmentHasGrowthStageManagement
    
    %% Management Relationships
    Amendment --> AmendmentType : hasAmendmentType
    Amendment --> AmendmentPlacement : withPlacement
    Amendment --> Timing : hasTiming
    FertilizerAmendment --|> Amendment
    TillageManagement --> Tillage : hasTillage
    TillageManagement --> TillageEvent : hasTillageEvent
    TillageManagement --> TillageMethod : usesTillageMethod
    PlantingManagement --> Cultivar : hasCultivar
    PlantingManagement --> PlantingMethod : usesPlantingMethod
    PlantingManagement --> Timing : hasTiming
    GrazingManagement --> AnimalClass : hasAnimalClass
    GrazingManagement --> AnimalSpecies : hasAnimalSpecies
    GrowthStageManagement --> GrowthStage : hasGrowthStage
    Rotation --> Cultivar : hasCrop

    %% Crop Relationships
    Cultivar --> BroadleafOrGrass : hasBroadleafOrGrass
    
    %% Measurement Relationships
    Measurement --> QuantityValue : quantityValue
    Measurement --> ExperimentalUnit : fromUnit
    SoilSample --|> Measurement
    SoilChemicalSample --|> SoilSample
    SoilBiologicalSample --|> SoilSample
    SoilPhysicalSample --|> SoilSample
    WeatherObservation --|> Measurement
    GHGFlux --|> Measurement
    CropRelatedMeasurement --|> Measurement
    BiomassAnalysis --|> CropRelatedMeasurement
    YieldNutrientUptake --|> CropRelatedMeasurement
    ResidueMeasurement --|> Measurement
    ErosionMeasurement --|> Measurement
    
    %% Spatial Relationships
    Location --> Geometry : hasGeometry
    Location --> AdministrativeRegion : sfWithin
    AdministrativeRegion_0 --|> AdministrativeRegion
    AdministrativeRegion_1 --|> AdministrativeRegion
    AdministrativeRegion_2 --|> AdministrativeRegion
    
    %% Bibliographic Relationships
    BibliographicResource --> Person : creator
    JournalArticle --|> BibliographicResource
    BookChapter --|> BibliographicResource
    Report --|> BibliographicResource
    Thesis --|> BibliographicResource
    Person --> Organization : affiliation
    
    %% Measurement Support
    QuantityValue --> Unit : hasUnit
    Timing --> StartStopInterval : withStartStopInterval
```

This detailed schema visualization shows the SOCKG structure organized into major sections:

**🔬 Core Experimental Structure** (top): The foundation showing how Projects contain ExperimentalUnits that receive Treatments and generate Measurements

**🌾 Management Practices** (middle-left): All agricultural interventions including tillage, planting, amendments, grazing, and residue management

**📊 Measurements** (middle-right): Various types of measurements including soil samples (chemical, biological, physical), weather observations, GHG flux, and crop-related data

**🗺️ Geographic & Spatial** (lower-left): Location data with administrative regions at multiple levels and spatial geometries

**📚 Bibliographic** (lower-right): Publications, authors, organizations, and funding sources

**⚙️ Supporting Classes** (bottom): Measurement infrastructure like quantity values, units, and timing information

The arrows show key relationships, with solid lines representing associations and dashed lines (--|>) representing inheritance/subclass relationships.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 using claude-sonnet-4-20250514 on 2025-12-22*
