# SAWGraph FRS Knowledge Graph Exploration

👤 **User**  
@fiokg

---

🧠 **Assistant**  
I'll help you explore this knowledge graph! Let me start by getting information about it.

Great! I can see this is the **SAWGraph FRS KG** (Facility Registry Service Knowledge Graph), which is part of the SAWGraph project focused on monitoring PFAS and other contaminants in food and water systems.

Now let me get the schema to understand what data is available:

Perfect! Now I have a comprehensive view of the **SAWGraph FRS Knowledge Graph**. This is a rich environmental dataset containing information about facilities, their industries, environmental programs, and compliance records.

## What's in this Knowledge Graph?

This knowledge graph contains comprehensive data about **826,000+ regulated facilities** across the United States from the EPA's Facility Registry Service. Here are the key components:

### Core Entities

- **Facilities** - Industrial, federal, and utility facilities tracked by EPA programs
- **Organizations** - Companies and agencies that own/operate facilities  
- **Industries** - NAICS classification codes (hierarchical: Sector → Subsector → Industry Group → Industry)
- **Environmental Records** - Permits, monitoring data, enforcement actions, compliance reports
- **Environmental Programs** - Air, water, waste, hazardous materials, underground storage tanks, etc.

### Key Features

- **2.6 million entities** and **10+ million triples**
- Spatial indexing using S2 cells (Level 13) and county subdivisions
- Links to environmental interest types and compliance systems
- Temporal tracking of facility activities
- **PFAS facility identification** - facilities potentially handling PFAS chemicals

### What You Can Explore

Would you like to:
1. **Find facilities** by location, industry, or environmental program
2. **Explore PFAS-related facilities** and their industries
3. **Analyze compliance and enforcement** patterns
4. **Examine industry classifications** and facility types
5. **Investigate specific environmental programs** (air quality, water, waste, etc.)

What interests you most about this data?

---

👤 **User**  
Visualize the schema

---

