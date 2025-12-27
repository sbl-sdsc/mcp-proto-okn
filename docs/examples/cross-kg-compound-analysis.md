# Chat Transcript
## Chemical Compound Representations Analysis Across Open Knowledge Networks

👤 **User**  
Objective:
Analyze multiple knowledge graphs (KGs) accessible via the MCP service to identify, characterize, and compare chemical compound representations, with an emphasis on identifiers, normalization, and cross-KG interoperability.

Tasks

1. Chemical Compound Inventory

For each KG:

Identify all chemical compound representations, including:

* Compound names (preferred names, synonyms, trade names)
* Registry and database identifiers:

   * CAS Registry Number
   * PubChem CID
   * ChEMBL ID
   * DrugBank ID
   * InChI
   * InChIKey
   * SMILES
   * Other KG-specific or custom identifiers

* Distinguish between:

   * Small molecules
   * Drugs / approved therapeutics
   * Metabolites
   * Environmental chemicals / pollutants

* Report the number of compound instances per identifier type.

2. Summary Table

Create a consolidated table with (at minimum):

* KG name
* Compound entity type (e.g., SmallMolecule, Drug, Metabolite)
* Identifier type (CAS, PubChem CID, InChIKey, etc.)
* Identifier namespace / schema
* Number of instances
* Presence of synonyms / alternate names
* Availability of structural representations (SMILES, InChI, molecular graph)

3. Cross-KG Linking & Normalization Potential

* Identify which KGs share common chemical identifiers suitable for linking.
* Evaluate identifier reliability and uniqueness:

   * Canonical identifiers (InChIKey, PubChem CID)
   * Ambiguous or many-to-one identifiers (names, CAS)

* Describe strategies for:

   * Cross-KG compound alignment
   * Synonym resolution
   * Handling stereochemistry, salts, and mixtures

* Note schema or modeling differences (e.g., compound vs drug vs exposure agent).

4. Integration Opportunities & Use Cases

Describe use cases enabled by harmonized compound representations, such as:

* Linking compounds to:

   * Genes, proteins, pathways
   * Diseases and phenotypes
   * Environmental exposures
   * Assays, measurements, or experimental results

* Cross-KG drug repurposing analyses
* Chemical–biological interaction networks
* Exposure → biomarker → outcome modeling
* Federated queries over toxicology, pharmacology, and omics data

Output Requirements

* Provide one or more summary tables.
* Use KG-specific terminology where applicable.
* Clearly document assumptions, limitations, and missing identifier coverage.
* Highlight recommended canonical identifiers for integration.

---

🧠 **Assistant**  

I've completed a comprehensive analysis of chemical compound representations across the Open Knowledge Network (OKN) knowledge graphs. Here's a summary of the key findings:

## Executive Summary

This analysis examined chemical compound representations across 11 knowledge graphs (KGs) accessible via the FRINK MCP service. The analysis identifies identifier types, normalization approaches, cross-KG linking opportunities, and integration use cases for chemical compound data.

### Key Findings

1. **Over 7.1 million unique compound references** exist across the analyzed KGs
2. **CAS Registry Numbers** serve as the most common cross-KG identifier (present in 6 KGs)
3. **EPA DSSTox IDs (DTXSID)** provide robust linking for toxicology-focused KGs
4. **InChIKey** serves as the most reliable canonical identifier for structural matching
5. **PubChem CID** offers the largest reference namespace (~6.6 million compounds)

---

## 1. Chemical Compound Inventory by Knowledge Graph

### 1.1 SPOKE-OKN (Scalable Precision Medicine Open Knowledge Engine)

**Description**: Comprehensive biomedical and environmental health knowledge graph integrating genomics, environmental science, and public health data.

| Attribute | Value |
|-----------|-------|
| Total Compounds | 798 |
| Entity Type | biolink:ChemicalEntity |
| Primary Namespace | PubChem InChIKey (762), ChEBI (35), ChEMBL (1) |

**Identifier Coverage**:
- InChIKey (via PubChem): 762 compounds
- ChEBI IDs: 35 compounds
- ChEMBL IDs: 1 compound
- Labels: 798 (100% coverage)
- SMILES: Not present in current dataset
- Synonyms: Available via dedicated predicate

