#!/usr/bin/env python3
"""
Build the graph registry (config/registry.json) from existing metadata sources.

Sources:
- metadata/descriptions/{kg_name}.txt → description_summary
- metadata/entities/{kg_name}_entities.csv → entity_types (also defines the
  canonical list of graph names — every graph must have an entities CSV)
- Hardcoded domain tag, identifier namespace, and example-query mappings below

Endpoint URLs are derived from the canonical graph name as
`https://apps.okn.us/{kg_name}/sparql`.
"""

import csv
import json
import os
import sys

# Project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Domain tag mapping (from README domain table and analysis)
DOMAIN_TAGS = {'biobricks-aopwiki': ['biology', 'health', 'toxicology'],
 'biobricks-ice': ['biology', 'chemistry', 'toxicology'],
 'biobricks-mesh': ['biology', 'health', 'vocabulary'],
 'biobricks-pubchem-annotations': ['chemistry', 'pharmacology', 'toxicology'],
 'biobricks-tox21': ['chemistry', 'toxicology'],
 'biobricks-toxcast': ['chemistry', 'toxicology'],
 'biohealth': ['biology', 'health', 'social_determinants'],
 'biomarkerkg': ['biomarkers', 'biomedical', 'disease', 'genomics'],
 'climatemodelskg': ['climate', 'environment', 'geospatial'],
 'digcfdekg': ['biomedical', 'disease', 'genomics', 'phenotypes'],
 'dreamkg': ['homelessness', 'social_services'],
 'evoweb': ['comparative_genomics',
            'microbial_systems_biology',
            'protein_function',
            'protein_interactions'],
 'fiokg': ['environment', 'industry', 'regulatory'],
 'gene-expression-atlas-okn': ['biology', 'genomics', 'health'],
 'geoconnex': ['environment', 'geospatial', 'hydrology'],
 'hydrologykg': ['environment', 'hydrology', 'water_quality'],
 'medical-device-kg': ['adverse_events', 'medical_devices'],
 'nasa-gesdisc-kg': ['climate', 'earth_science', 'geospatial'],
 'ncipidkg': ['biology', 'biomedical', 'cancer', 'pathways'],
 'nde': ['data_discovery', 'health', 'infectious_disease'],
 'nikg': ['geospatial', 'public_safety', 'urban_planning'],
 'oard-kg': ['clinical_data', 'health', 'phenotypes', 'rare_disease'],
 'phaseskg': ['aging_research', 'health'],
 'pankgraph': ['biomedical', 'diabetes', 'genomics', 'pancreas', 'regulatory_genomics'],
 'prokn': ['biomedical',
           'drug_discovery',
           'genetic_variants',
           'pathways',
           'post_translational_modification',
           'precision_medicine',
           'protein_knowledge'],
 'rdkg': ['biomedical', 'disease', 'genomics', 'phenotypes', 'rare_disease'],
 'ruralkg': ['criminal_justice', 'health', 'rural_health'],
 'sawgraph': ['environment', 'food_safety', 'PFAS', 'water_quality'],
 'scales': ['criminal_justice', 'legal'],
 'securechainkg': ['software_security', 'supply_chain'],
 'sockg': ['agriculture', 'climate', 'soil_science'],
 'spatialkg': ['administrative_boundaries', 'geospatial'],
 'spoke-genelab': ['biology', 'genomics', 'space_biology'],
 'spoke-okn': ['biology', 'chemistry', 'environment', 'geospatial', 'health'],
 'sudokn': ['manufacturing', 'supply_chain'],
 'ufokn': ['emergency_response', 'infrastructure', 'urban_flooding'],
 'wildlifekn': ['biodiversity', 'conservation', 'wildlife']}

