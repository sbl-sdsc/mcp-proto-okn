"""Tests for node property parsing.

When the same node property URI appears in multiple CSV rows (one per class
it sits on), the schema must list it once per class instead of keeping only
the last row.
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


def _mock_urlopen(csv_text):
    """Return a context-manager mock that yields csv_text from urlopen."""
    mock_response = MagicMock()
    mock_response.read.return_value = csv_text.encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = lambda s, *a: None
    return mock_response


def _node_properties(mock_urlopen):
    mock_urlopen.return_value = _mock_urlopen(SHARED_NODE_PROPS_CSV)

    server = SPARQLServer(endpoint_url="http://localhost/sparql")
    server.registry_url = "http://example.org"
    server.kg_name = "test-kg"
    block = server.query_schema()["node_properties"]
    return [dict(zip(block["columns"], row)) for row in block["data"]]


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