**Chemical Categories**: Environmental pollutants, pesticides, drugs, metabolites linked to diseases, genes, and geographic locations.

---

### 1.2 BioBricks Tox21

**Description**: Open knowledge graph for Tox21 toxicology screening data from high-throughput screening (qHTS) experiments.

| Attribute | Value |
|-----------|-------|
| Total Compounds | 8,947 |
| Entity Type | CHEMINF:000446 (Chemical Identifier) |
| Primary Namespace | CAS Registry Number |

**Identifier Coverage**:
- CAS Numbers: 8,947 (100%)
- Labels: 8,947 (100%)
- Source attribute: CAS

**Chemical Categories**: Predominantly environmental chemicals, industrial compounds, and drug-like molecules tested for toxicity.

---

### 1.3 BioBricks ICE (Integrated Chemical Environment)

**Description**: Comprehensive cheminformatics and chemical safety data from EPA's NICEATM ICE database.

| Attribute | Value |
|-----------|-------|
| Total Chemical Entities | 206,543 |
| Entity Type | biolink:ChemicalEntity |
| Primary Namespace | EPA DSSTox (DTXSID) |

**Identifier Coverage**:
- DSSTox Substance IDs (DTXSID): ~199,729
- CAS Numbers: ~199,729
- InChIKey: ~199,729 (via structure descriptors)
- Labels: High coverage

**Chemical Categories**: Environmental chemicals, pharmaceuticals, industrial compounds with bioassay data.

---

### 1.4 BioBricks ToxCast

**Description**: EPA ToxCast high-throughput screening data knowledge graph.

| Attribute | Value |
|-----------|-------|
| Total Compounds | 9,542 |
| Entity Type | biolink:ChemicalEntity |
| Primary Namespace | EPA DSSTox (DTXSID) + CAS |

**Identifier Coverage**:
- DSSTox IDs: 9,542 (100%)
- CAS Numbers: 9,542 (100%)
- Labels: 9,542 (100%)

**Chemical Categories**: Environmental chemicals and pesticides tested across 2,205 assay endpoints.

---

### 1.5 BioBricks PubChem Annotations

**Description**: Chemical annotations from PubChem covering regulatory data, physical properties, biological activities, and hazard information.

| Attribute | Value |
|-----------|-------|
| Unique Compounds | ~6,591,894 |
| Entity Type | oa:Annotation targets |
| Primary Namespace | PubChem CID |

**Identifier Coverage**:
- PubChem CID: ~6.6 million (100%)
- Total Annotations: 10,718,093

**Chemical Categories**: Broad coverage including drugs, environmental chemicals, natural products, metabolites.

---

### 1.6 BioBricks AOP-Wiki

**Description**: Adverse Outcome Pathways (AOPs) linking chemical exposures to adverse health outcomes.

| Attribute | Value |
|-----------|-------|
| Total Chemicals | 391 |
| Entity Type | CHEMINF:000446 |
| Primary Namespace | CAS Registry Number |

**Identifier Coverage**:
- CAS Numbers: 391 (100%)
- Cross-references: ChEBI, ChEMBL, PubChem, KEGG, Wikidata

**Chemical Categories**: Chemicals as molecular initiating event (MIE) stressors in toxicity pathways.

---

### 1.7 BioBricks MeSH

**Description**: Medical Subject Headings controlled vocabulary from the U.S. National Library of Medicine.

| Attribute | Value |
|-----------|-------|
| Chemical/Drug Descriptors | 10,413 |
| Supplementary Concepts | ~249,243 (chemical substances) |
| Entity Type | meshv:Descriptor, meshv:SupplementaryConcept |
| Primary Namespace | MeSH Descriptor ID |

**Identifier Coverage**:
- MeSH Tree Numbers: Category D (Chemicals and Drugs)
- Labels: 98%+ coverage
- Pharmacological Action links

**Chemical Categories**: Drugs, biological substances, inorganic compounds, organic compounds organized in hierarchical taxonomy.

---

### 1.8 SAWGraph PFAS KG

**Description**: Safe Agricultural Products and Water Graph for tracking PFAS and other contaminants in food and water systems.