# Identifier namespace mapping
IDENTIFIER_NAMESPACES = {'biobricks-aopwiki': ['CAS', 'ChEBI', 'ChEMBL', 'InChIKey', 'PubChem'],
 'biobricks-ice': ['CAS', 'DTXSID', 'InChIKey', 'NCBI_Gene'],
 'biobricks-mesh': ['MeSH'],
 'biobricks-pubchem-annotations': ['InChI', 'InChIKey', 'PubChem', 'SMILES'],
 'biobricks-tox21': ['CAS'],
 'biobricks-toxcast': ['CAS', 'DTXSID', 'InChIKey'],
 'biohealth': ['MeSH', 'MONDO', 'UMLS'],
 'biomarkerkg': ['DOID', 'NCBI_Gene', 'OBCI', 'OMIM', 'PubChem', 'UBERON'],
 'climatemodelskg': ['GeoNames'],
 'digcfdekg': ['NCBI_Gene', 'Orphanet', 'EFO', 'MONDO', 'HPO'],
 'dreamkg': [],
 'evoweb': ['NCBI_Protein', 'RefSeq'],
 'fiokg': ['FIPS', 'NAICS', 'S2Cell'],
 'gene-expression-atlas-okn': ['CL', 'Ensembl', 'GeneSymbol', 'GO', 'NCBI_Gene', 'UBERON'],
 'geoconnex': ['Geoconnex'],
 'hydrologykg': ['FIPS', 'NHDPlus_COMID', 'S2Cell'],
 'medical-device-kg': ['DCTERMS',
             'FDA_Product_Code',
             'LDF_VOID_EXT',
             'MedicalDevice_Ontology',
             'PAV',
             'VOID'],
 'nasa-gesdisc-kg': ['DOI', 'GCMD', 'NASA_CMR', 'OpenAlex', 'ORCID', 'ROR'],
 'ncipidkg': ['GO', 'INDRA', 'NCI-PID', 'RDF', 'RO', 'VoID'],
 'nde': ['PubMed'],
 'nikg': ['FIPS'],
 'oard-kg': ['HPO', 'MONDO', 'UMLS'],
 'phaseskg': ['BCIO',
              'BCIOR',
              'BFO',
              'DC',
              'DCTERMS',
              'GO',
              'IAO',
              'MF',
              'MFOEM',
              'OBI',
              'oboInOwl',
              'OGMS',
              'OMO',
              'OWL',
              'PAV',
              'PHASES',
              'RDF',
              'RDFS',
              'RO',
              'Schema.org',
              'SDGIO',
              'SKOS',
              'VOID',
              'VOID-EXT',
              'Wikidata'],                   
 'pankgraph': ['BioSample',
               'dbSNP',
               'Ensembl',
               'GEO',
               'GO',
               'HGNC',
               'NCBI_Gene',
               'PanKbase',
               'PubMed',
               'SO'],
 'prokn': ['BAO',
           'EC_Number',
           'Ensembl',
           'GO',
           'InChIKey',
           'NCBI_Taxon',
           'NCIT',
           'PubMed',
           'SMILES',
           'UniProt'],
 'rdkg': ['MONDO', 'Orphanet', 'OMIM', 'UMLS', 'NCBI_Gene', 'HPO'],
 'ruralkg': ['FIPS', 'RUCC'],
 'sawgraph': ['CAS'],
 'scales': [],
 'securechainkg': ['CPE', 'CVE'],
 'sockg': [],
 'spatialkg': ['FIPS', 'S2Cell'],
 'spoke-genelab': ['CL', 'GeneSymbol', 'NCBI_Gene', 'UBERON'],
 'spoke-okn': ['ChEBI', 'DOID', 'Ensembl', 'FIPS', 'InChIKey', 'TAXON'],
 'sudokn': ['NAICS'],
 'ufokn': ['S2Cell'],
 'wildlifekn': []}

# Example queries per graph
EXAMPLE_QUERIES = {'biobricks-aopwiki': ['What adverse outcome pathways involve estrogen receptor activation?'],
 'biobricks-ice': ['What bioassays are available for a specific chemical?',
                   'What is the toxicity profile of bisphenol A?'],
 'biobricks-tox21': ['What chemicals have been tested in Tox21 assays?'],
 'biobricks-toxcast': ['What high-throughput screening results exist for PFAS chemicals?'],
 'biohealth': ['What social determinants are associated with diabetes?'],
 'biomarkerkg': ['What biomarkers are diagnostic for a specific disease?',
                 'Which genes or compounds indicate the risk of developing a disease?',
                 'What tissue or anatomical sample is used to measure a biomarker?'],
 'climatemodelskg': ['What climate models cover a specific region?'],
 'digcfdekg': ['What genes are associated with a specific trait or disease?',
               'Which latent disease-mechanism factors connect genes to a phenotype?',
               'What CFDE gene sets predict relevance for a given trait?'],
 'dreamkg': ['What social services are available for homeless individuals?'],
 'evoweb': ['What proteins are members of a co-evolving protein group?',
            'What co-evolving genes may participate in shared protein complexes or pathways?'],
 'fiokg': ['What regulated facilities exist in a county?'],
 'gene-expression-atlas-okn': ['What genes are differentially expressed in breast cancer?',
                               'What tissues show high expression of BRCA1?'],
 'geoconnex': ['What monitoring sites exist in a watershed?'],
 'hydrologykg': ['What is the hydrological connectivity between surface water features?'],
 'medical-device-kg': ['What event types are reported for a specific medical device?'],
 'nasa-gesdisc-kg': ['Which datasets does a specific NASA data center or DAAC distribute?',
                     'What platform and instrument collected a given dataset, and which project is it part of?',
                     'Which publications and authors use a specific dataset, and what other datasets are frequently used with it?'],
 'ncipidkg': ['What proteins directly regulate EGFR in NCI-PID pathways?',
              'Which molecular interactions have evidence counts and evidence URLs?',
              'What pathway relationships are annotated with Gene Ontology process or '
              'post-translational-modification types?'],
 'nikg': ['What incidents occurred in specific neighborhoods?'],
 'oard-kg': ['What phenotypes are associated with a specific rare disease?',
             'Which rare disease associations have supporting studies with log odds ratio '
             'evidence?',
             'What phenotype-phenotype associations are supported by clinical data?'],
 'phaseskg': ['Which factors or behaviors are associated with healthy aging?'],
 'pankgraph': ['What genes are associated with type 1 diabetes in pancreatic islets?',
               'Which SNPs or SNVs are linked to type 1 diabetes genes?',
               'What eQTL or fine-mapping evidence connects variants to pancreatic gene '
               'expression?'],
 'prokn': ['What post-translational modification annotations are available for a specific protein '
           'such as APOE?',
           'Which protein kinases or kinase-substrate relationships are connected to a protein of '
           'interest?',
           'What genetic variants, pathways, or disease annotations are associated with a UniProt '
           'protein?'],
 'rdkg': ['What genes are associated with a specific rare disease?',
          'What phenotypes and mode of inheritance are linked to a rare disease?',
          'How is a rare disease cross-referenced across MONDO, Orphanet, and OMIM?'],
 'ruralkg': ['What substance abuse treatment providers are in rural counties?',
             'What is the relationship between rurality and mental health services?'],
 'sawgraph': ['Where have PFAS been detected in drinking water?',
              'What food products contain contaminants?'],
 'scales': ['How many criminal cases were filed in federal court?'],
 'securechainkg': ['What vulnerabilities affect a Python package?'],
 'sockg': ['What soil carbon measurements exist for different tillage practices?'],
 'spatialkg': ['What administrative regions contain a specific location?'],
 'spoke-genelab': ['What genes are differentially expressed in spaceflight experiments?',
                   'What are the mouse orthologs of human disease genes?',
                   'What methylation changes occur in spaceflight studies?'],
 'spoke-okn': ['What drugs treat rheumatoid arthritis?',
               "What genes are associated with Crohn's disease?",
               'What is the prevalence of diabetes in California counties?',
               'What compounds are found in water supplies in Texas?'],
 'sudokn': ['What manufacturers have specific process capabilities?']}

