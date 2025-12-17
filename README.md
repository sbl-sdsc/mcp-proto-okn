# MCP Proto-OKN Server

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://badge.fury.io/py/mcp-proto-okn.svg?cachebust=1)](https://badge.fury.io/py/mcp-proto-okn)

A Model Context Protocol (MCP) server providing seamless access to SPARQL endpoints with specialized support for the NSF-funded [Proto-OKN Project](https://www.proto-okn.net/) (Prototype Open Knowledge Network). This server enables querying the scientific knowledge graphs hosted on the [FRINK](https://frink.renci.org/) platform. In addition, third-party SPARQL endpoints can be queried.

## Features

- **🔗 FRINK Integration**: Automatic detection and documentation linking for FRINK-hosted knowledge graphs
- **🧬 Proto-OKN Ecosystem**: Optimized support for biomedical and scientific knowledge graphs, including:
  - **SPOKE** - Scalable Precision Medicine Open Knowledge Engine
  - **BioBricks ICE** - Chemical safety and cheminformatics data
  - **SAWGraph** - Safe Agricultural Products and Water monitoring
  - **Additional Proto-OKN knowledge graphs** - Expanding ecosystem of scientific data
- **⚙️ Flexible Configuration**: Support for both FRINK and custom SPARQL endpoints
- **📚 Automatic Documentation**: Registry links and metadata for Proto-OKN knowledge graphs
- **🔗 Federated Query**: Prompts can query multiple endpoints

## Architecture

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/mcp_architecture.png"
     alt="Tool Selector"
     width="600">

The MCP Server Proto-OKN acts as a bridge between AI assistants (like Claude) and SPARQL knowledge graphs, enabling natural language queries to be converted into structured SPARQL queries and executed against scientific databases.

## Prerequisites

Before installing the MCP Server Proto-OKN, ensure you have:

- **Operating System**: macOS, Linux, or Windows
- **Client Application**: One of the following:
  - Claude Desktop with Pro or Max subscription
  - VS Code Insiders with GitHub Copilot subscription

## Installation

[Installation instructions for Claude Desktop and VS Code Insiders](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/installation.md)

## Quick Start

Once configured, you can start querying knowledge graphs through natural language prompts in Claude Desktop or VS Code chat interface.

### Select and Configure MCP Tools

From the top menu bar:
```
1. Select: Claude->Settings->Connectors
2. Click: Configure for the MCP endpoints you want to use
3. Select Tool permissions: Always allow
```

In the prompt dialog box, click the `+` button:
```
1. Turn off Web search
2. Toggle MCP services on/off as needed
```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/select_mcp_server.png"
     alt="Tool Selector"
     width="500">

To create a transcript of a chat (see examples below), use the following prompt: 
```Create a chat transcript```. 
The transcript can then be downloaded in .md format.

### Example Queries

1. **Knowledge Graph Overview and Class Diagram (spoke-genelab, spoke-okn, biobricks-toxcast, sawgraph)**

   Use `@kg_name` to refer to a specific KG, e.g., `@spoke-genelab` in a chat. The examples below create an overview and a class diagram for each KG.

   [spoke-genelab chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_genelab_overview.md)

   [spoke-okn chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_okn_overview.md)

   [biobricks-toxcast chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/toxcast_overview.md)

   [sawgraph chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/sawgraph_overview.md)

   [scales chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/scales_overview.md)

   [sudokn chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/sudokn_overview.md)

   [ufokn chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/ufokn_overview.md)

2. **Spaceflight Gene Expression Analysis (spoke-genelab, spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_spaceflight_analysis.md)

3. **PFOA in Drinking Water (spoke-genelab)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_okn_pfoa_drinking_water.md)

4. **Disease Prevalence in the US (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/us_county_disease_prevalence.md)

5. **Disease Prevalence - Socio-Economic Factors Correlation (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/disease_socio_economic_correlation.md)

6. **Data about PFOA (spoke-okn, biobricks-toxcast)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/pfoa_data_spoke_okn_biobricks_toxcast.md)

7. **Biological Targets for PFOA (biobricks-toxcast)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks_toxcast_PFOA_targets.md)

8. **Criminal Justice Patterns (scales)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/scales_criminal_justice_analysis.md)

9. **Michigan Flooding Event (ufokn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/ufokn_michigan_flood.md)

10. **Chemical Identifiers (Proto-OKN KGs)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/chemical_identifiers.md)


### Building and Publishing (maintainers only)

```bash
# Increment version number (major|minor|patch)
uv version --bump minor

# Remove distributions for previous versions
rm -rf dist

# Build the package
uv build

# Publish to TestPyPI first (recommended)
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_PYPI_TOKEN_HERE

# Test the deployment
For testing, add the following parameters to the `args` option in the claude_desktop_config.json.
  "args": [
    "--index-url",
    "https://test.pypi.org/simple/",
    "--extra-index-url",
    "https://pypi.org/simple/",
    "mcp-proto-okn"
  ]

# Publish to PyPI (production release)
uv publish --token pypi-YOUR_PYPI_TOKEN_HERE

# Clear uv cache (optional, if there are problems)
uv cache clean

# Remove cached tool installation (optional, if problems persist)
rm -rf ~/.local/share/uv/tools/mcp-proto-okn
```

