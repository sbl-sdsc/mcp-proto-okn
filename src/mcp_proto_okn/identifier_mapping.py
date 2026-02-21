"""
Identifier mapping and join strategy helpers for cross-graph analysis.

Provides static bridge tables mapping identifier types to graphs and their
URI patterns, plus functions for finding common identifiers and suggesting
join strategies between graphs.
"""

from typing import Any, Dict, List, Optional


# Maps identifier types to the graphs that use them and how
IDENTIFIER_BRIDGES: Dict[str, Dict[str, Dict[str, str]]] = {
    # Gene identifiers
    "NCBI_Gene": {
        "spoke-genelab": {
            "description": "NCBI Entrez Gene ID as node URI",
            "uri_pattern": "Gene node URI contains Entrez ID",
            "property": "symbol (for gene symbol lookup)",
        },
        "gene-expression-atlas-okn": {
            "description": "NCBI Gene ID as node property",
            "property": "https://spoke.ucsf.edu/genelab/ncbi_gene_id",
        },
        "biobricks-ice": {
            "description": "Entrez Gene ID for assay targets",
            "property": "https://ice.ntp.niehs.nih.gov/property/assay_entrez_gene_id",
        },
    },
    "Ensembl": {
        "spoke-okn": {
            "description": "Ensembl ID as node property on Gene",
            "property": "https://purl.org/okn/frink/kg/spoke-okn/schema/ensembl",
        },
        "gene-expression-atlas-okn": {
            "description": "Ensembl ID as node property on Gene",
            "property": "https://spoke.ucsf.edu/genelab/ensembl_id",
        },
    },
    "GeneSymbol": {
        "spoke-genelab": {
            "description": "Gene symbol as node property",
            "property": "https://purl.org/okn/frink/kg/spoke-genelab/schema/symbol",
        },
        "gene-expression-atlas-okn": {
            "description": "Gene symbol as node property",
            "property": "https://w3id.org/biolink/vocab/symbol",
        },
    },
    # Chemical identifiers
    "CAS": {
        "biobricks-tox21": {
            "description": "CAS Registry Number via identifiers.org URIs",
            "uri_pattern": "https://identifiers.org/cas:",
        },
        "biobricks-ice": {
            "description": "CAS number in chemical identifiers",
        },
        "biobricks-toxcast": {
            "description": "CAS number in chemical records",
        },
        "biobricks-aopwiki": {
            "description": "CAS number for chemical stressors",
        },
        "sawgraph": {
            "description": "CAS number for contaminant substances",
            "property": "casNumber",
        },
    },
    "DTXSID": {
        "biobricks-ice": {
            "description": "EPA DSSTox Substance ID",
        },
        "biobricks-toxcast": {
            "description": "EPA DSSTox Substance ID",
        },
    },
    "InChIKey": {
        "spoke-okn": {
            "description": "InChIKey via database cross-references",
        },
        "biobricks-ice": {
            "description": "InChIKey for chemical structure matching",
        },
        "biobricks-toxcast": {
            "description": "InChIKey in chemical structure descriptors",
        },
        "biobricks-aopwiki": {
            "description": "InChIKey for chemical stressors",
        },
    },
    # Disease identifiers
    "MONDO": {
        "spoke-okn": {
            "description": "MONDO disease ontology URIs",
            "uri_pattern": "http://purl.obolibrary.org/obo/MONDO_",
        },
        "biohealth": {
            "description": "MONDO disease identifiers",
        },
    },
    # Location identifiers
    "FIPS": {
        "spoke-okn": {
            "description": "FIPS codes for counties/states",
            "property": "https://purl.org/okn/frink/kg/spoke-okn/schema/state_fips",
        },
        "nikg": {
            "description": "FIPS codes for census tracts",
        },
        "ruralkg": {
            "description": "FIPS codes for counties",
        },
        "spatialkg": {
            "description": "FIPS codes for administrative regions",
        },
        "hydrologykg": {
            "description": "FIPS codes for water system locations",
        },
    },
    "S2Cell": {
        "spatialkg": {
            "description": "S2 Cell IDs (Level 13) for spatial indexing",
        },
        "hydrologykg": {
            "description": "S2 Cell IDs for water features",
        },
        "fiokg": {
            "description": "S2 Cell IDs for facility locations",
        },
        "ufokn": {
            "description": "S2 Cell IDs for flood risk points",
        },
    },
    # Biomedical vocabularies
    "MeSH": {
        "biobricks-mesh": {
            "description": "Full MeSH vocabulary",
        },
        "biohealth": {
            "description": "MeSH terms for diseases and concepts",
        },
    },
    "ChEBI": {
        "spoke-okn": {
            "description": "ChEBI chemical ontology identifiers",
        },
        "biobricks-aopwiki": {
            "description": "ChEBI identifiers for chemical stressors",
        },
    },
    "UBERON": {
        "spoke-genelab": {
            "description": "UBERON anatomy ontology for tissue types",
        },
        "gene-expression-atlas-okn": {
            "description": "UBERON anatomy ontology for tissue types",
        },
    },
    "NAICS": {
        "fiokg": {
            "description": "NAICS industry classification codes",
        },
        "sudokn": {
            "description": "NAICS codes for manufacturer classification",
        },
    },
}

