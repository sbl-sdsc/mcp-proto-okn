# Chat Transcript: US Counties with High Disease Prevalence

**Date:** December 11, 2025  
**Topic:** Analysis of disease prevalence data in US counties using SPOKE-OKN knowledge graph

---

## User Query
> Which US counties have high disease prevalence?

---

## Analysis Process

### Initial Investigation
I began by exploring the SPOKE-OKN (SPOKE Open Knowledge Network) knowledge graph, which is a comprehensive biomedical and environmental health knowledge graph that integrates diverse data across genomics, environmental science, and public health.

### Data Structure Discovery
The knowledge graph contains:
- **9 chronic diseases tracked**: obesity, hypertension, diabetes mellitus, coronary artery disease, chronic obstructive pulmonary disease (COPD), arteriosclerosis, asthma, cerebrovascular disease, and depressive disorder
- **Coverage**: 26,343 data points per disease across US locations
- **Geographic levels**: Cities/towns that are part of counties, allowing county-level aggregation

### Query Methodology
I queried disease prevalence data by:
1. Identifying reified relationships between diseases and locations with prevalence values
2. Aggregating city-level data to county level
3. Calculating average prevalence rates per county per disease
4. Filtering for counties with high disease burden (>28% average prevalence across diseases with >20% individual values)

---

## Key Findings

### Top 10 Counties by Overall Disease Burden

| Rank | County | State | Avg Prevalence | # Cities |
|------|--------|-------|----------------|----------|
| 1 | Sunflower County | Mississippi | 39.3% | 7 |
| 2 | Leflore County | Mississippi | 39.0% | 6 |
| 3 | Wilcox County | Alabama | 38.2% | 5 |
| 4 | Bolivar County | Mississippi | 38.2% | 14 |
| 5 | Lowndes County | Alabama | 38.2% | 6 |
| 6 | Coahoma County | Mississippi | 38.1% | 7 |
| 7 | Humphreys County | Mississippi | 38.0% | 4 |
| 8 | Sumter County | Alabama | 37.9% | 9 |
| 9 | Holmes County | Mississippi | 37.9% | 7 |
| 10 | Greene County | Alabama | 37.8% | 4 |

### Counties with Highest Obesity Prevalence (>50%)

| County | State | Obesity Rate |
|--------|-------|--------------|
| Greene County | Alabama | 53.2% |
| Perry County | Alabama | 52.8% |
| Sunflower County | Mississippi | 51.7% |
| Jefferson County | Mississippi | 51.6% |
| Holmes County | Mississippi | 51.5% |
| Coahoma County | Mississippi | 51.2% |
| Tensas Parish | Louisiana | 50.8% |
| Claiborne County | Mississippi | 50.6% |
| East Carroll Parish | Louisiana | 50.5% |
| Issaquena County | Mississippi | 50.1% |
| Quitman County | Mississippi | 50.1% |
| Chicot County | Arkansas | 50.0% |

### Counties with Highest Hypertension Prevalence (>50%)

| County | State | Hypertension Rate |
|--------|-------|-------------------|
| Jefferson County | Mississippi | 54.2% |
| Holmes County | Mississippi | 53.9% |
| Issaquena County | Mississippi | 53.8% |
| Quitman County | Mississippi | 53.0% |
| Bolivar County | Mississippi | 52.5% |
| Claiborne County | Mississippi | 52.0% |
| Greene County | Alabama | 51.9% |
| Coahoma County | Mississippi | 51.2% |
| Leflore County | Mississippi | 51.1% |
| Tallahatchie County | Mississippi | 50.9% |

---

## Geographic Patterns

### Mississippi Delta Region
The Mississippi Delta shows the highest concentration of severe disease burden:
- **Sunflower, Leflore, Bolivar, Coahoma, Holmes, Humphreys, Tallahatchie, Quitman, and Issaquena counties** all show average prevalence rates above 35%
- This region has historically faced socioeconomic challenges, limited healthcare access, and high poverty rates

### Alabama Black Belt
Multiple Alabama counties in the historic Black Belt region show elevated disease prevalence:
- **Greene, Wilcox, Lowndes, Perry, Sumter, Monroe, and Bullock counties**
- Named for its rich, dark soil, this region has significant health disparities

### Louisiana Parishes
Several Louisiana parishes show high disease burden:
- **Tensas, East Carroll, Webster, Tangipahoa, Claiborne, Concordia, and Assumption parishes**
- Concentrated in northern and central Louisiana

### Other Affected Regions
- **Texas border counties**: Hidalgo, Cameron, Webb, Brooks, Zapata, Willacy, Starr (prevalence 32-35%)
- **Appalachian region**: Multiple West Virginia counties
- **Native American reservations**: Wade Hampton Census Area (Alaska), Shannon County (SD), Buffalo County (SD), Glacier County (MT)
- **California agricultural regions**: Fresno, Tulare, Imperial counties

---

## Health Equity Implications

### Disparities Identified
1. **Rural vs. Urban**: The highest disease burden counties are predominantly rural
2. **Socioeconomic factors**: Many high-prevalence counties have high poverty rates and limited healthcare infrastructure
3. **Regional clustering**: Disease burden is not random but clusters in specific regions with shared historical and social determinants
4. **Multiple disease burden**: Counties with high rates of one chronic disease typically have high rates of others, suggesting common underlying risk factors

### Contributing Factors (Contextual)
While the knowledge graph provides prevalence data, common contributing factors in these regions often include:
- Limited access to healthcare facilities
- Food deserts and limited access to healthy food options
- Lower rates of physical activity opportunities
- Higher poverty and unemployment rates
- Educational disparities
- Environmental factors

---

## Data Source

**SPOKE-OKN Knowledge Graph**
- Endpoint: https://frink.apps.renci.org/spoke-okn/sparql
- Comprehensive biomedical and environmental health knowledge graph
- Integrates genomics, environmental science, and public health data
- Funded by NSF Award #2333819
- Principal Investigator: Sergio Baranzini, UCSF

---

## Technical Notes

### Query Approach
The analysis used SPARQL queries against the SPOKE-OKN endpoint to:
1. Access reified RDF statements connecting diseases to locations with prevalence values
2. Join city-level data with county boundaries using `PARTOF_LpL` relationships
3. Aggregate and calculate average prevalence rates
4. Filter for statistically significant disease burden

### Data Quality
- All 9 diseases have consistent coverage (26,343 data points each)
- Data includes cities/towns with their county affiliations
- Prevalence values are stored as percentages
- Geographic coverage appears comprehensive across the United States

---

## Summary

The analysis reveals significant geographic health disparities in the United States, with the Mississippi Delta, Alabama Black Belt, and Louisiana parishes bearing the highest burden of chronic disease. Rural counties in the Deep South consistently show prevalence rates exceeding 35% across multiple conditions, with some individual diseases affecting more than half the population in certain areas. This data underscores the critical need for targeted public health interventions and healthcare resources in these underserved regions.
