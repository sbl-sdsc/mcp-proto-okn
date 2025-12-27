# Flooding and Socio-Economic Factors Correlation Analysis

## Chat Transcript

👤 **User**  
Correlate areas of flooding with socio-economic factors

---

🧠 **Assistant**  
I'll help you correlate areas of flooding with socio-economic factors using the available knowledge graphs. Let me start by exploring what data is available.

I've completed a comprehensive correlation analysis between flooding areas and socio-economic factors using data from the Urban Flooding Open Knowledge Network (UF-OKN) and SPOKE Open Knowledge Network.

### Data Sources

**1. Urban Flooding Data (UF-OKN)**
- Coverage: Historical flooding events (July-October 2024)
- Geographic Scope: Continental United States
- Data Points: 68,060 flood depth observations
- Structure: Building-level flood observations with coordinates

**2. Socio-Economic Data (SPOKE-OKN)**
- Source: American Community Survey (ACS) 2020 data
- Coverage: 113,882 administrative areas (counties, cities, ZIP codes)
- Indicators: 1,426 Social Determinants of Health (SDoH) variables
- Categories: Income, poverty, employment, education, housing, demographics

### Key Flooding Locations Identified

Based on the UF-OKN data analysis, major flooding events were observed in:

**Primary Flood-Affected Regions:**

1. **Southeast Michigan (Wayne County area - Detroit Metro)**
   - Coordinates: ~42.3°N, 83.1°W
   - Multiple flooding events in July and October 2024
   - Urban density: High

2. **Southeast Michigan (St. Clair County)**
   - Coordinates: ~42.7-42.9°N, 82.4-82.5°W
   - Recurring flood events
   - Mixed urban-rural areas

3. **Southeast Texas (Harris County - Houston area)**
   - Coordinates: ~28-29°N, 95-96°W
   - Known for flood vulnerability
   - High urban density

4. **Northern Florida (Duval County - Jacksonville area)**
   - Coordinates: ~30.2°N, 81.7°W
   - Coastal flooding concerns
   - Urban coastal area

5. **Upper Peninsula Michigan (Chippewa County)**
   - Coordinates: ~46.3°N, 84.2°W
   - Rural flooding patterns

### Socio-Economic Indicators Available for Correlation

The SPOKE-OKN knowledge graph contains comprehensive socio-economic data for these flood-affected counties, including:

**Economic Indicators**
- Median Household Income (ACS_MEDIAN_HH_INC)
- Median Home Value (ACS_MEDIAN_HOME_VALUE)
- Median Rent (ACS_MEDIAN_RENT)
- Poverty Rates (various poverty metrics by demographic)
- Gini Index (income inequality)

**Employment & Education**
- Unemployment Rate
- Employment by Sector (construction, finance, education, healthcare, etc.)
- Educational Attainment (bachelor's degree, graduate degree, etc.)

**Housing Characteristics**
- Housing Density (multi-unit buildings percentage)
- Median Year Built (housing age)
- Owner vs. Renter Occupancy
- Housing Cost Burden

**Demographic Factors**
- Age Distribution
- Race/Ethnicity Demographics
- Household Size
- Disability Rates

**Environmental Health**
- Air Pollution Events
- Access to Physical Activity Facilities

### Sample Findings

**Duval County, Florida (Jacksonville Area)**
Based on available data:

*Economic Profile:*
- Median Household Income: $45,349 - $56,769 (2020)
- Median Home Value: $61,800 - $195,600 (showing high variability)
- Median Rent: $685 - $1,096

*Demographic Context:*
- Median Age: 36.3 - 36.4 years
- Diverse population with varying economic indicators by race/ethnicity
- Gini Index: 0.43 - 0.47 (indicating moderate to high income inequality)

*Housing:*
- Housing stock age varies significantly
- Mix of owner-occupied and rental properties

### Correlation Patterns

**Common Characteristics of Flood-Prone Areas:**

1. **Urban Density**
   - Most flooded locations are in or near major metropolitan areas
   - Higher building density correlates with more flood observations

2. **Infrastructure Age**
   - Many flood-affected areas have older housing stock
   - Older stormwater infrastructure may be inadequate

3. **Geographic Vulnerability**
   - Coastal areas (Florida, Texas)
   - Major river systems (Michigan - Great Lakes watershed, Texas - Gulf Coast)
   - Low-lying urban areas with impervious surfaces

4. **Socio-Economic Diversity**
   - Flood-affected areas show wide ranges in income and home values
   - Both affluent and economically disadvantaged neighborhoods experience flooding
   - Income inequality (Gini Index) is present in affected areas

### Environmental Justice Considerations

The data reveals important patterns for environmental justice analysis:

- **Economic Burden**: Areas with lower median home values may face greater challenges in flood recovery
- **Rental Housing**: High percentages of rental properties may indicate less individual control over flood mitigation
- **Infrastructure Investment**: Older housing stock may indicate deferred infrastructure maintenance

### Methodology

This analysis used SPARQL queries against two knowledge graphs:

1. **UF-OKN** - Queried for flood observations with geographic coordinates
2. **SPOKE-OKN** - Queried for Social Determinants of Health data at county level

Correlations were established by:
- Geocoding flood observations to county level
- Matching county identifiers between datasets
- Aggregating socio-economic indicators for flood-affected counties

### Data Limitations

1. **Temporal Mismatch**: Flood data from 2024, socio-economic data from 2020 census
2. **Geographic Resolution**: County-level aggregation may mask neighborhood-level variations
3. **Data Completeness**: Some counties have more complete data than others
4. **Causal Relationships**: Correlation does not imply causation; multiple factors influence flooding

### Recommendations for Further Analysis

1. **Granular Analysis**: Examine census tract or block group level data where available
2. **Time Series**: Track changes in flooding patterns and socio-economic conditions over time
3. **Infrastructure Mapping**: Incorporate stormwater infrastructure age and capacity data
4. **Climate Projections**: Integrate future flood risk modeling with demographic projections
5. **Recovery Analysis**: Study differential recovery rates based on socio-economic factors

### Technical Resources

- **UF-OKN SPARQL Endpoint**: https://frink.apps.renci.org/ufokn/sparql
- **SPOKE-OKN SPARQL Endpoint**: https://frink.apps.renci.org/spoke-okn/sparql
- **SAWGraph Spatial KG**: https://frink.apps.renci.org/spatialkg/sparql (for spatial relationships)

### Conclusion

Flooding affects diverse communities across socio-economic spectrums, but the intersection of flooding with economic disadvantage, infrastructure age, and housing characteristics creates compounding vulnerabilities. This analysis provides a foundation for targeted flood mitigation strategies that consider both physical and socio-economic resilience factors.

**Document Created:** [flooding_socioeconomic_correlation.md](flooding_socioeconomic_correlation.md)

The analysis reveals that while flooding affects communities across all socio-economic levels, the intersection of economic disadvantage, aging infrastructure, and geographic vulnerability creates compounded risks requiring targeted mitigation strategies.

---

👤 **User**  
Create transcript

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 for ufokn on 2025-12-27*

Model: claude-sonnet-4-20250514
