# Criminal Justice Data Analysis - SCALES Knowledge Graph

## Executive Summary

This analysis examines patterns in criminal justice data from the SCALES (Systematic Content Analysis of Litigation Events) knowledge graph, which contains over 523 million triples covering **2.37 million criminal cases** from federal, state, and local court systems.

---

## 1. Overview Statistics

### Dataset Scope
- **Total Criminal Cases**: 2,368,748
- **Total Bookings**: 363,466 (Fulton County Jail)
- **Court System**: Superior Court of Fulton County (91,601 cases)
- **People in System**: 137,002 individuals with demographic data

---

## 2. Charge Severity Analysis

### Distribution by Severity Level

| Severity Level | Number of Charges | Percentage |
|---------------|-------------------|------------|
| **Felony** | 170,037 | 46.9% |
| **Misdemeanor** | 159,236 | 43.9% |
| None | 32,926 | 9.1% |
| Conversion | 662 | 0.2% |
| Local Ordinance | 514 | 0.1% |

**Key Finding**: The data shows a nearly even split between felony (47%) and misdemeanor (44%) charges, suggesting the system processes a balanced mix of serious and less serious offenses.

---

## 3. Most Common Charges

### Top 30 Charges (All Types)

| Rank | Charge | Count |
|------|--------|-------|
| 1 | Speeding 16-20 over | 136,681 |
| 2 | Tag - none/expired/invalid | 113,503 |
| 3 | Speeding 21-25 over | 99,382 |
| 4 | Following too close | 78,877 |
| 5 | License - driving suspended/revoked | 65,431 |
| 6 | **Driving under influence** | 65,255 |
| 7 | Speeding 11-15 over | 64,367 |
| 8 | Improper lane change | 61,781 |
| 9 | **Criminal trespass** | 59,843 |
| 10 | Violation of seatbelt law | 51,154 |
| 11 | Stop or yield sign violation | 51,011 |
| 12 | Red light violation | 50,706 |
| 13 | Speeding 26-30 over | 50,415 |
| 14 | **Possession of marijuana one ounce or less** | 44,903 |
| 15 | Insurance - no proof | 41,523 |
| 16 | License - none or class violation | 41,224 |
| 17 | Obstructing an officer | 40,338 |
| 18 | Violation of GA Controlled Substance Act | 38,515 |
| 19 | **Simple Battery** | 37,156 |
| 20 | Battery - family violence | 32,009 |

### Analysis by Charge Type

**Traffic Offenses** (dominant category):
- Combined speeding violations: ~351,000 charges
- License/registration issues: ~147,000 charges
- Traffic offenses represent the majority of all charges

**Substance-Related**:
- Marijuana possession (≤1 oz): 44,903 charges
- Controlled substance violations: 38,515 charges

**Violent/Person Crimes**:
- Simple Battery: 37,156 charges
- Battery-family violence: 32,009 charges
- Aggravated assault: 28,049 charges

**Property Crimes**:
- Criminal trespass: 59,843 charges
- Theft by shoplifting: 30,314 charges
- Theft by taking: 30,207 charges
- Deposit account fraud: 31,186 charges

---

## 4. Demographic Patterns

### Gender Distribution

| Gender | Count | Percentage |
|--------|-------|------------|
| **Male (M)** | 111,818 | 81.6% |
| **Female (F)** | 25,163 | 18.4% |
| Unknown (U) | 20 | <0.1% |

**Total individuals**: 137,002

### Racial Distribution

| Race Code | Count | Percentage | Likely Meaning |
|-----------|-------|------------|----------------|
| **B** | 121,985 | 89.0% | Black/African American |
| **W** | 12,238 | 8.9% | White |
| **H** | 1,161 | 0.8% | Hispanic/Latino |
| **U** | 836 | 0.6% | Unknown |
| **A** | 373 | 0.3% | Asian |
| Other | ~400 | 0.3% | Various |

**Critical Finding**: The demographic data shows significant racial disparities, with Black/African American individuals representing 89% of people in this dataset. This likely reflects data primarily from Fulton County, Georgia (Atlanta area), but may also indicate systemic disparities in criminal justice contact.

---

## 5. Gender and Severity Analysis

### Charges by Gender and Severity

| Severity | Male | Female | M:F Ratio |
|----------|------|--------|-----------|
| **Felony** | 147,811 | 22,217 | 6.7:1 |
| **Misdemeanor** | 128,939 | 30,288 | 4.3:1 |
| **None** | 27,676 | 5,247 | 5.3:1 |

**Analysis**:
- Males are charged with felonies at a 6.7:1 ratio compared to females
- The gender disparity is somewhat less pronounced for misdemeanors (4.3:1)
- Overall, males constitute 82% of people in the system across all charge types

