"""Unit tests for identifier mapping (no network required)."""

import pytest
from mcp_proto_okn.identifier_mapping import (
    IDENTIFIER_BRIDGES,
    find_common_identifiers,
    get_graphs_for_identifier,
    suggest_join_strategy,
    build_gene_lookup_query,
    build_gene_bridge_query,
)


def test_find_common_cas():
    """biobricks-tox21 and biobricks-ice share CAS."""
    common = find_common_identifiers("biobricks-tox21", "biobricks-ice")
    assert "CAS" in common


def test_find_common_none():
    """dreamkg and scales share nothing."""
    common = find_common_identifiers("dreamkg", "scales")
    assert len(common) == 0


def test_get_graphs_for_identifier_cas():
    """CAS found in multiple graphs."""
    graphs = get_graphs_for_identifier("CAS")
    assert "biobricks-tox21" in graphs
    assert "biobricks-ice" in graphs
    assert "sawgraph" in graphs
    assert len(graphs) >= 4


def test_get_graphs_for_identifier_unknown():
    """Unknown identifier type returns empty list."""
    graphs = get_graphs_for_identifier("UNKNOWN_ID_TYPE")
    assert len(graphs) == 0


def test_suggest_join_joinable():
    """Returns strategy with common identifiers."""
    result = suggest_join_strategy("biobricks-tox21", "biobricks-ice")
    assert result["can_join"] is True
    assert "CAS" in result["common_identifiers"]
    assert len(result["strategy"]) > 0


def test_suggest_join_not_joinable():
    """Returns can_join: false when no shared identifiers."""
    result = suggest_join_strategy("dreamkg", "scales")
    assert result["can_join"] is False
    assert len(result["common_identifiers"]) == 0


def test_gene_bridges_ncbi_to_ensembl():
    """spoke-genelab (NCBI) and spoke-okn (Ensembl) can join via bridge."""
    result = suggest_join_strategy("spoke-genelab", "spoke-okn")
    assert result["can_join"] is True
    # They might have direct overlap or need bridge
    if not result["common_identifiers"]:
        assert "bridge_graph" in result
        assert result["bridge_graph"] == "gene-expression-atlas-okn"


def test_gene_bridges_symbol():
    """spoke-genelab and gene-expression-atlas-okn share GeneSymbol."""
    common = find_common_identifiers("spoke-genelab", "gene-expression-atlas-okn")
    assert "GeneSymbol" in common


def test_gene_bridges_ncbi():
    """spoke-genelab and gene-expression-atlas-okn share NCBI_Gene."""
    common = find_common_identifiers("spoke-genelab", "gene-expression-atlas-okn")
    assert "NCBI_Gene" in common


def test_build_gene_lookup_query_spoke_okn():
    """Generates SPARQL using ensembl property for spoke-okn."""
    query = build_gene_lookup_query("spoke-okn", "FOS")
    assert query is not None
    assert "ensembl" in query
    assert "FOS" in query


def test_build_gene_lookup_query_spoke_genelab():
    """Generates SPARQL using symbol property for spoke-genelab."""
    query = build_gene_lookup_query("spoke-genelab", "Fos")
    assert query is not None
    assert "symbol" in query
    assert "Fos" in query


def test_build_gene_lookup_query_gene_expression_atlas():
    """Generates SPARQL with both NCBI and Ensembl for gene-expression-atlas-okn."""
    query = build_gene_lookup_query("gene-expression-atlas-okn", "BRCA1")
    assert query is not None
    assert "ncbi_gene_id" in query
    assert "ensembl_id" in query
    assert "BRCA1" in query


def test_build_gene_lookup_query_biobricks_ice():
    """Generates SPARQL for biobricks-ice Entrez gene lookup."""
    query = build_gene_lookup_query("biobricks-ice", "672")
    assert query is not None
    assert "entrez_gene_id" in query


def test_build_gene_lookup_query_unknown_graph():
    """Returns None for unsupported graph."""
    query = build_gene_lookup_query("dreamkg", "BRCA1")
    assert query is None


def test_build_gene_bridge_query():
    """Generates bridge query via gene-expression-atlas-okn."""
    query = build_gene_bridge_query(
        "spoke-genelab",
        "spoke-okn",
        ["14281", "2353"],
    )
    assert query is not None
    assert "14281" in query
    assert "2353" in query


def test_build_gene_bridge_query_empty_ids():
    """Returns None when no gene IDs provided."""
    query = build_gene_bridge_query("spoke-genelab", "spoke-okn", [])
    assert query is None


def test_identifier_bridges_structure():
    """IDENTIFIER_BRIDGES has expected structure."""
    assert "CAS" in IDENTIFIER_BRIDGES
    assert "Ensembl" in IDENTIFIER_BRIDGES
    assert "NCBI_Gene" in IDENTIFIER_BRIDGES
    assert "MONDO" in IDENTIFIER_BRIDGES
    assert "FIPS" in IDENTIFIER_BRIDGES

    # Each entry should have description
    for id_type, graphs in IDENTIFIER_BRIDGES.items():
        for graph_name, info in graphs.items():
            assert "description" in info, f"Missing description for {id_type}/{graph_name}"