# Aliases: alternate names that resolve to a canonical graph name. Useful when
# a graph is commonly referred to by a short name (e.g. "spoke" → "spoke-okn").
ALIASES = {
    "spoke": "spoke-okn",
}


def load_description(kg_name):
    """Load description from metadata/descriptions/{kg_name}.txt."""
    desc_path = os.path.join(ROOT, "metadata", "descriptions", f"{kg_name}.txt")
    if os.path.exists(desc_path):
        with open(desc_path) as f:
            return f.read().strip()
    return ""


def load_entities(kg_name):
    """Load entity types from metadata/entities/{kg_name}_entities.csv."""
    entity_path = os.path.join(ROOT, "metadata", "entities", f"{kg_name}_entities.csv")
    if not os.path.exists(entity_path):
        return {"classes": [], "predicates": [], "has_edge_properties": False}

    classes = []
    predicates = []
    has_edge_properties = False

    with open(entity_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            entity_type = row.get("Type", "").strip()
            label = row.get("Label", "").strip()
            if not label:
                continue

            if entity_type == "Class":
                if label not in classes:
                    classes.append(label)
            elif entity_type == "Predicate":
                if label not in predicates:
                    predicates.append(label)
            elif entity_type == "EdgeProperty":
                has_edge_properties = True

    return {
        "classes": classes,
        "predicates": predicates,
        "has_edge_properties": has_edge_properties,
    }


def build_registry():
    """Build the complete registry."""
    registry = []

    # Canonical graph names come from the metadata directory: every graph
    # has either an entity file, a description file, or both.
    entity_dir = os.path.join(ROOT, "metadata", "entities")
    desc_dir = os.path.join(ROOT, "metadata", "descriptions")
    all_names = set()
    if os.path.exists(entity_dir):
        for f in os.listdir(entity_dir):
            if f.endswith("_entities.csv"):
                all_names.add(f.replace("_entities.csv", ""))
    if os.path.exists(desc_dir):
        for f in os.listdir(desc_dir):
            if f.endswith(".txt"):
                all_names.add(f.replace(".txt", ""))

    for kg_name in sorted(all_names):
        endpoint_url = f"https://apps.okn.us/{kg_name}/sparql"

        # Build named graph URI
        named_graph_uri = f"https://purl.org/okn/frink/kg/{kg_name}"

        # Build display name
        display_name = kg_name.replace("-", " ").title()

        # Load metadata
        description = load_description(kg_name)
        entities = load_entities(kg_name)
        domain_tags = DOMAIN_TAGS.get(kg_name, [])
        id_namespaces = IDENTIFIER_NAMESPACES.get(kg_name, [])
        examples = EXAMPLE_QUERIES.get(kg_name, [])

        # Build aliases list
        aliases = [
            alias for alias, canonical in ALIASES.items()
            if canonical == kg_name and alias != kg_name
        ]

        entry = {
            "name": kg_name,
            "display_name": display_name,
            "named_graph_uri": named_graph_uri,
            "endpoint_url": endpoint_url,
            "domain_tags": domain_tags,
            "description_summary": description,
            "entity_types": entities,
            "identifier_namespaces": id_namespaces,
            "example_queries": examples,
        }
        if aliases:
            entry["aliases"] = aliases

        registry.append(entry)

    return registry


def main():
    registry = build_registry()
    output_path = os.path.join(ROOT, "config", "registry.json")
    with open(output_path, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Built registry with {len(registry)} graphs → {output_path}")


if __name__ == "__main__":
    main()
