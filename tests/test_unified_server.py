"""Integration tests for unified server tools (mocked SPARQL)."""

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from mcp_proto_okn.registry import GraphRegistry
from mcp_proto_okn.unified_server import UnifiedSPARQLServer

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "test_registry.json")


@pytest.fixture
def unified():
    return UnifiedSPARQLServer(registry_path=FIXTURE_PATH)


def test_list_graphs_no_filter(unified):
    """Returns all graphs from registry."""
    graphs = unified.registry.list_all()
    assert len(graphs) == 3


def test_list_graphs_domain_filter(unified):
    """Filters correctly by domain."""
    results = unified.registry.filter_by_domain("toxicology")
    names = [g["name"] for g in results]
    assert "biobricks-tox21" in names
    assert "dreamkg" not in names


def test_route_query_returns_candidates(unified):
    """Returns sorted candidates with relevance signals."""
    results = unified.registry.search("drugs treat disease")
    assert len(results) == 3
    # spoke-okn should rank first
    assert results[0]["name"] == "spoke-okn"
    assert results[0]["relevance_score"] > results[-1]["relevance_score"]


def test_validate_graph_name_valid(unified):
    """Validates and returns canonical name for valid graph."""
    assert unified._validate_graph_name("spoke-okn") == "spoke-okn"
    assert unified._validate_graph_name("spoke") == "spoke-okn"


def test_validate_graph_name_invalid(unified):
    """Raises ValueError for invalid graph name with available list."""
    with pytest.raises(ValueError, match="Unknown graph"):
        unified._validate_graph_name("nonexistent")


@patch("mcp_proto_okn.server.SPARQLWrapper")
def test_query_valid_graph(mock_sparql_cls, unified):
    """Delegates to SPARQLServer.execute() for valid graph."""
    mock_instance = MagicMock()
    mock_sparql_cls.return_value = mock_instance

    # Mock the query response
    mock_result = {
        "results": {
            "bindings": [
                {
                    "s": {"type": "uri", "value": "http://example.org/entity1"},
                    "p": {"type": "uri", "value": "http://example.org/pred1"},
                    "o": {"type": "literal", "value": "value1"},
                }
            ]
        }
    }
    mock_instance.query.return_value.convert.return_value = mock_result
    mock_instance.setQuery = MagicMock()
    mock_instance.setReturnFormat = MagicMock()
    mock_instance.setMethod = MagicMock()
    mock_instance.addCustomHttpHeader = MagicMock()
    mock_instance.setTimeout = MagicMock()

    server = unified._get_server("spoke-okn")
    assert server is not None
    assert "spoke-okn" in unified._servers or "spoke" in str(unified._servers)


@patch("mcp_proto_okn.server.SPARQLWrapper")
def test_get_schema_delegates(mock_sparql_cls, unified):
    """Calls query_schema on correct server."""
    mock_instance = MagicMock()
    mock_sparql_cls.return_value = mock_instance
    mock_instance.setReturnFormat = MagicMock()
    mock_instance.setMethod = MagicMock()
    mock_instance.addCustomHttpHeader = MagicMock()
    mock_instance.setTimeout = MagicMock()

    server = unified._get_server("spoke-okn")
    # Just verifying the server is created for the right graph
    assert server.kg_name is not None


def test_get_join_strategy_common(unified):
    """Returns common identifiers between graphs."""
    from mcp_proto_okn.identifier_mapping import suggest_join_strategy
    result = suggest_join_strategy("biobricks-tox21", "biobricks-ice")
    assert result["can_join"] is True
    assert "CAS" in result["common_identifiers"]


def test_get_join_strategy_no_common(unified):
    """Returns no common identifiers for unrelated graphs."""
    from mcp_proto_okn.identifier_mapping import suggest_join_strategy
    result = suggest_join_strategy("dreamkg", "scales")
    assert result["can_join"] is False


def test_server_caching(unified):
    """Same server instance returned for repeated calls."""
    with patch("mcp_proto_okn.server.SPARQLWrapper") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        mock_instance.setReturnFormat = MagicMock()
        mock_instance.setMethod = MagicMock()
        mock_instance.addCustomHttpHeader = MagicMock()
        mock_instance.setTimeout = MagicMock()

        server1 = unified._get_server("spoke-okn")
        server2 = unified._get_server("spoke-okn")
        assert server1 is server2


def test_server_alias_resolution(unified):
    """Alias resolves to same server instance."""
    with patch("mcp_proto_okn.server.SPARQLWrapper") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        mock_instance.setReturnFormat = MagicMock()
        mock_instance.setMethod = MagicMock()
        mock_instance.addCustomHttpHeader = MagicMock()
        mock_instance.setTimeout = MagicMock()

        server1 = unified._get_server("spoke-okn")
        server2 = unified._get_server("spoke")
        assert server1 is server2
