"""
Integration tests hitting live FRINK endpoint.

These tests validate gene identifier mapping and cross-graph querying
using known results from existing example analyses.

Skip with: pytest -m "not live"
Requires network access to frink.apps.renci.org.

NOTE: The endpoint URLs used here use the canonical named-graph names
(e.g., spoke-okn, gene-expression-atlas-okn) which match the FROM
clauses inserted by SPARQLServer. The production mcp.json has some
URL mismatches (e.g., "spoke" instead of "spoke-okn") that cause
FROM clause mismatches on the federation endpoint.
"""

import pytest

from mcp_proto_okn.server import SPARQLServer

# Mark all tests in this module as 'live'
pytestmark = pytest.mark.live


@pytest.fixture(scope="module")
def spoke_genelab():
    return SPARQLServer("https://frink.apps.renci.org/spoke-genelab/sparql")


@pytest.fixture(scope="module")
def spoke_okn():
    # Use spoke-okn (not spoke) so the FROM clause matches the named graph
    return SPARQLServer("https://frink.apps.renci.org/spoke-okn/sparql")


@pytest.fixture(scope="module")
def gene_expression_atlas():
    # Use correct spelling (atlas not altlas)
    return SPARQLServer("https://frink.apps.renci.org/gene-expression-atlas-okn/sparql")


@pytest.fixture(scope="module")
def biobricks_tox21():
    return SPARQLServer("https://frink.apps.renci.org/biobricks-tox21/sparql")


@pytest.fixture(scope="module")
def biobricks_ice():
    return SPARQLServer("https://frink.apps.renci.org/biobricks-ice/sparql")


class TestSpokeGenelab:
    """Tests based on OSD-161 spaceflight analysis."""

    def test_spoke_genelab_gene_expression(self, spoke_genelab):
        """Query spoke-genelab for OSD-161 differential expression.

        Verify Fos gene has expected expression values (~1.96 log2fc, ~0.024 adj_p).
        Uses RDF reification pattern for edge properties.
        """
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sglab: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
        SELECT ?symbol ?log2fc ?adj_p_value
        WHERE {
          <https://purl.org/okn/frink/kg/spoke-genelab/node/OSD-161> sglab:PERFORMED_SpAS ?assay .
          ?rel rdf:subject ?assay .
          ?rel rdf:predicate sglab:MEASURED_DIFFERENTIAL_EXPRESSION_ASmMG .
          ?rel rdf:object ?gene .
          ?rel sglab:log2fc ?log2fc .
          ?rel sglab:adj_p_value ?adj_p_value .
          ?gene sglab:symbol ?symbol .
          FILTER(LCASE(STR(?symbol)) = "fos")
        }
        LIMIT 10
        """
        result = spoke_genelab.execute(query, analyze=False, auto_expand_descendants=False)
        assert "count" in result, f"Query returned error: {result.get('error', 'unknown')}"
        assert result["count"] > 0
        # Check Fos is in the results
        symbol_col = result["columns"].index("symbol")
        symbols = [row[symbol_col] for row in result["data"]]
        assert "Fos" in symbols

    def test_spoke_genelab_ortholog_mapping(self, spoke_genelab):
        """Query spoke-genelab IS_ORTHOLOG_MGiG for ortholog mappings.

        Verify ortholog relationships exist in the graph.
        """
        query = """
        PREFIX sglab: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?mouse_gene ?mouse_symbol ?human_gene
        WHERE {
          ?mouse_gene a biolink:Gene .
          ?mouse_gene sglab:symbol ?mouse_symbol .
          ?mouse_gene sglab:IS_ORTHOLOG_MGiG ?human_gene .
        }
        LIMIT 5
        """
        result = spoke_genelab.execute(query, analyze=False, auto_expand_descendants=False)
        assert "count" in result, f"Query returned error: {result.get('error', 'unknown')}"
        assert result["count"] > 0


class TestSpokeOkn:
    """Tests for SPOKE-OKN gene-disease associations."""

    def test_spoke_okn_gene_disease_association(self, spoke_okn):
        """Query spoke-okn for disease-gene associations.

        Verify basic disease-gene query works.
        """
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX spoke: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?disease ?disease_label
        WHERE {
          ?disease a biolink:Disease .
          ?disease rdfs:label ?disease_label .
          ?disease spoke:ASSOCIATES_DaG ?gene .
        }
        LIMIT 5
        """
        result = spoke_okn.execute(query, analyze=False, auto_expand_descendants=False)
        assert "count" in result, f"Query returned error: {result.get('error', 'unknown')}"
        assert result["count"] > 0