## API Reference

### Available Tools

#### `get_description`
Retrieves endpoint metadata and documentation.

**Parameters:**
- None

**Returns:**
- String containing either:
  - Registry page content prefixed with a header line identifying the registry source (for FRINK endpoints)
  - The static/server-provided description when no registry URL applies

#### `get_schema`
Retrieves the schema (classes, relationships, properties) for the knowledge graph endpoint.

> **Important:** Always call this tool FIRST before making any queries to understand what data is available in the knowledge graph.

**Parameters:**
- `compact` (boolean, optional): If `true` (default), returns compact URI:label mappings. If `false`, returns full metadata with descriptions.

**Returns:**
- JSON object containing the endpoint's schema information in the specified format, including:
  - Available classes
  - Relationships/predicates
  - Properties with labels and descriptions (when available)

#### `query`
Executes SPARQL queries against the configured endpoint.

> **Important:** You MUST call `get_schema()` first before using this query tool to understand the available classes and predicates in the knowledge graph.

**Parameters:**
- `query_string` (string, required): A valid SPARQL query string
- `format` (string, optional): Output format. Options:
  - `'compact'` (default): Columns + data arrays, no repeated keys
  - `'simplified'`: JSON with dict rows
  - `'full'`: Complete SPARQL JSON response
  - `'values'`: List of dictionaries
  - `'csv'`: CSV string format

**Returns:**
- Query results in the specified format

#### `clean_mermaid_diagram`
Cleans Mermaid class diagrams by removing unwanted elements.

**Parameters:**
- `mermaid_content` (string, required): The raw Mermaid class diagram content

**Returns:**
- Cleaned Mermaid content with the following elements removed:
  - All note statements that would render as unreadable yellow boxes
  - Empty curly braces from class definitions

---
### Command Line Interface

**Required Parameters:**
- `--endpoint` : SPARQL endpoint URL (e.g., `https://frink.apps.renci.org/spoke/sparql`)

**Optional Parameters:**
- `--description` : Custom description for the SPARQL endpoint (auto-generated for FRINK endpoints)

**Example Usage:**

```bash
uvx mcp-proto-okn --endpoint https://frink.apps.renci.org/spoke/sparql
```

## Troubleshooting

### Common Issues

**MCP server not appearing in Claude Desktop:**
- Ensure you've completely quit and restarted Claude Desktop (not just closed the window)
- Check that your JSON configuration is valid (use a JSON validator)
- Verify that `uvx` is installed and accessible in your PATH

**Connection errors:**
- Check your internet connection
- Verify the SPARQL endpoint URL is correct and accessible
- Some endpoints may have rate limits or temporary downtime

**Performance issues:**
- Complex SPARQL queries may take time to execute
- Consider breaking down complex queries into smaller parts
- Check the endpoint's documentation for query best practices

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Citation

If you use MCP Server Proto-OKN in your research, please cite the following works:

```bibtex
@software{rose2025mcp-proto-okn,
  title={MCP Server Proto-OKN},
  author={Rose, P.W. and Nelson, C.A. and Shi, Y. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/sbl-sdsc/mcp-proto-okn}
}

@software{rose2025spoke-genelab,
  title={NASA SPOKE-GeneLab Knowledge Graph},
  author={Rose, P.W. and Nelson, C.A. and Gebre, S.G. and Saravia-Butler AM, and Soman, K. and Grigorev, K.A. and Sanders, L.M. and Costes, S.V. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/BaranziniLab/spoke_genelab}
}
```

### Related Publications

- Nelson, C.A., Rose, P.W., Soman, K., Sanders, L.M., Gebre, S.G., Costes, S.V., Baranzini, S.E. (2025). "Nasa Genelab-Knowledge Graph Fabric Enables Deep Biomedical Analysis of Multi-Omics Datasets." *NASA Technical Reports*, 20250000723. [Link](https://ntrs.nasa.gov/citations/20250000723)

- Sanders, L., Costes, S., Soman, K., Rose, P., Nelson, C., Sawyer, A., Gebre, S., Baranzini, S. (2024). "Biomedical Knowledge Graph Capability for Space Biology Knowledge Gain." *45th COSPAR Scientific Assembly*, July 13-21, 2024. [Link](https://ui.adsabs.harvard.edu/abs/2024cosp...45.2183S/abstract)

## Acknowledgments

### Funding

This work is in part supported by:
- **National Science Foundation** Award [#2333819](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333819): "Proto-OKN Theme 1: Connecting Biomedical information on Earth and in Space via the SPOKE knowledge graph"

### Related Projects

- [Proto-OKN Project](https://www.proto-okn.net/) - Prototype Open Knowledge Network initiative
- [FRINK Platform](https://frink.renci.org/) - Knowledge graph hosting infrastructure  
- [Knowledge Graph Registry](https://frink.renci.org/registry/) - Catalog of available knowledge graphs
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI assistant integration standard
- [Original MCP Server SPARQL](https://github.com/ekzhu/mcp-server-sparql/) - Base implementation reference

---

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/sbl-sdsc/mcp-proto-okn).*
