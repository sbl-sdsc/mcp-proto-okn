#!/usr/bin/env python3
"""
Build the graph registry (config/registry.json) from existing metadata sources.

Sources:
- metadata/descriptions/{kg_name}.txt → description_summary
- metadata/entities/{kg_name}_entities.csv → entity_types
- config/mcp.json → canonical list of graph names and endpoint URLs
- Hardcoded domain tag mapping and identifier namespace mapping
"""

import csv
import json
import os
import sys

# Project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Domain tag mapping (from README domain table and analysis)
DOMAIN_TAGS = {
    "biobricks-aopwiki": ["toxicology", "biology", "health"],
    "biobricks-ice": ["toxicology", "chemistry", "biology"],
    "biobricks-mesh": ["biology", "health", "vocabulary"],
    "biobricks-pubchem-annotations": ["chemistry", "toxicology", "pharmacology"],
    "biobricks-tox21": ["toxicology", "chemistry"],
    "biobricks-toxcast": ["toxicology", "chemistry"],
    "biohealth": ["biology", "health", "social_determinants"],
    "climatemodelskg": ["climate", "environment", "geospatial"],
    "dreamkg": ["social_services", "homelessness"],
    "fiokg": ["environment", "regulatory", "industry"],
    "gene-expression-atlas-okn": ["genomics", "biology", "health"],
    "geoconnex": ["hydrology", "geospatial", "environment"],
    "hydrologykg": ["hydrology", "environment", "water_quality"],
    "nasa-gesdisc-kg": ["climate", "earth_science", "geospatial"],
    "nde": ["infectious_disease", "health", "data_discovery"],
    "nikg": ["public_safety", "urban_planning", "geospatial"],
    "ruralkg": ["rural_health", "health", "criminal_justice"],
    "sawgraph": ["food_safety", "water_quality", "PFAS", "environment"],
    "scales": ["criminal_justice", "legal"],
    "securechainkg": ["software_security", "supply_chain"],
    "sockg": ["agriculture", "soil_science", "climate"],
    "spatialkg": ["geospatial", "administrative_boundaries"],
    "spoke-genelab": ["genomics", "space_biology", "biology"],
    "spoke-okn": ["biology", "health", "chemistry", "environment", "geospatial"],
    "sudokn": ["manufacturing", "supply_chain"],
    "ufokn": ["urban_flooding", "infrastructure", "emergency_response"],
    "wildlifekn": ["wildlife", "biodiversity", "conservation"],
}

# Identifier namespace mapping
IDENTIFIER_NAMESPACES = {
    "biobricks-aopwiki": ["CAS", "ChEBI", "ChEMBL", "PubChem", "InChIKey"],
    "biobricks-ice": ["DTXSID", "NCBI_Gene", "InChIKey", "CAS"],
    "biobricks-mesh": ["MeSH"],
    "biobricks-pubchem-annotations": ["PubChem", "InChI", "InChIKey", "SMILES"],
    "biobricks-tox21": ["CAS"],
    "biobricks-toxcast": ["DTXSID", "InChIKey", "CAS"],
    "biohealth": ["MONDO", "MeSH", "UMLS"],
    "climatemodelskg": ["GeoNames"],
    "dreamkg": [],
    "fiokg": ["NAICS", "S2Cell", "FIPS"],
    "gene-expression-atlas-okn": ["NCBI_Gene", "Ensembl", "GeneSymbol", "UBERON", "CL", "GO"],
    "geoconnex": ["Geoconnex"],
    "hydrologykg": ["NHDPlus_COMID", "FIPS", "S2Cell"],
    "nasa-gesdisc-kg": [],
    "nde": ["PubMed"],
    "nikg": ["FIPS"],
    "ruralkg": ["FIPS", "RUCC"],
    "sawgraph": ["CAS"],
    "scales": [],
    "securechainkg": ["CVE", "CPE"],
    "sockg": [],
    "spatialkg": ["S2Cell", "FIPS"],
    "spoke-genelab": ["NCBI_Gene", "GeneSymbol", "UBERON", "CL"],
    "spoke-okn": ["Ensembl", "MONDO", "ChEBI", "InChIKey", "FIPS"],
    "sudokn": ["NAICS"],
    "ufokn": ["S2Cell"],
    "wildlifekn": [],
}