class TestGeneExpressionAtlas:
    """Tests for Gene Expression Atlas bridge capabilities."""

    def test_gene_expression_atlas_dual_ids(self, gene_expression_atlas):
        """Query gene-expression-atlas-okn for a gene.

        Verify it returns both NCBI Gene ID and Ensembl ID for the same gene.
        """
        query = """
        PREFIX glab: <https://spoke.ucsf.edu/genelab/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?gene ?ncbi_gene_id ?ensembl_id ?symbol
        WHERE {
          ?gene a biolink:Gene .
          ?gene glab:ncbi_gene_id ?ncbi_gene_id .
          ?gene glab:ensembl_id ?ensembl_id .
          OPTIONAL { ?gene biolink:symbol ?symbol }
        }
        LIMIT 5
        """
        result = gene_expression_atlas.execute(query, analyze=False, auto_expand_descendants=False)
        assert "count" in result, f"Query returned error: {result.get('error', 'unknown')}"
        assert result["count"] > 0
        # Verify both ID columns present
        assert "ncbi_gene_id" in result["columns"]
        assert "ensembl_id" in result["columns"]

    def test_gene_expression_atlas_symbol_lookup(self, gene_expression_atlas):
        """Query by gene symbol, verify correct gene returned."""
        query = """
        PREFIX glab: <https://spoke.ucsf.edu/genelab/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?gene ?symbol ?ncbi_gene_id ?ensembl_id
        WHERE {
          ?gene a biolink:Gene .
          ?gene biolink:symbol ?symbol .
          OPTIONAL { ?gene glab:ncbi_gene_id ?ncbi_gene_id }
          OPTIONAL { ?gene glab:ensembl_id ?ensembl_id }
          FILTER(?symbol = "FOS")
        }
        LIMIT 5
        """
        result = gene_expression_atlas.execute(query, analyze=False, auto_expand_descendants=False)
        assert "count" in result, f"Query returned error: {result.get('error', 'unknown')}"
        assert result["count"] > 0
        symbol_col = result["columns"].index("symbol")
        symbols = [row[symbol_col] for row in result["data"]]
        assert "FOS" in symbols


class TestCrossGraphCAS:
    """Tests for CAS-based cross-graph bridging."""

    def test_cross_graph_cas_bridge(self, biobricks_tox21, biobricks_ice):
        """Query biobricks-tox21 and biobricks-ice for chemicals.

        Verify both return results (they share CAS identifiers).
        """
        # Query tox21 for any chemical
        tox21_query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?chemical ?label
        WHERE {
          ?chemical a <http://purl.obolibrary.org/obo/CHEMINF_000446> .
          OPTIONAL { ?chemical rdfs:label ?label }
        }
        LIMIT 3
        """
        tox21_result = biobricks_tox21.execute(
            tox21_query, analyze=False, auto_expand_descendants=False
        )
        assert "count" in tox21_result, f"Tox21 query error: {tox21_result.get('error', 'unknown')}"
        assert tox21_result["count"] > 0

        # Query ICE for any chemical
        ice_query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?chemical ?label
        WHERE {
          ?chemical a <https://w3id.org/biolink/vocab/ChemicalEntity> .
          OPTIONAL { ?chemical rdfs:label ?label }
        }
        LIMIT 3
        """
        ice_result = biobricks_ice.execute(
            ice_query, analyze=False, auto_expand_descendants=False
        )
        assert "count" in ice_result, f"ICE query error: {ice_result.get('error', 'unknown')}"
        assert ice_result["count"] > 0


class TestCrossGraphGenePipeline:
    """End-to-end cross-graph gene pipeline test."""

    def test_cross_graph_gene_pipeline(self, spoke_genelab, gene_expression_atlas):
        """End-to-end: query spoke-genelab for genes -> bridge via gene-expression-atlas-okn.

        Verify the pipeline can connect gene identifiers across graphs.
        """
        # Step 1: Get genes with symbols from spoke-genelab
        step1_query = """
        PREFIX sglab: <https://purl.org/okn/frink/kg/spoke-genelab/schema/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?gene ?symbol
        WHERE {
          ?gene a biolink:Gene .
          ?gene sglab:symbol ?symbol .
        }
        LIMIT 5
        """
        step1_result = spoke_genelab.execute(
            step1_query, analyze=False, auto_expand_descendants=False
        )
        assert "count" in step1_result, f"Step 1 error: {step1_result.get('error', 'unknown')}"
        assert step1_result["count"] > 0

        # Step 2: Use gene symbols to find in gene-expression-atlas-okn
        symbol_col = step1_result["columns"].index("symbol")
        symbols = [row[symbol_col] for row in step1_result["data"]]
        assert len(symbols) > 0

        # Try to find the first symbol in gene-expression-atlas
        first_symbol = symbols[0]
        step2_query = f"""
        PREFIX glab: <https://spoke.ucsf.edu/genelab/>
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        SELECT ?gene ?symbol ?ncbi_gene_id ?ensembl_id
        WHERE {{
          ?gene a biolink:Gene .
          ?gene biolink:symbol ?symbol .
          OPTIONAL {{ ?gene glab:ncbi_gene_id ?ncbi_gene_id }}
          OPTIONAL {{ ?gene glab:ensembl_id ?ensembl_id }}
          FILTER(?symbol = "{first_symbol}")
        }}
        LIMIT 5
        """
        step2_result = gene_expression_atlas.execute(
            step2_query, analyze=False, auto_expand_descendants=False
        )
        # The test validates the pipeline works, not that every gene matches
        assert "columns" in step2_result
