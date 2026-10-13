"""Tests for entities CSVs that list one URI on several rows.

A property is listed once per class it sits on, and a URI can be both a class
and a predicate.  The schema must keep every row instead of only the last one.
"""

from unittest.mock import MagicMock, patch

from mcp_proto_okn.server import SPARQLServer


# Minimal CSV that reproduces the bug: organism sits on both Gene and Study.
# Before the fix, only Study (the last one processed) was reported.
SHARED_NODE_PROPS_CSV = """\
URI,Label,Description,Type,EdgePropertyOf,SourceClass,TargetClass
https://ex.org/schema/Gene,Gene,A gene,Class,,,
https://ex.org/schema/Study,Study,A study,Class,,,
https://ex.org/schema/organism,organism,Organism of the gene (string),NodeProperty,,Gene,
https://ex.org/schema/organism,organism,Organism of the study (string),NodeProperty,,Study,
https://ex.org/schema/symbol,symbol,Gene symbol (string),NodeProperty,,Gene,
"""

# NIEM-style graph: Judge is a class and also the predicate that points at a
# judge, and the predicates sit on more than one class.
SHARED_PREDICATES_CSV = """\
URI,Label,Description,Type,EdgePropertyOf,SourceClass,TargetClass
https://ex.org/schema/Case,Case,A case,Class,,,
https://ex.org/schema/Judge,Judge,A judge,Class,,,
https://ex.org/schema/Party,Party,A party,Class,,,
https://ex.org/schema/Judge,judge,Judge of the case,Predicate,,Case,Judge
https://ex.org/schema/Judge,judge,Judge of the case,Predicate,,Party,Judge
https://ex.org/schema/name,name,Name,Predicate,,Judge,
https://ex.org/schema/name,name,Name,Predicate,,Party,
"""


def _mock_urlopen(csv_text):
    """Return a context-manager mock that yields csv_text from urlopen."""
    mock_response = MagicMock()
    mock_response.read.return_value = csv_text.encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = lambda s, *a: None
    return mock_response


def _schema_block(mock_urlopen, csv_text, block_name):
    mock_urlopen.return_value = _mock_urlopen(csv_text)

    server = SPARQLServer(endpoint_url="http://localhost/sparql")
    server.registry_url = "http://example.org"
    server.kg_name = "test-kg"
    block = server.query_schema()[block_name]
    return [dict(zip(block["columns"], row)) for row in block["data"]]


def _node_properties(mock_urlopen):
    return _schema_block(mock_urlopen, SHARED_NODE_PROPS_CSV, "node_properties")


class TestSharedNodeProperties:
    """A node property on several classes is listed once per class."""

    @patch("mcp_proto_okn.server.urlopen")
    def test_duplicate_uri_keeps_every_class(self, mock_urlopen):
        props = _node_properties(mock_urlopen)

        classes = [p["class"] for p in props if p["label"] == "organism"]
        assert classes == ["Gene", "Study"]

    @patch("mcp_proto_okn.server.urlopen")
    def test_each_class_keeps_its_own_description(self, mock_urlopen):
        props = _node_properties(mock_urlopen)

        descriptions = {p["class"]: p["description"] for p in props if p["label"] == "organism"}
        assert descriptions == {
            "Gene": "Organism of the gene (string)",
            "Study": "Organism of the study (string)",
        }

    @patch("mcp_proto_okn.server.urlopen")
    def test_unique_node_property_unchanged(self, mock_urlopen):
        props = _node_properties(mock_urlopen)

        assert [p["class"] for p in props if p["label"] == "symbol"] == ["Gene"]
        assert len(props) == 3


class TestSharedPredicates:
    """A predicate on several classes is listed once per class."""

    @patch("mcp_proto_okn.server.urlopen")
    def test_duplicate_uri_keeps_every_source_class(self, mock_urlopen):
        preds = _schema_block(mock_urlopen, SHARED_PREDICATES_CSV, "predicates")

        pairs = [(p["source_class"], p["target_class"]) for p in preds if p["label"] == "judge"]
        assert pairs == [("Case", "Judge"), ("Party", "Judge")]
        assert [p["source_class"] for p in preds if p["label"] == "name"] == ["Judge", "Party"]

    @patch("mcp_proto_okn.server.urlopen")
    def test_uri_that_is_class_and_predicate_keeps_both(self, mock_urlopen):
        classes = _schema_block(mock_urlopen, SHARED_PREDICATES_CSV, "classes")

        assert [c["label"] for c in classes] == ["Case", "Judge", "Party"]
