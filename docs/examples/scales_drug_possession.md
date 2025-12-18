## Chat Transcript
# Analysis of Co-occurring Charges in Drug Possession Cases

👤 **User**  
@scales: Analyze cases containing a drug possession charge. Identify all other charges that appear in the same cases. Output a table with columns for:

* co-occurring charge type
* number of cases
* percentage of drug possession cases
Sort the table by number of cases in descending order.

---

🧠 **Assistant**  
I'll help you analyze drug possession charges and their co-occurring charges in the SCALES knowledge graph. Let me start by getting information about this dataset.

*[Retrieved SCALES knowledge graph description]*

SCALES is an integrated justice platform to connect criminal justice data across data silos. The knowledge graph contains over 523 million triples describing 96.5 million entities spanning more than 4.1 million cases, including 2.4 million criminal cases and 1.8 million civil cases.

*[Retrieved schema information and executed SPARQL queries]*

## Analysis Summary

I've analyzed **6,854 criminal cases** containing drug possession charges in the SCALES knowledge graph and identified all co-occurring charges. Here are the key findings:

**Top 5 Co-occurring Charges:**

1. **21:841(a)** (Federal drug trafficking statute) - 734 cases (10.71%)
2. **Possession of Marijuana with Intent to Distribute** - 608 cases (8.87%)
3. **Possession of Cocaine** - 356 cases (5.19%)
4. **Possession of Firearm by Convicted Felon** - 298 cases (4.35%)
5. **Possession of Marijuana-Less Than 1 Oz.** - 268 cases (3.91%)

**Notable Patterns:**

- **Drug-related charges** are the most common co-occurring charges, including other possession offenses and intent to distribute charges
- **Firearm charges** appear frequently (multiple variations in the top 20), suggesting a strong connection between drug possession and weapons offenses
- **Obstruction charges** are common, indicating confrontations with law enforcement during drug-related arrests
- **Minor traffic and administrative violations** (driving without license, no insurance, pedestrian violations) co-occur in many cases
- **Property crimes** like theft by receiving stolen property appear in about 2% of drug possession cases

The complete table with all 50 most common co-occurring charges is available in the detailed report: [drug_possession_cooccurring_charges.md](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/drug_possession_cooccurring_charges.md)

---

👤 **User**  
Group the charges into categories, but keeping the same table layout

---

🧠 **Assistant**  
I've reorganized the analysis with charges grouped into meaningful categories. Here are the key insights:

## Category Summary

Out of **6,854 drug possession cases**, co-occurring charges break down as follows:

1. **Drug Offenses** (52.66%) - Other drug-related charges like intent to distribute, cocaine possession, heroin, methamphetamine
2. **Firearm Offenses** (15.86%) - Felon in possession, firearms during commission of felony
3. **Obstruction/Law Enforcement** (10.39%) - Obstruction, false information, tampering with evidence
4. **Marijuana Offenses (Minor)** (6.41%) - Small quantity marijuana possession
5. **Drug Paraphernalia** (5.15%) - Drug-related objects, drugs not in original container
6. **Public Order/Nuisance** (4.55%) - Trespassing, loitering, pedestrian violations
7. **Traffic/Driving Offenses** (3.71%) - Suspended license, reckless driving, no insurance
8. **Property Crimes** (2.20%) - Theft by receiving stolen property

### Summary by Category

| Category | Total Cases | Percentage of Drug Possession Cases |
|----------|-------------|-------------------------------------|
| Drug Offenses | 3,609 | 52.66% |
| Firearm Offenses | 1,087 | 15.86% |
| Obstruction/Law Enforcement | 712 | 10.39% |
| Marijuana Offenses (Minor) | 439 | 6.41% |
| Drug Paraphernalia | 353 | 5.15% |
| Public Order/Nuisance | 312 | 4.55% |
| Traffic/Driving Offenses | 254 | 3.71% |
| Property Crimes | 151 | 2.20% |

The categorized table maintains the same layout showing individual charges within each category, sorted by frequency. This reveals that over half of drug possession cases involve additional drug charges, while nearly 16% involve firearms—highlighting the intersection between drug and weapons offenses in the criminal justice system.

Complete categorized breakdown available at: [drug_possession_categorized.md](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/drug_possession_categorized.md)

---

👤 **User**  
create a chat transcript

---

🧠 **Assistant**  
*Creating this chat transcript document*

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) on 2025-12-17*