---

## 6. Race and Severity Analysis

### Felony Charges by Race

| Race | Felony Count | % of Felonies |
|------|-------------|---------------|
| **B** | 149,745 | 88.3% |
| **W** | 18,858 | 11.1% |
| **A** | 445 | 0.3% |
| **H** | 314 | 0.2% |
| **O** | 179 | 0.1% |

### Misdemeanor Charges by Race

| Race | Misdemeanor Count | % of Misdemeanors |
|------|------------------|-------------------|
| **B** | 133,162 | 83.7% |
| **W** | 24,117 | 15.2% |
| **A** | 654 | 0.4% |
| **H** | 400 | 0.3% |
| **O** | 227 | 0.1% |

**Key Observation**: The racial distribution is consistent across felony and misdemeanor charges, with Black individuals comprising 83-88% of charges regardless of severity level.

---

## 7. Sentencing Patterns

### Sentence Types

| Sentence Description | Count | Percentage |
|---------------------|-------|------------|
| **Probation (prob)** | 170,831 | 48.4% |
| **Serve (incarceration)** | 90,154 | 25.5% |
| **None** | 48,636 | 13.8% |
| **First Offender Probation (fop)** | 42,356 | 12.0% |
| Work Release | 2,668 | 0.8% |
| **Life** | 387 | 0.1% |
| **Life without parole** | 156 | <0.1% |

**Total sentences analyzed**: 353,094

### Key Sentencing Insights:

1. **Probation dominates**: Nearly half (48%) of all sentences are standard probation
2. **Incarceration**: Only 25.5% result in serving time
3. **First Offender Programs**: 12% receive first offender probation, suggesting rehabilitation focus
4. **Life sentences**: 543 total life sentences (387 with parole possibility, 156 without)

---

## 8. Key Findings and Implications

### 1. **Traffic Offenses Dominate the System**
- More than 50% of all charges are traffic-related
- This suggests significant system resources devoted to minor infractions
- May indicate over-policing of traffic violations

### 2. **Significant Demographic Disparities**
- Black individuals represent 89% of people in the system
- Men are 6.7x more likely to face felony charges than women
- These disparities warrant deeper investigation into systemic factors

### 3. **Drug Enforcement Patterns**
- 44,903 charges for marijuana possession (≤1 oz)
- 38,515 controlled substance violations
- Combined drug charges represent ~83,000 cases

### 4. **Probation-Heavy Sentencing**
- 60% of sentences involve probation (standard or first offender)
- Only 25% result in incarceration
- Suggests system preference for community supervision

### 5. **Geographic Concentration**
- Data heavily weighted toward Fulton County, Georgia (Atlanta)
- 363,466 bookings at Fulton County Jail
- May not represent national patterns

### 6. **Family Violence Prevalence**
- 32,009 battery-family violence charges
- 37,156 simple battery charges
- Domestic violence represents significant system burden

---

## 9. Data Quality and Limitations

### Strengths:
- Large sample size (2.37M cases)
- Standardized NIEM format
- Links across arrests, charges, bookings, and sentences

### Limitations:
- Geographic concentration (primarily Fulton County, GA)
- Demographic data may reflect local population + policing patterns
- Some queries exceeded endpoint capacity (very large dataset)
- Missing disposition data for many charges
- Limited temporal analysis (booking dates not fully accessible)

---

## 10. Recommendations for Further Analysis

1. **Temporal Analysis**: Examine trends over time to identify changes in enforcement patterns
2. **Outcome Analysis**: Link charges to dispositions and case outcomes
3. **Geographic Comparison**: Compare Fulton County patterns to other jurisdictions
4. **Racial Disparity Studies**: Control for local demographics to measure disproportionality
5. **Recidivism Analysis**: Track individuals across multiple cases
6. **Attorney Effectiveness**: Analyze public defender vs. private attorney outcomes
7. **Bail and Pretrial**: Examine pretrial detention patterns
8. **Drug Policy Impact**: Analyze marijuana charges before/after policy changes

---

## Data Source

**SCALES Knowledge Graph**
- Endpoint: https://frink.apps.renci.org/scales/sparql
- PI: Danny O'Neal (danny.e.oneal@gmail.com)
- Funding: NSF Award #2333803
- Documentation: https://scales-okn.org/

**Analysis Date**: December 14, 2024
**Analyst**: Claude (Anthropic)

---

*Note: This analysis represents patterns in the available data, which is primarily from Fulton County, Georgia. Findings should not be generalized to the entire U.S. criminal justice system without additional comparative analysis.*