# Example queries per graph
EXAMPLE_QUERIES = {
    "spoke-okn": [
        "What drugs treat rheumatoid arthritis?",
        "What genes are associated with Crohn's disease?",
        "What is the prevalence of diabetes in California counties?",
        "What compounds are found in water supplies in Texas?",
    ],
    "spoke-genelab": [
        "What genes are differentially expressed in spaceflight experiments?",
        "What are the mouse orthologs of human disease genes?",
        "What methylation changes occur in spaceflight studies?",
    ],
    "gene-expression-atlas-okn": [
        "What genes are differentially expressed in breast cancer?",
        "What tissues show high expression of BRCA1?",
    ],
    "biobricks-tox21": [
        "What chemicals have been tested in Tox21 assays?",
    ],
    "biobricks-ice": [
        "What bioassays are available for a specific chemical?",
        "What is the toxicity profile of bisphenol A?",
    ],
    "biobricks-toxcast": [
        "What high-throughput screening results exist for PFAS chemicals?",
    ],
    "biobricks-aopwiki": [
        "What adverse outcome pathways involve estrogen receptor activation?",
    ],
    "sawgraph": [
        "Where have PFAS been detected in drinking water?",
        "What food products contain contaminants?",
    ],
    "ruralkg": [
        "What substance abuse treatment providers are in rural counties?",
        "What is the relationship between rurality and mental health services?",
    ],
    "scales": [
        "How many criminal cases were filed in federal court?",
    ],
    "dreamkg": [
        "What social services are available for homeless individuals?",
    ],
    "biohealth": [
        "What social determinants are associated with diabetes?",
    ],
    "nikg": [
        "What incidents occurred in specific neighborhoods?",
    ],
    "geoconnex": [
        "What monitoring sites exist in a watershed?",
    ],
    "hydrologykg": [
        "What is the hydrological connectivity between surface water features?",
    ],
    "climatemodelskg": [
        "What climate models cover a specific region?",
    ],
    "securechainkg": [
        "What vulnerabilities affect a Python package?",
    ],
    "sockg": [
        "What soil carbon measurements exist for different tillage practices?",
    ],
    "sudokn": [
        "What manufacturers have specific process capabilities?",
    ],
    "spatialkg": [
        "What administrative regions contain a specific location?",
    ],
    "fiokg": [
        "What regulated facilities exist in a county?",
    ],
}

# Aliases: map mcp.json names to entity file names
ALIASES = {
    "spoke": "spoke-okn",
    "gene-expression-altlas-okn": "gene-expression-atlas-okn",  # typo in mcp.json
}


def load_mcp_config():
    """Load graph names and endpoints from mcp.json."""
    config_path = os.path.join(ROOT, "config", "mcp.json")
    with open(config_path) as f:
        config = json.load(f)

    graphs = {}
    for name, server in config.get("servers", {}).items():
        args = server.get("args", [])
        endpoint_url = None
        for i, arg in enumerate(args):
            if arg == "--endpoint" and i + 1 < len(args):
                endpoint_url = args[i + 1]
                break
        if endpoint_url:
            # Resolve canonical name
            canonical = ALIASES.get(name, name)
            if canonical not in graphs:
                graphs[canonical] = {
                    "endpoint_url": endpoint_url,
                    "mcp_name": name,
                }
    return graphs


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
    mcp_graphs = load_mcp_config()
    registry = []

    # Collect all canonical names from entity files + mcp config
    entity_dir = os.path.join(ROOT, "metadata", "entities")
    entity_names = set()
    if os.path.exists(entity_dir):
        for f in os.listdir(entity_dir):
            if f.endswith("_entities.csv"):
                name = f.replace("_entities.csv", "")
                entity_names.add(name)

    # Merge with mcp config names
    all_names = set(mcp_graphs.keys()) | entity_names

    # Remove non-FRINK endpoints
    non_frink = set()
    for name in all_names:
        info = mcp_graphs.get(name, {})
        url = info.get("endpoint_url", "")
        if url and "frink.apps.renci.org" not in url:
            non_frink.add(name)
    all_names -= non_frink

    for kg_name in sorted(all_names):
        info = mcp_graphs.get(kg_name, {})
        endpoint_url = info.get("endpoint_url", f"https://frink.apps.renci.org/{kg_name}/sparql")

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
        aliases = []
        for alias, canonical in ALIASES.items():
            if canonical == kg_name and alias != kg_name:
                aliases.append(alias)
        # Also add the mcp_name if different
        mcp_name = info.get("mcp_name")
        if mcp_name and mcp_name != kg_name and mcp_name not in aliases:
            aliases.append(mcp_name)

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
