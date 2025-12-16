# Michigan Flood Event Analysis - Chat Transcript

## October 29, 2024 Flood Event Analysis using UFOKN Knowledge Graph

---

👤 **User**

@ufokn: Find the most recent flood event in Michigan and the impact.

---

🤖 **Claude**

I'll help you find information about recent flood events in Michigan from the UFOKN knowledge graph. Let me start by understanding the schema and then querying for flood events.

After querying the UFOKN knowledge graph, I found a significant flood event that occurred on **October 29, 2024, at 8:00 AM** in Michigan.

## Most Recent Flood Event in Michigan (October 29, 2024)

### Event Details
The UFOKN knowledge graph contains data about a significant flood event that occurred on **October 29, 2024, at 8:00 AM** in Michigan. This appears to be flood predictions/observations that may have been associated with the aftermath of Hurricane Milton, which made landfall in Florida on October 9, 2024.

### Impact Summary

**Scale of Impact:**
- **19,575 buildings** were predicted to experience flooding across Michigan
- The affected area spanned a large geographic region

**Geographic Extent:**
- **Latitude range:** 41.648°N to 46.494°N (covering much of Michigan)
- **Longitude range:** -89.724°W to -82.422°W
- The flooding primarily affected the southeastern Michigan region, particularly around **Detroit and Ann Arbor** (coordinates around 42.26°N, -83.14°W)

**Affected Areas:**
The flooding impacted multiple regions across Michigan, from the southern border extending into the Upper Peninsula, with particular concentration in urban areas of southeastern Michigan.

### Context
While Hurricane Milton directly impacted Florida in early October 2024, the data suggests Michigan experienced significant flood predictions on October 29, potentially from related weather systems or remnant effects. The web search results show that Michigan National Guard members were deployed to Florida to assist with Hurricane Milton recovery efforts, but the knowledge graph data indicates Michigan itself faced flooding conditions later in the month.

The predictions in the knowledge graph indicate this was a widespread flooding event affecting nearly 20,000 buildings across a broad swath of Michigan, making it a significant disaster event for the state.

---

👤 **User**

Add an isosurface to an OpenStreetMap to visualize spatial clusters of buildings experiencing significant flooding in this event. Use a random sampling of 200 locations.

---

🤖 **Claude**

I've created an interactive map visualization showing spatial clusters of flooded buildings in Michigan from the October 29, 2024 event using a random sample of 200 locations from the UFOKN knowledge graph.

## Interactive Map Visualization

[Download Michigan Flood Map](https://sbl-sdsc.github.io/mcp-proto-okn/examples/michigan_flood_map.html)

### Key Features:

1. **Heatmap/Isosurface Layer**: Shows spatial density of flooded buildings using color gradients:
   - Blue/Cyan: Low concentration
   - Green/Yellow: Moderate concentration  
   - Orange/Red: High concentration areas

2. **200 Random Sampled Locations**: Individual building markers from across the affected region

3. **Interactive Elements**:
   - Click markers to see exact coordinates and event details
   - Toggle between heatmap and individual markers using the layer control
   - Zoom and pan to explore different areas
   - Scale bar for distance reference

4. **Information Panel**: Shows event statistics:
   - Date: October 29, 2024
   - Sample size: 200 buildings
   - Total affected: 19,575 buildings

### Spatial Patterns Revealed:

The heatmap clearly shows **two major flooding clusters**:
1. **Southeastern Michigan** (Detroit/Ann Arbor area around 42.2-42.4°N, -83.0 to -83.2°W) - the densest concentration
2. **Port Huron area** (northeastern region around 42.7-43.0°N, -82.4 to -82.5°W)
3. **Upper Peninsula** scattered locations (around 46°N, -84°W)

The isosurface visualization effectively highlights that the most severe flooding was concentrated in the urbanized Detroit metropolitan area, with significant secondary impacts along the St. Clair River corridor.

### Technical Implementation:

The visualization uses:
- **Leaflet.js** for the interactive map framework
- **OpenStreetMap** tiles for the base layer
- **Simpleheat** library for smooth isosurface/heatmap rendering
- **Custom color gradient** (blue→cyan→green→yellow→orange→red) to show flood density
- **Layer controls** for toggling between visualization modes

The heatmap creates a smooth density surface that acts as an isosurface visualization, where areas of similar flood concentration are represented by continuous color bands, making it easy to identify spatial clustering patterns and high-impact zones.

---

## Summary

This analysis demonstrates how the UFOKN knowledge graph can be used to:
1. Query and retrieve detailed flood event data with precise temporal and spatial information
2. Analyze the scale and geographic distribution of disaster impacts
3. Visualize spatial patterns using interactive geospatial techniques
4. Identify high-risk areas and clustering patterns for emergency response planning

The October 29, 2024 Michigan flood event affected nearly 20,000 buildings across the state, with the most severe impacts concentrated in the Detroit metropolitan area.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on December 15, 2025*