🧠 **Assistant**  
```mermaid
classDiagram
    class Facility["Facility"]
    Facility : +hasFRSId string
    
    class Organization["Organization"]
    
    class Industry["Industry"]
    
    class NAICSIndustryCode["NAICS Industry Code"]
    
    class NAICSIndustrySector["NAICS Industry Sector (2 digits)"]
    
    class NAICSIndustrySubsector["NAICS Industry Subsector (3 digits)"]
    
    class NAICSIndustryGroup["NAICS Industry Group (4 digits)"]
    
    class NAICSIndustry["NAICS Industry (6 digits)"]
    
    class FRSFacility["FRS Facility"]
    
    class EPAPFASFacility["EPA PFAS Facility"]
    
    class FacilityType["Facility Type"]
    
    class Record["Facility Record"]
    
    class SupplementalRecord["Supplemental Record"]
    
    class MonitoringRecord["Monitoring Record"]
    
    class PermitRecord["Permit Record"]
    
    class EnforcementActivity["Enforcement Activity"]
    
    class ComplianceRecord["Compliance Record"]
    
    class RegistrationRecord["Registration Record"]
    
    class ReportingRecord["Reporting Record"]
    
    class RiskPlanRecord["Risk Plan Record"]
    
    class SiteRecord["Site Record"]
    
    class ProjectRecord["Project Record"]
    
    class EnvironmentalInterestType["Environmental Interest Type"]
    
    class EnvironmentalInterestByProgram["Environmental Interest By Program"]
    
    class EnvironmentalInterestByRecordType["Environmental Interest By Record Type"]
    
    class ComplianceInterest["Compliance Interest"]
    
    class EnforcementInterest["Enforcement Interest"]
    
    class PermitInterest["Permit Interest"]
    
    class RegistryInterest["Registry Interest"]
    
    class ReportingInterest["Reporting Interest"]
    
    class RiskInterest["Risk Interest"]
    
    class SiteInterest["Site Interest"]
    
    class ProgramInformationSystem["Program Information System"]
    
    class ComplianceSystem["Compliance System"]
    
    class EnforcementSystem["Enforcement System"]
    
    class PermitSystem["Permit System"]
    
    class RegistrySystem["Registry System"]
    
    class ReportingSystem["Reporting System"]
    
    class GrantSystem["Grant System"]
    
    class ProjectSystem["Project System"]
    
    class SiteSystem["Site System"]
    
    class StationSystem["Station System"]
    
    class StateSystem["State System"]
    
    class TribalSystem["Tribal System"]
    
    class LegacySystem["Legacy System"]
    
    class AirProgram["AIR PROGRAMS"]
    
    class WaterProgram["WASTE WATER PROGRAMS"]
    
    class DrinkingWaterProgram["DRINKING WATER PROGRAMS"]
    
    class HazardousWasteProgram["HAZARDOUS WASTE PROGRAMS"]
    
    class SolidWasteProgram["SOLID WASTE PROGRAMS"]
    
    class ChemicalReleaseProgram["CHEMICAL RELEASE PROGRAMS"]
    
    class Agency["Agency"]
    
    Facility <|-- FRSFacility : is a
    FRSFacility <|-- EPAPFASFacility : is a
    
    NAICSIndustryCode <|-- NAICSIndustrySector : is a
    NAICSIndustryCode <|-- NAICSIndustrySubsector : is a
    NAICSIndustryCode <|-- NAICSIndustryGroup : is a
    NAICSIndustryCode <|-- NAICSIndustry : is a
    
    NAICSIndustrySector <-- NAICSIndustrySubsector : subcodeOf
    NAICSIndustrySubsector <-- NAICSIndustryGroup : subcodeOf
    NAICSIndustryGroup <-- NAICSIndustry : subcodeOf
    
    Record <|-- SupplementalRecord : is a
    Record <|-- MonitoringRecord : is a
    SupplementalRecord <|-- PermitRecord : is a
    SupplementalRecord <|-- EnforcementActivity : is a
    SupplementalRecord <|-- ComplianceRecord : is a
    SupplementalRecord <|-- RegistrationRecord : is a
    SupplementalRecord <|-- ReportingRecord : is a
    SupplementalRecord <|-- RiskPlanRecord : is a
    SupplementalRecord <|-- SiteRecord : is a
    SupplementalRecord <|-- ProjectRecord : is a
    
    EnvironmentalInterestType <|-- EnvironmentalInterestByProgram : is a
    EnvironmentalInterestType <|-- EnvironmentalInterestByRecordType : is a
    
    EnvironmentalInterestByRecordType <|-- ComplianceInterest : is a
    EnvironmentalInterestByRecordType <|-- EnforcementInterest : is a
    EnvironmentalInterestByRecordType <|-- PermitInterest : is a
    EnvironmentalInterestByRecordType <|-- RegistryInterest : is a
    EnvironmentalInterestByRecordType <|-- ReportingInterest : is a
    EnvironmentalInterestByRecordType <|-- RiskInterest : is a
    EnvironmentalInterestByRecordType <|-- SiteInterest : is a
    
    EnvironmentalInterestByProgram <|-- AirProgram : is a
    EnvironmentalInterestByProgram <|-- WaterProgram : is a
    EnvironmentalInterestByProgram <|-- DrinkingWaterProgram : is a
    EnvironmentalInterestByProgram <|-- HazardousWasteProgram : is a
    EnvironmentalInterestByProgram <|-- SolidWasteProgram : is a
    EnvironmentalInterestByProgram <|-- ChemicalReleaseProgram : is a
    
    ProgramInformationSystem <|-- ComplianceSystem : is a
    ProgramInformationSystem <|-- EnforcementSystem : is a
    ProgramInformationSystem <|-- PermitSystem : is a
    ProgramInformationSystem <|-- RegistrySystem : is a
    ProgramInformationSystem <|-- ReportingSystem : is a
    ProgramInformationSystem <|-- GrantSystem : is a
    ProgramInformationSystem <|-- ProjectSystem : is a
    ProgramInformationSystem <|-- SiteSystem : is a
    ProgramInformationSystem <|-- StationSystem : is a
    ProgramInformationSystem <|-- StateSystem : is a
    ProgramInformationSystem <|-- TribalSystem : is a
    ProgramInformationSystem <|-- LegacySystem : is a
    
    Facility --> Organization : ownedBy
    Organization --> Facility : hasFacility
    Facility --> FacilityType : ofFacilityType
    Facility --> NAICSIndustryCode : ofPrimaryIndustry
    Facility --> NAICSIndustryCode : ofSecondaryIndustry
    Facility --> EnvironmentalInterestType : hasEnvironmentalInterest
    Facility --> Record : hasRecord
    Facility --> SupplementalRecord : hasSupplementalRecord
    Facility --> MonitoringRecord : hasMonitoringRecord
    
    Record --> ProgramInformationSystem : fromSystem
    EnvironmentalInterestType --> EnvironmentalInterestType : ofInterestType
    
    NAICSIndustryCode --> NAICSIndustryCode : sameCode
    NAICSIndustryCode --> NAICSIndustryCode : subcodeOf
```

This visualization shows the structure of the SAWGraph FRS Knowledge Graph with four main hierarchies:

1. **Facilities & Organizations** (left) - Shows how facilities relate to organizations and their classifications
2. **NAICS Industry Codes** (top-left) - Hierarchical industry classification from 2-digit sectors down to 6-digit industries
3. **Environmental Records** (center) - Different types of records associated with facilities
4. **Environmental Programs** (right side) - Program types and information systems that track facilities

The diagram illustrates how facilities connect to their industries, environmental programs, and various tracking records through the EPA's regulatory systems.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 using claude-sonnet-4-20250514 on 2025-12-22*