| Attribute | Value |
|-----------|-------|
| Total Substances | 338 |
| Entity Type | coso:Substance |
| Primary Namespace | CAS Numbers (partial), Custom IDs |

**Identifier Coverage**:
- CAS Numbers: 133 (~39%)
- Substance IDs: Variable coverage
- Labels: 338 (100%)

**Chemical Categories**: PFAS compounds (perfluoroalkyl and polyfluoroalkyl substances), environmental contaminants, water pollutants.

---

### 1.9 SOC-KG (Soil Organic Carbon KG)

**Description**: Agricultural experimental data for soil carbon modeling and voluntary carbon markets.

| Attribute | Value |
|-----------|-------|
| Active Ingredients | 84 |
| Entity Type | sockg:ActiveIngredient |
| Primary Namespace | CAS (embedded in labels) |

**Identifier Coverage**:
- CAS Numbers: Embedded in label text (e.g., "Atrazine; CAS No. 1912-24-9")
- Labels: 84 (100%)

**Chemical Categories**: Pesticides, herbicides, fertilizer compounds used in agricultural management.

---

### 1.10 Other KGs Examined

The following KGs were examined but contain minimal or no direct chemical compound data:

| KG | Chemical Content |
|----|------------------|
| **DREAM-KG** | Social services focus; no chemical compounds |
| **Rural Resilience KG** | Health/justice focus; no direct chemical data |
| **Hydrology KG** | Water systems; potential contaminant data |
| **Climate Models KG** | Climate modeling; no direct chemical data |

---

## 2. Summary Table: Chemical Identifier Coverage

| KG Name | Entity Type | Compounds | CAS | DTXSID | PubChem CID | InChIKey | ChEBI | SMILES | Synonyms |
|---------|-------------|-----------|-----|--------|-------------|----------|-------|--------|----------|
| **SPOKE-OKN** | ChemicalEntity | 798 | ❌ | ❌ | ❌ | ✅ (762) | ✅ (35) | ❌ | ✅ |
| **Tox21** | Chemical Identifier | 8,947 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ICE** | ChemicalEntity | 206,543 | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **ToxCast** | ChemicalEntity | 9,542 | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **PubChem Annot.** | Annotation | 6,591,894 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | Partial |
| **AOP-Wiki** | Chemical Identifier | 391 | ✅ | ❌ | Xref | ❌ | Xref | ❌ | ❌ |
| **MeSH** | Descriptor | 10,413+ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **SAWGraph** | Substance | 338 | Partial | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **SOC-KG** | ActiveIngredient | 84 | In label | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Legend
- ✅ = Available as structured identifier
- ❌ = Not available
- Partial = Incomplete coverage
- In label = Embedded in text, not structured
- Xref = Available via cross-reference

---

## 3. Cross-KG Linking & Normalization Potential

### 3.1 Shared Identifier Analysis

The following identifier types enable cross-KG linking:

#### CAS Registry Number (Highest Overlap)
- **Present in**: Tox21, ICE, ToxCast, AOP-Wiki, SAWGraph (partial), SOC-KG (text)
- **URI Pattern**: `http://identifiers.org/cas/{number}` or `https://identifiers.org/cas/{number}`
- **Reliability**: High for unique identification, but many-to-one mappings exist for mixtures and salts
- **Example shared compound**: CAS 100-00-5 (1-Chloro-4-nitrobenzene) found in Tox21, ICE, ToxCast, and AOP-Wiki

#### EPA DSSTox Substance ID (DTXSID)
- **Present in**: ICE, ToxCast
- **URI Pattern**: `https://comptox.epa.gov/dashboard/chemical/details/{DTXSID}`
- **Reliability**: Very high - curated by EPA, unique per chemical structure
- **Advantage**: Links to extensive CompTox Dashboard data

#### PubChem CID
- **Present in**: PubChem Annotations (primary), SPOKE-OKN (via InChIKey)
- **URI Pattern**: `http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID{number}`
- **Reliability**: High for unique structures; represents standardized compounds

