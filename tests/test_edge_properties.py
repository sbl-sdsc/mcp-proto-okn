"""Tests for edge property parsing — verifies fix for GitHub issue #8.

When the same edge property URI appears in multiple CSV rows (belonging to
different parent predicates), _get_entity_metadata must accumulate all
EdgePropertyOf values so that every predicate gets its edge properties.
"""

import csv
import os
from io import StringIO
from unittest.mock import patch

import pytest

from mcp_proto_okn.server import SPARQLServer


# Minimal CSV that reproduces the bug: adj_p_value and log2fc belong to
# both EXPRESSION and ABUNDANCE predicates.  Before the fix, only
# ABUNDANCE (the last one processed) would end up with those properties.
SHARED_EDGE_PROPS_CSV = """\
URI,Label,Description,Type,EdgePropertyOf,SourceClass,TargetClass
https://ex.org/schema/Assay,Assay,An assay,Class,,,
https://ex.org/schema/Gene,Gene,A gene,Class,,,
https://ex.org/schema/Organism,Organism,An organism,Class,,,
https://ex.org/schema/EXPRESSION,EXPRESSION,Expression predicate,Predicate,,Assay,Gene
https://ex.org/schema/ABUNDANCE,ABUNDANCE,Abundance predicate,Predicate,,Assay,Organism
https://ex.org/schema/adj_p_value,adj_p_value,Adjusted p-value (float),EdgeProperty,EXPRESSION,,
https://ex.org/schema/log2fc,log2fc,Log2 fold change (float),EdgeProperty,EXPRESSION,,
https://ex.org/schema/adj_p_value,adj_p_value,Adjusted p-value (float),EdgeProperty,ABUNDANCE,,
https://ex.org/schema/log2fc,log2fc,Log2 fold change (float),EdgeProperty,ABUNDANCE,,
https://ex.org/schema/lnfc,lnfc,Natural log fold change (float),EdgeProperty,ABUNDANCE,,
"""


def _mock_urlopen(csv_text):
    """Return a context-manager mock that yields csv_text from urlopen."""
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.read.return_value = csv_text.encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = lambda s, *a: None
    return mock_response


class TestGetEntityMetadata:
    """Unit tests for _get_entity_metadata duplicate-URI handling."""

    @patch("mcp_proto_okn.server.urlopen")
    def test_duplicate_uri_accumulates_edge_property_of(self, mock_urlopen):
        """When the same URI appears for different predicates, all parents are kept."""
        mock_urlopen.return_value = _mock_urlopen(SHARED_EDGE_PROPS_CSV)

        server = SPARQLServer(endpoint_url="http://localhost/sparql")
        server.registry_url = "http://example.org"
        server.kg_name = "test-kg"
        metadata = server._get_entity_metadata()

        adj = metadata["https://ex.org/schema/adj_p_value"]
        parents = {p.strip() for p in adj["edge_property_of"].split(";")}
        assert parents == {"EXPRESSION", "ABUNDANCE"}

    @patch("mcp_proto_okn.server.urlopen")
    def test_unique_edge_property_unchanged(self, mock_urlopen):
        """Edge properties that belong to only one predicate still work."""
        mock_urlopen.return_value = _mock_urlopen(SHARED_EDGE_PROPS_CSV)

        server = SPARQLServer(endpoint_url="http://localhost/sparql")
        server.registry_url = "http://example.org"
        server.kg_name = "test-kg"
        metadata = server._get_entity_metadata()

        lnfc = metadata["https://ex.org/schema/lnfc"]
        assert lnfc["edge_property_of"] == "ABUNDANCE"


class TestEdgePropertyJoin:
    """Integration-level tests: the full query_schema pipeline correctly
    assigns edge properties to ALL parent predicates."""

    @patch("mcp_proto_okn.server.urlopen")
    def test_all_predicates_have_edge_properties(self, mock_urlopen):
        """Both EXPRESSION and ABUNDANCE must have has_edge_properties=True
        and both must appear in the edge_properties output block."""
        mock_urlopen.return_value = _mock_urlopen(SHARED_EDGE_PROPS_CSV)

        server = SPARQLServer(endpoint_url="http://localhost/sparql")
        server.registry_url = "http://example.org"
        server.kg_name = "test-kg"
        result = server.query_schema()

        # Extract predicates as dicts keyed by label
        pred_cols = result["predicates"]["columns"]
        preds = {}
        for row in result["predicates"]["data"]:
            d = dict(zip(pred_cols, row))
            preds[d["label"]] = d

        assert preds["EXPRESSION"]["has_edge_properties"] is True, (
            "EXPRESSION should have edge properties"
        )
        assert preds["ABUNDANCE"]["has_edge_properties"] is True, (
            "ABUNDANCE should have edge properties"
        )

        # Both predicates must appear in the edge_properties block
        edge_props = result["edge_properties"]
        assert "EXPRESSION" in edge_props
        assert "ABUNDANCE" in edge_props

        # EXPRESSION should have adj_p_value and log2fc
        expr_labels = {p["label"] for p in edge_props["EXPRESSION"]["properties"]}
        assert "adj_p_value" in expr_labels
        assert "log2fc" in expr_labels

        # ABUNDANCE should have adj_p_value, log2fc, and lnfc
        abund_labels = {p["label"] for p in edge_props["ABUNDANCE"]["properties"]}
        assert "adj_p_value" in abund_labels
        assert "log2fc" in abund_labels
        assert "lnfc" in abund_labels

    @patch("mcp_proto_okn.server.urlopen")
    def test_real_spoke_genelab_csv(self, mock_urlopen):
        """Test with the actual spoke-genelab_entities.csv file to confirm
        MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG gets its edge properties."""
        csv_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "metadata",
            "entities",
            "spoke-genelab_entities.csv",
        )
        if not os.path.exists(csv_path):
            pytest.skip("spoke-genelab_entities.csv not found")

        with open(csv_path, "r") as f:
            content = f.read()

        mock_urlopen.return_value = _mock_urlopen(content)

        server = SPARQLServer(endpoint_url="http://localhost/sparql")
        server.registry_url = "http://example.org"
        server.kg_name = "spoke-genelab"
        result = server.query_schema()

        # Extract predicates
        pred_cols = result["predicates"]["columns"]
        preds = {}
        for row in result["predicates"]["data"]:
            d = dict(zip(pred_cols, row))
            preds[d["label"]] = d

        # The bug: this was False before the fix
        assert preds["MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG"]["has_edge_properties"] is True

        edge_props = result["edge_properties"]
        assert "MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG" in edge_props

        expr_labels = {
            p["label"]
            for p in edge_props["MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG"]["properties"]
        }
        expected = {"adj_p_value", "group_mean_1", "group_mean_2",
                    "group_stdev_1", "group_stdev_2", "log2fc"}
        assert expected == expr_labels

        # Other predicates should still work too
        assert preds["MEASURED_DIFFERENTIAL_ABUNDANCE_ASmO"]["has_edge_properties"] is True
        assert preds["MEASURED_DIFFERENTIAL_METHYLATION_ASmMR"]["has_edge_properties"] is True
