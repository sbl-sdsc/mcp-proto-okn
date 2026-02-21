"""Unit tests for GraphRegistry (no network required)."""

import os
import pytest
from mcp_proto_okn.registry import GraphRegistry, GraphInfo

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "test_registry.json")


@pytest.fixture
def registry():
    return GraphRegistry(FIXTURE_PATH)


def test_load_registry(registry):
    """Loads and populates all graphs from fixture."""
    assert len(registry.graph_names) == 3


def test_list_all(registry):
    """Returns all graphs with correct fields."""
    graphs = registry.list_all()
    assert len(graphs) == 3
    for g in graphs:
        assert "name" in g
        assert "display_name" in g
        assert "endpoint_url" in g
        assert "domain_tags" in g
        assert "entity_types" in g


def test_get_existing(registry):
    """Returns GraphInfo for a known graph."""
    graph = registry.get("spoke-okn")
    assert graph is not None
    assert isinstance(graph, GraphInfo)
    assert graph.name == "spoke-okn"
    assert graph.display_name == "SPOKE Open Knowledge Network"
    assert "Gene" in graph.entity_types["classes"]


def test_get_nonexistent(registry):
    """Returns None for unknown graph."""
    assert registry.get("nonexistent-graph") is None


def test_get_by_alias(registry):
    """Resolves alias to canonical name."""
    graph = registry.get("spoke")
    assert graph is not None
    assert graph.name == "spoke-okn"


def test_filter_by_domain(registry):
    """Filters by domain tag."""
    results = registry.filter_by_domain("biology")
    names = [g["name"] for g in results]
    assert "spoke-okn" in names
    assert "dreamkg" not in names


def test_filter_by_domain_case_insensitive(registry):
    """Domain filter is case-insensitive."""
    results = registry.filter_by_domain("BIOLOGY")
    names = [g["name"] for g in results]
    assert "spoke-okn" in names


def test_filter_by_entity_type(registry):
    """Filters by entity class name."""
    results = registry.filter_by_entity_type("Gene")
    names = [g["name"] for g in results]
    assert "spoke-okn" in names
    assert "dreamkg" not in names


def test_filter_by_entity_type_case_insensitive(registry):
    """Entity type filter is case-insensitive."""
    results = registry.filter_by_entity_type("gene")
    names = [g["name"] for g in results]
    assert "spoke-okn" in names


def test_search_relevance_ordering(registry):
    """Graphs with more relevance signals sort first."""
    results = registry.search("drugs treat disease")
    # spoke-okn should rank first (matches description, domain tags, entity types, examples)
    assert results[0]["name"] == "spoke-okn"
    assert results[0]["relevance_score"] > 0


def test_search_returns_all(registry):
    """All graphs returned, not just matches."""
    results = registry.search("drugs treat disease")
    assert len(results) == 3


def test_search_no_match(registry):
    """All graphs returned even with no keyword matches, all with score 0."""
    results = registry.search("xyzzy_totally_unrelated_query_12345")
    assert len(results) == 3
    assert all(r["relevance_score"] == 0 for r in results)


def test_resolve_name(registry):
    """Resolves canonical and alias names."""
    assert registry.resolve_name("spoke-okn") == "spoke-okn"
    assert registry.resolve_name("spoke") == "spoke-okn"
    assert registry.resolve_name("nonexistent") is None


def test_graph_names(registry):
    """Returns sorted list of all canonical names."""
    names = registry.graph_names
    assert names == ["biobricks-tox21", "dreamkg", "spoke-okn"]


def test_graph_info_to_dict(registry):
    """GraphInfo.to_dict() produces expected format."""
    graph = registry.get("spoke-okn")
    d = graph.to_dict()
    assert d["name"] == "spoke-okn"
    assert isinstance(d["domain_tags"], list)
    assert isinstance(d["entity_types"], dict)
    assert "aliases" not in d  # aliases not included in to_dict output