#### InChIKey
- **Present in**: SPOKE-OKN (as URI component), ICE (structure descriptor)
- **Format**: 27-character hash (e.g., `AAEVYOVXGOFMJO-UHFFFAOYSA-N`)
- **Reliability**: Highest - canonical structural identifier, stereochemistry-aware
- **Advantage**: Structure-based, database-independent

### 3.2 Identifier Reliability Assessment

| Identifier | Uniqueness | Ambiguity Risk | Recommended Use |
|------------|------------|----------------|-----------------|
| **InChIKey** | Canonical | Very Low | Primary linking key |
| **PubChem CID** | Unique | Low | Cross-reference validation |
| **DTXSID** | Unique | Very Low | EPA data integration |
| **CAS Number** | Often unique | Medium | Legacy system linking |
| **Compound Name** | Non-unique | High | Human reference only |
| **MeSH ID** | Unique | Low (broader concepts) | Literature indexing |

### 3.3 Normalization Strategies

#### Strategy 1: CAS-Based Federation
```sparql
# Federated query template across CAS-indexed KGs
SELECT ?chem ?label ?kg_source
WHERE {
  VALUES ?cas_uri { <http://identifiers.org/cas/100-00-5> }
  SERVICE <tox21_endpoint> { ?chem ?p ?cas_uri . }
  SERVICE <ice_endpoint> { ?chem ?p2 ?cas_uri . }
}
```

**Applicable KGs**: Tox21, ICE, ToxCast, AOP-Wiki

#### Strategy 2: DTXSID-Based Federation
```sparql
# Cross-reference via EPA DSSTox IDs
SELECT ?chem ?assay_result
WHERE {
  ?chem <has_identifier> ?dtxsid .
  FILTER(CONTAINS(STR(?dtxsid), "DTXSID5020281"))
}
```

**Applicable KGs**: ICE, ToxCast

#### Strategy 3: Structure-Based Matching
For KGs with InChIKey or SMILES, use structure matching:
- Convert SMILES to canonical InChIKey
- Match first 14 characters (connectivity layer) for non-stereospecific matching
- Full 27-character match for exact structures

### 3.4 Handling Complex Cases

#### Stereochemistry
- InChIKey encodes stereochemistry in characters 15-27
- For stereoisomer-agnostic queries, match only first 14 characters (connectivity layer)

#### Salts and Hydrates
- Different CAS numbers may exist for free base vs. salt forms
- Use DSSTox "preferred name" or PubChem parent compound for normalization
- Example: "Methyl viologen dichloride hydrate" (CAS 75365-73-0) vs. "Paraquat" (CAS 4685-14-7)

#### Mixtures
- SAWGraph PFAS data includes mixture categories (e.g., "Total PFAS")
- Represent as SubstanceCollection where individual components aren't measured
- Link to constituent compounds where known

#### Name Variants
- Build synonym tables from MeSH and PubChem
- Use exact string matching on preferred names, fuzzy matching on synonyms
- Example: "4-Nitroaniline" = "p-Nitroaniline" = "4-Nitrobenzenamine"

---

## 4. Integration Opportunities & Use Cases

### 4.1 Chemical-Biological Interaction Networks

**Use Case**: Build comprehensive chemical-biological interaction networks by linking compounds across KGs to their biological targets.

**Integrable Data**:
| KG | Data Type |
|----|-----------|
| SPOKE-OKN | Compound-Gene (upregulates/downregulates), Compound-Disease |
| ICE | Bioassay results, mechanistic targets |
| ToxCast | High-throughput screening endpoints |
| AOP-Wiki | Molecular initiating events, key events |
| MeSH | Pharmacological actions |

### 4.2 Drug Repurposing Analysis

**Use Case**: Identify existing drugs with activity profiles suggesting potential new indications.

**Workflow**:
1. Query SPOKE-OKN for drugs with known disease associations
2. Cross-reference with ICE/ToxCast for mechanism data
3. Use AOP-Wiki to understand adverse outcome risks
4. Validate with MeSH pharmacological classifications

**Value**: Leverage existing safety data and mechanism understanding for computational drug repositioning.

### 4.3 Environmental Exposure → Biomarker → Outcome Modeling

**Use Case**: Track contaminant exposure pathways from environmental presence to health outcomes.