# Gene bridge graph: gene-expression-atlas-okn stores both NCBI and Ensembl
GENE_BRIDGE_GRAPH = "gene-expression-atlas-okn"


def find_common_identifiers(graph_a: str, graph_b: str) -> List[str]:
    """Find identifier types shared between two graphs."""
    common = []
    for id_type, graphs in IDENTIFIER_BRIDGES.items():
        if graph_a in graphs and graph_b in graphs:
            common.append(id_type)
    return common


def get_graphs_for_identifier(id_type: str) -> List[str]:
    """Get list of graphs that support a given identifier type."""
    bridge = IDENTIFIER_BRIDGES.get(id_type, {})
    return list(bridge.keys())


def suggest_join_strategy(graph_a: str, graph_b: str) -> Dict[str, Any]:
    """Suggest how to join results from two graphs."""
    common = find_common_identifiers(graph_a, graph_b)

    if not common:
        # Check if gene bridge is possible
        gene_graphs = set()
        for id_type in ["NCBI_Gene", "Ensembl", "GeneSymbol"]:
            for g in get_graphs_for_identifier(id_type):
                if g in (graph_a, graph_b):
                    gene_graphs.add(g)

        if len(gene_graphs) == 2:
            # Both graphs have some gene identifier, check if bridge is possible
            a_gene_ids = [
                id_type for id_type in ["NCBI_Gene", "Ensembl", "GeneSymbol"]
                if graph_a in IDENTIFIER_BRIDGES.get(id_type, {})
            ]
            b_gene_ids = [
                id_type for id_type in ["NCBI_Gene", "Ensembl", "GeneSymbol"]
                if graph_b in IDENTIFIER_BRIDGES.get(id_type, {})
            ]
            if a_gene_ids and b_gene_ids and not set(a_gene_ids) & set(b_gene_ids):
                return {
                    "can_join": True,
                    "common_identifiers": [],
                    "strategy": (
                        f"No direct shared identifiers, but gene bridge possible via "
                        f"{GENE_BRIDGE_GRAPH}. {graph_a} uses {a_gene_ids} and "
                        f"{graph_b} uses {b_gene_ids}. The bridge graph stores both "
                        f"NCBI Gene IDs and Ensembl IDs."
                    ),
                    "bridge_graph": GENE_BRIDGE_GRAPH,
                    "source_id_types": a_gene_ids,
                    "target_id_types": b_gene_ids,
                }

        return {
            "can_join": False,
            "common_identifiers": [],
            "strategy": f"No shared identifier namespaces found between {graph_a} and {graph_b}.",
        }

    strategies = []
    for id_type in common:
        a_info = IDENTIFIER_BRIDGES[id_type].get(graph_a, {})
        b_info = IDENTIFIER_BRIDGES[id_type].get(graph_b, {})
        strategies.append(
            f"Join on {id_type}: {graph_a} ({a_info.get('description', '')}) ↔ "
            f"{graph_b} ({b_info.get('description', '')})"
        )

    return {
        "can_join": True,
        "common_identifiers": common,
        "strategy": "; ".join(strategies),
    }


