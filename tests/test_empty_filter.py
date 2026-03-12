"""Tests for QueryAnalyzer.remove_empty_filters."""

import pytest

from mcp_proto_okn.server import QueryAnalyzer


QUERY_WITH_EMPTY_FILTER = """\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?diseaseLabel ?drugLabel ?cooccur ?enrichment
WHERE {
  ?sdohStmt rdf:subject ?sdoh ;
            rdf:predicate schema:ASSOCIATES_SaD ;
            rdf:object ?disease ;
            schema:cooccur ?cooccur ;
            schema:enrichment ?enrichment .
  ?treatStmt rdf:subject ?drug ;
             rdf:predicate schema:TREATS_CtD ;
             rdf:object ?disease .
  ?sdoh rdfs:label ?sdohLabel .
  FILTER(LCASE(STR(?sdohLabel)) IN ())
  ?disease rdfs:label ?diseaseLabel .
  ?drug rdfs:label ?drugLabel .
}
ORDER BY DESC(?enrichment)
"""


def test_removes_lcase_str_empty_filter():
    cleaned, removed = QueryAnalyzer.remove_empty_filters(QUERY_WITH_EMPTY_FILTER)
    assert len(removed) == 1
    assert "IN ()" not in cleaned
    # The rest of the query should be intact
    assert "?disease rdfs:label ?diseaseLabel" in cleaned
    assert "ORDER BY DESC(?enrichment)" in cleaned


def test_removes_plain_empty_filter():
    query = "SELECT ?x WHERE { ?x a ?type . FILTER(?type IN ()) }"
    cleaned, removed = QueryAnalyzer.remove_empty_filters(query)
    assert len(removed) == 1
    assert "FILTER" not in cleaned


def test_removes_str_only_empty_filter():
    query = "SELECT ?x WHERE { ?x rdfs:label ?name . FILTER(STR(?name) IN ()) }"
    cleaned, removed = QueryAnalyzer.remove_empty_filters(query)
    assert len(removed) == 1
    assert "FILTER" not in cleaned


def test_preserves_nonempty_filter():
    query = 'SELECT ?x WHERE { ?x rdfs:label ?name . FILTER(?name IN ("foo", "bar")) }'
    cleaned, removed = QueryAnalyzer.remove_empty_filters(query)
    assert len(removed) == 0
    assert cleaned == query


def test_removes_multiple_empty_filters():
    query = (
        "SELECT ?x ?y WHERE { "
        "?x rdfs:label ?a . FILTER(?a IN ()) "
        "?y rdfs:label ?b . FILTER(LCASE(?b) IN ()) "
        "}"
    )
    cleaned, removed = QueryAnalyzer.remove_empty_filters(query)
    assert len(removed) == 2
    assert "FILTER" not in cleaned


def test_case_insensitive():
    query = "SELECT ?x WHERE { ?x a ?type . filter(?type in ()) }"
    cleaned, removed = QueryAnalyzer.remove_empty_filters(query)
    assert len(removed) == 1
    assert "filter" not in cleaned.lower() or "in ()" not in cleaned.lower()
