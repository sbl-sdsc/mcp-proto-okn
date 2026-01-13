# North Dakota Mining Industry Suppliers - Knowledge Graph Query

👤 **User**  
@sudokn: Show me the businesses supplying the mining industry in North Dakota. Include the address, latitude, and longitude.

---

🧠 **Assistant**  
I'll query the sudokn knowledge graph to find businesses supplying the mining industry in North Dakota with their location information.

First, I retrieved the knowledge graph description and schema to understand the data structure. The SUDOKN (Supply and Demand Open Knowledge Network) is an interconnected network of publicly available manufacturing capability data focused on Small and Medium-Sized Manufacturers across the United States.

After exploring the schema, I found that the knowledge graph contains:
- Manufacturers with their locations
- Industry relationships (including a "Mining-industry-individual" with 1,741 manufacturers supplying to it)
- Geographic data including addresses, cities, states, and coordinates

I then queried for all businesses in North Dakota that supply to the mining industry and found **27 business locations** (21 unique businesses, some with multiple locations).

## Results: Businesses Supplying the Mining Industry in North Dakota

| Business Name | Address | City | State | ZIP Code | Latitude | Longitude |
|--------------|---------|------|-------|----------|----------|-----------|
| ARNOLD MACHINERY CO. | | Jamestown | North Dakota | 58401 | 46.9 | -98.7 |
| Ben's Structural Fabrication, Inc. | | Fargo | North Dakota | 58105 | 46.8954 | -96.8078 |
| Central Machining & Pump Repair, Inc. | | Minot | North Dakota | 58701 | 48.1 | -101.3 |
| Champ Industries USA Inc. | | Jamestown | North Dakota | 58401 | 46.9 | -98.7 |
| CNC STEEL LLC | | Fargo | North Dakota | 58102 | 46.93 | -96.83 |
| CNC STEEL LLC | | Casselton | North Dakota | 58012 | 47.0 | -97.2 |
| Custom Engineered Machine LLC | | Dickinson | North Dakota | 58602 | 46.8792 | -102.79 |
| Custom Engineered Machine LLC | | Williston | North Dakota | 58801 | 48.3 | -103.7 |
| Delta Constructors | | Grassy Butte | North Dakota | 58634 | 47.4431 | -103.294 |
| Delta Constructors | | Stanley | North Dakota | 58784 | 48.4 | -102.4 |
| Delta Constructors | | Tioga | North Dakota | 58784 | 48.4 | -102.4 |
| Delta Constructors | | Watford City | North Dakota | 58854 | 47.8 | -103.1 |
| FISHER SAND & GRAVEL CO. | | Dickinson | North Dakota | 58601 | 46.9 | -102.8 |
| Jetheat Inc. | | Williston | North Dakota | 58801 | 48.3 | -103.7 |
| Leonardite Products | | Williston | North Dakota | 58801 | 48.3 | -103.7 |
| Leonardite Products | | Williston | North Dakota | 58802-0548 | 48.1465 | -103.622 |
| MALLOY ELECTRIC MOTOR & MACHINING | | Fargo | North Dakota | 58105 | 46.8954 | -96.8078 |
| MALLOY ELECTRIC MOTOR & MACHINING | | Mandan | North Dakota | 58554 | 46.7 | -100.9 |
| Midway Machining, Inc. | | Mandan | North Dakota | 58554 | 46.7 | -100.9 |
| MIDWEST HOSE & SPECIALTY INC. | | Williston | North Dakota | 58802 | 48.1688 | -103.615 |
| NXL Technologies | | Williston | North Dakota | 58801 | 48.3 | -103.7 |
| Patterson-UTI | | Williston | North Dakota | 58801 | 48.3 | -103.7 |
| Rig Mats Of America, Inc. | | Williston | North Dakota | 58801 | 48.2257 | -103.649 |
| RMS Tritec LLC | | Bismarck | North Dakota | 58501 | 43.76 | -93.34 |
| Sabin Metal Corporation | | Williston | North Dakota | 58802-1347 | 48.1465 | -103.622 |
| Sheet Metal Specialties, Inc. | | Bismarck | North Dakota | 58504-6922 | 46.8 | -100.8 |
| Wanzek, Inc. | | Fargo | North Dakota | 58104 | 46.79 | -96.84 |

The businesses are concentrated in key areas like Williston (western ND oil/mining region), Fargo, Dickinson, and Bismarck. Note that street addresses are not available in the dataset for most locations, but city, state, ZIP code, latitude, and longitude coordinates are provided.

---

👤 **User**  
Visualize the location of these businesses on a map

---

🧠 **Assistant**  
I've created an interactive map showing all 27 locations of businesses supplying the mining industry in North Dakota. The map includes:

- **Red markers** for each business location
- **Interactive popups** - click any marker to see the business name, city, ZIP code, and exact coordinates
- **Zoom controls** to explore different regions
- **Scale indicator** for distance reference

Key observations from the map:
- **Western concentration**: Many suppliers are clustered around Williston and the western oil/mining region
- **Urban centers**: Fargo, Bismarck, and Minot also have significant supplier presence
- **Geographic spread**: Businesses are distributed across the state to serve various mining operations

The map is fully interactive - you can zoom in/out and click on any marker for detailed information about each business location.

**[Interactive Map]**

[Mining Suppliers in North Dakota](https://sbl-sdsc.github.io/mcp-proto-okn/examples/mining_suppliers_map.html)


---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.5.0 on 2026-01-13*

Model: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
