# Chat Transcript: PFOA Contamination in Drinking Water Analysis

## Analyzing PFOA Concentrations Using SPOKE-OKN Knowledge Graph

👤 **User**  
@spoke-okn: get the top 3 locations where PFOA has the highest concentration in drinking water

---

🧠 **Assistant**  

Based on the SPOKE-OKN knowledge graph data, I found the **top 3 locations with the highest PFOA concentrations in drinking water**:

### Top 3 Locations:

1. **ZIP Code 19426, Pennsylvania**
   - Concentration: 0.235 µg/L (with detection limit of 0.004 µg/L)
   - This is the highest concentration found

2. **ZIP Code 26106, West Virginia**
   - Concentration: 0.0465 µg/L (with detection limit of 0.004 µg/L)
   - Multiple ZIP codes in West Virginia showed this same concentration level

3. **ZIP Code 85541, Arizona**
   - Concentration: 0.0409 µg/L (with detection limit of 0.004 µg/L)

### Key Details:
- **Data source**: UCMR5 (Fifth Unregulated Contaminant Monitoring Rule)
- **Measurement type**: Maximum Concentration (with Minimum Reporting Level)
- **Units**: µg/L (micrograms per liter)

### Analysis:
The Pennsylvania location (ZIP 19426) shows a notably higher PFOA concentration - about 5 times higher than the second-highest locations in West Virginia. PFOA is a perfluorooctanoic acid, one of the persistent "forever chemicals" (PFAS) that have raised significant public health concerns.

### Technical Query Details:
The analysis involved querying the SPOKE-OKN knowledge graph, which integrates:
- Biomedical and environmental health data
- Geographic information (from countries to ZIP codes)
- Chemical compounds and their environmental presence
- Social determinants of health

The query specifically searched for:
- PFOA compound (Perfluorooctanoic acid - PubChem InChIKey: SNGREZUHAYWORS-UHFFFAOYSA-N)
- Relationships indicating chemical presence in locations (FOUNDIN_CfL)
- Media type filtered to "Drinking Water"
- Sorted by concentration values to identify the highest levels

### Data Insights:
- Total PFOA drinking water measurements: 1,721 locations
- Data represents the Fifth Unregulated Contaminant Monitoring Rule (UCMR5) testing
- Measurements include both the detected concentration and the minimum reporting level (in parentheses)
- The pattern shows concentrated areas of concern in PA, WV, and AZ

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on 2025-12-17*