**Data Flow**:
```
SAWGraph (PFAS measurements)
    ↓ (CAS linking)
ICE/ToxCast (biological activity)
    ↓ (mechanism)
AOP-Wiki (adverse outcome pathways)
    ↓ (health outcomes)
SPOKE-OKN (disease prevalence, geographic distribution)
```

### 4.4 Toxicology Data Integration

**Use Case**: Federated queries over toxicology, pharmacology, and omics data for chemical hazard assessment.

**Integrable Resources**:
| Data Type | Source KG |
|-----------|-----------|
| qHTS Screening | Tox21 |
| Bioassay Results | ICE |
| Assay Endpoints | ToxCast |
| Adverse Outcomes | AOP-Wiki |
| Chemical Annotations | PubChem |
| Disease Associations | SPOKE-OKN |
| Biomedical Vocabulary | MeSH |

### 4.5 Agricultural Chemical Safety

**Use Case**: Link pesticide usage data with environmental fate and health outcomes.

**Workflow**:
1. SOC-KG: Identify active ingredients in agricultural treatments
2. Parse embedded CAS numbers for cross-reference
3. Query Tox21/ToxCast for toxicity profiles
4. Link to SPOKE-OKN for environmental presence data

---

## 5. Limitations and Missing Coverage

### 5.1 Identifier Gaps

| Gap | Affected KGs | Impact |
|-----|--------------|--------|
| No InChIKey | Tox21, ToxCast, AOP-Wiki, MeSH | Structural matching limited |
| No SMILES | All KGs except annotations | 2D structure queries unavailable |
| CAS only in text | SOC-KG | Requires text parsing for linking |
| No DrugBank IDs | All KGs | Pharmaceutical data linking limited |
| No ChEMBL IDs | Most KGs | Drug-like property queries limited |

### 5.2 Schema Heterogeneity

| Issue | Description |
|-------|-------------|
| **Entity typing** | "ChemicalEntity" vs "Substance" vs "Chemical Identifier" vs "Descriptor" |
| **Relationship modeling** | Compound-disease as direct edges (SPOKE) vs. via AOPs (AOP-Wiki) |
| **Measurement context** | ToxCast stores activity values; SAWGraph stores environmental concentrations |
| **URI schemes** | HTTP vs HTTPS identifiers.org URIs require normalization |

---

## 6. Recommendations

### 6.1 Canonical Identifiers for Integration

**Primary**: InChIKey
- Structure-based, canonical
- Enables exact structural matching
- Recommendation: Generate for all KGs lacking this identifier

**Secondary**: PubChem CID
- Widely adopted reference
- Links to extensive annotation data
- Recommendation: Map CAS and DTXSID to PubChem CID via API

**Tertiary**: EPA DTXSID
- High-quality curated identifiers
- Essential for regulatory/toxicology applications
- Recommendation: Use for EPA data alignment

### 6.2 Cross-KG Alignment Strategy

1. **Build identifier mapping table**: CAS → DTXSID → InChIKey → PubChem CID
2. **Normalize URI patterns**: Standardize http/https and identifiers.org usage
3. **Create bridging predicates**: owl:sameAs or skos:exactMatch between chemical entities
4. **Handle name variants**: Build authoritative synonym table from MeSH + PubChem

### 6.3 Priority Integration Targets

| Integration | KGs Involved | Value |
|-------------|--------------|-------|
| Toxicology Hub | Tox21 + ICE + ToxCast | Unified toxicity screening data |
| Exposure-Outcome | SAWGraph + AOP-Wiki + SPOKE | Environmental health pathways |
| Drug Safety | SPOKE + ICE + MeSH | Pharmacovigilance support |

---

## Deliverables

Two files have been created with the complete analysis:

1. **chemical_compound_kg_analysis.md** - Comprehensive markdown report with full details
2. **chemical_compound_kg_analysis.xlsx** - Excel workbook with 5 sheets:
   - Compound Inventory
   - Identifier Coverage Matrix
   - Cross-KG Linking Opportunities
   - Integration Use Cases
   - Recommendations

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.4.0 for spoke-okn on 2025-12-26*

Model: claude-opus-4-5-20250514
