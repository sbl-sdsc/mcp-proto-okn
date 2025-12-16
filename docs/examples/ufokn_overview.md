# UF-OKN Knowledge Graph Exploration

## Chat Transcript

👤 **User**  
@ufokn

---

🧠 **Assistant**  
I'll help you explore the UFOKN knowledge graph. Let me first get some information about it.

The **Urban Flooding Open Knowledge Network (UF-OKN)** is a geospatial knowledge graph infrastructure that integrates urban built environment data with real-time and historical hydrologic forecasts to enable flood risk assessment and emergency response. 

**Key Information:**
- **Homepage:** https://ufokn.com
- **Contact:** Lilit Yeghiazarian (yeghialt@ucmail.uc.edu)
- **Funding:** NSF Award #2333726
- **SPARQL Endpoint:** https://frink.apps.renci.org/ufokn/sparql

**What UF-OKN Contains:**
- Structured representations of urban infrastructure (buildings, roads, stormwater networks, power stations) derived from OpenStreetMap
- Hydrologic features (rivers, streams) linked to operational forecast models including NOAA's National Water Model and local models like HEC-RAS and SWMM
- "Risk-Points™" - locations where built and natural environments interact with potential flood impacts
- 24-year historical analysis coverage across the continental United States

**Schema Overview:**

The knowledge graph contains 6 main classes:
- **Place** - Urban infrastructure locations (buildings, roads, etc.)
- **GeoCoordinates** & **GeoShape** - Geographic positioning data
- **Observation** - Hydrologic measurements and forecasts
- **PropertyValue** - Property attributes
- **S2Cell** - Spatial indexing cells

And 17 key properties including:
- Geographic data (latitude, longitude, elevation, WKT geometries)
- Identifiers, names, descriptions
- Observation data (dates, measured properties, values, units)
- Additional type classifications

This knowledge graph is particularly useful for queries about:
- Urban infrastructure locations and their flood risk
- Hydrologic observations and forecasts
- Spatial relationships between built environment and water features
- Historical flood data analysis

---

👤 **User**  
Visualize the schema as a diagram

---

🧠 **Assistant**  
Here's the UF-OKN schema visualization:

```mermaid
classDiagram
    class Place {
        schema:name
        schema:description
        schema:identifier
        schema:additionalType
        schema:elevation
    }
    
    class GeoCoordinates {
        schema:latitude
        schema:longitude
        schema:elevation
    }
    
    class GeoShape {
        geosparql:asWKT
    }
    
    class Observation {
        schema:observationDate
    }
    
    class PropertyValue {
        schema:propertyID
        schema:value
        schema:unitCode
        schema:unitText
    }
    
    class S2Cell {
    }
    
    Place --> GeoCoordinates : schema:geo
    Place --> GeoShape : schema:geo
    Observation --> Place : schema:observationAbout
    Observation --> PropertyValue : schema:measuredProperty
    Observation --> PropertyValue : schema:variableMeasured
```

**Key Components:**

- **Place** is the central class representing urban infrastructure (buildings, roads, stormwater networks, etc.) with names, descriptions, and identifiers
- **GeoCoordinates** and **GeoShape** provide precise geographic positioning (lat/long and WKT geometries)
- **Observation** captures hydrologic measurements and forecasts, linked to specific places
- **PropertyValue** stores measured values with units (like water levels, flow rates)
- **S2Cell** provides spatial indexing for efficient geographic queries

The relationships show how observations about flood conditions are linked to specific geographic places and their measured properties.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on 2025-12-15*