def build_gene_lookup_query(graph_name: str, gene_symbol_or_id: str) -> Optional[str]:
    """Build a SPARQL query to find a gene in a specific graph.

    Adapts the query to the graph's schema (Ensembl, NCBI Gene ID, or gene symbol).
    """
    gene_input = gene_symbol_or_id.strip()

    if graph_name == "spoke-okn":
        # spoke-okn uses Ensembl IDs as node property
        return f"""
PREFIX spoke: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?gene ?ensembl ?label
WHERE {{
  ?gene a biolink:Gene .
  ?gene spoke:ensembl ?ensembl .
  OPTIONAL {{ ?gene rdfs:label ?label }}
  FILTER(
    STR(?ensembl) = "{gene_input}" ||
    CONTAINS(LCASE(STR(?label)), LCASE("{gene_input}"))
  )
}}
LIMIT 10
"""
    elif graph_name == "spoke-genelab":
        # spoke-genelab uses NCBI Gene (Entrez) IDs and gene symbols
        return f"""
PREFIX sglab: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?gene ?symbol ?organism
WHERE {{
  ?gene a biolink:Gene .
  OPTIONAL {{ ?gene sglab:symbol ?symbol }}
  OPTIONAL {{ ?gene sglab:organism ?organism }}
  FILTER(
    STR(?symbol) = "{gene_input}" ||
    CONTAINS(STR(?gene), "{gene_input}")
  )
}}
LIMIT 10
"""
    elif graph_name == "gene-expression-atlas-okn":
        # gene-expression-atlas-okn has both NCBI Gene ID and Ensembl ID
        return f"""
PREFIX glab: <https://spoke.ucsf.edu/genelab/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?gene ?ncbi_gene_id ?ensembl_id ?symbol ?name
WHERE {{
  ?gene a biolink:Gene .
  OPTIONAL {{ ?gene glab:ncbi_gene_id ?ncbi_gene_id }}
  OPTIONAL {{ ?gene glab:ensembl_id ?ensembl_id }}
  OPTIONAL {{ ?gene biolink:symbol ?symbol }}
  OPTIONAL {{ ?gene biolink:name ?name }}
  FILTER(
    STR(?symbol) = "{gene_input}" ||
    STR(?ncbi_gene_id) = "{gene_input}" ||
    STR(?ensembl_id) = "{gene_input}" ||
    CONTAINS(STR(?gene), "{gene_input}")
  )
}}
LIMIT 10
"""
    elif graph_name == "biobricks-ice":
        # biobricks-ice uses Entrez Gene IDs for assay targets
        return f"""
PREFIX ice: <https://ice.ntp.niehs.nih.gov/property/>
SELECT ?assay ?gene_id
WHERE {{
  ?assay ice:assay_entrez_gene_id ?gene_id .
  FILTER(STR(?gene_id) = "{gene_input}")
}}
LIMIT 10
"""
    return None


def build_gene_bridge_query(
    source_graph: str,
    target_graph: str,
    gene_ids: List[str],
) -> Optional[str]:
    """Build a SPARQL query to bridge gene identifiers between graphs.

    Uses gene-expression-atlas-okn as a bridge since it stores both NCBI Gene IDs
    and Ensembl IDs for the same gene.
    """
    if not gene_ids:
        return None

    # Determine what ID types source and target use
    source_id_types = [
        id_type for id_type in ["NCBI_Gene", "Ensembl", "GeneSymbol"]
        if source_graph in IDENTIFIER_BRIDGES.get(id_type, {})
    ]
    target_id_types = [
        id_type for id_type in ["NCBI_Gene", "Ensembl", "GeneSymbol"]
        if target_graph in IDENTIFIER_BRIDGES.get(id_type, {})
    ]

    if not source_id_types or not target_id_types:
        return None

    # Build VALUES clause for input IDs
    values_str = " ".join(f'"{gid}"' for gid in gene_ids)

    # Build the bridge query through gene-expression-atlas-okn
    source_type = source_id_types[0]
    target_type = target_id_types[0]

    # Map ID types to bridge graph properties
    property_map = {
        "NCBI_Gene": ("glab:ncbi_gene_id", "?ncbi_gene_id"),
        "Ensembl": ("glab:ensembl_id", "?ensembl_id"),
        "GeneSymbol": ("biolink:symbol", "?symbol"),
    }

    if source_type not in property_map or target_type not in property_map:
        return None

    src_prop, src_var = property_map[source_type]
    tgt_prop, tgt_var = property_map[target_type]

    return f"""
PREFIX glab: <https://spoke.ucsf.edu/genelab/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?gene {src_var} {tgt_var} ?name
WHERE {{
  VALUES {src_var} {{ {values_str} }}
  ?gene a biolink:Gene .
  ?gene {src_prop} {src_var} .
  ?gene {tgt_prop} {tgt_var} .
  OPTIONAL {{ ?gene biolink:name ?name }}
}}
"""
