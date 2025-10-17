# MCP Proto-OKN Server

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://badge.fury.io/py/mcp_proto_okn.svg)](https://badge.fury.io/py/mcp-proto-okn)

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

![MCP Architecture](https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/mcp_architecture.png)

The MCP Server Proto-OKN acts as a bridge between AI assistants (like Claude) and SPARQL knowledge graphs, enabling natural language queries to be converted into structured SPARQL queries and executed against scientific databases.

## Prerequisites

Before installing the MCP Server Proto-OKN, ensure you have:

- **Operating System**: macOS, Linux, or Windows
- **Client Application**: One of the following:
  - Claude Desktop with Pro or Max subscription
  - VS Code Insiders with GitHub Copilot subscription

## Installation

### Prerequisites

The MCP Proto-OKN server requires the `uv` package manager to be installed on your system. If you don't have it installed run:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> **Note**: Once `uv` is installed, the `uvx` command in the configuration below will automatically download and run the latest version from PyPI when needed.

### Claude Desktop Setup

**Recommended for most users**

1. **Download and Install Claude Desktop**

   Visit [https://claude.ai/download](https://claude.ai/download) and install Claude Desktop for your operating system.

   > **Requirements**: Claude Pro or Max subscription is required for MCP server functionality.

2. **Configure MCP Server**

   **Option A: Download Pre-configured File (Recommended)**

   Download the pre-configured `claude_desktop_config.json` file with FRINK endpoints from the repository and copy it to the appropriate location:

   **macOS**:
   ```bash
   # Download the config file
   curl -o /tmp/claude_desktop_config.json https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/config/claude_desktop_config.json
   
   # Copy to Claude Desktop configuration directory
   cp /tmp/claude_desktop_config.json "$HOME/Library/Application Support/Claude/"
   ```

   **Windows PowerShell**:
   ```powershell
   # Download the config file
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/config/claude_desktop_config.json" -OutFile "$env:TEMP\claude_desktop_config.json"
   
   # Copy to Claude Desktop configuration directory
   Copy-Item "$env:TEMP\claude_desktop_config.json" "$env:APPDATA\Claude\"
   ```

   **Option B: Manual Configuration**

   Alternatively, you can manually edit the configuration file in Claude Desktop. Navigate to `Claude->Settings->Developer->Edit Config`
   to edit it.

   Below is an example of how to configure FRINK endpoints. Third-party SPARQL endpoints with a custom description can be added (see uniprot-sparql example below).

   ```json
   {
     "mcpServers": {
       "spoke": {
         "command": "uvx",
         "args": [
           "mcp-proto-okn",
           "--endpoint",
           "https://frink.apps.renci.org/spoke/sparql"
         ]
       },
       "biobricks-ice": {
         "command": "uvx",
         "args": [
           "mcp-proto-okn",
           "--endpoint",
           "https://frink.apps.renci.org/biobricks-ice/sparql"
         ]
       },
       "uniprot": {
         "command": "uvx",
         "args": [
           "mcp-proto-okn",
           "--endpoint",
           "https://sparql.uniprot.org/sparql",
           "--description",
           "Resource for protein sequence and function information. For details: https://purl.uniprot.org/html/index-en.htm"
         ]
       }
     }
   }
   ```

   > **Important**: If you have existing MCP server configurations, do not use Option A as it will overwrite your existing configuration. Instead, use Option B and manually merge the Proto-OKN endpoints with your existing `mcpServers` configuration.

3. **Restart Claude Desktop**

   After saving the configuration file, quit Claude Desktop completely and restart it. The application needs to restart to load the new configuration and start the MCP servers.

4. **Verify Installation**

   1. Launch Claude Desktop
   2. Navigate to `Claude->Settings->Connectors`
   3. Verify that the configured Proto-OKN endpoints appear in the connector list
   4. You can configure each service to always ask for permission or to run it unsupervised (recommended)

### VS Code Setup

**For advanced users and developers**

1. **Install VS Code Insiders**

   Download and install VS Code Insiders from [https://code.visualstudio.com/insiders/](https://code.visualstudio.com/insiders/)

   > **Note**: VS Code Insiders is required as it includes the latest MCP (Model Context Protocol) features.

2. **Install GitHub Copilot Extension**

   - Open VS Code Insiders
   - Sign in with your GitHub account
   - Install the GitHub Copilot extension

   > **Requirements**: GitHub Copilot subscription is required for MCP integration.

3. **Configure MCP Server**

   **Option A: Download Pre-configured File (Recommended)**

   Download the pre-configured `mcp.json` file with FRINK endpoints from the repository and copy it to the appropriate location.

   **macOS**:
   ```bash
   # Download the config file
   curl -o /tmp/mcp.json https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/config/mcp.json
   
   # Copy to VS Code Insiders configuration directory
   cp /tmp/mcp.json "$HOME/Library/Application Support/Code - Insiders/User/mcp.json"
   ```
 > **Note**: VS Code Insiders mcp.json file is identical to the claude_desktop_config.json file, except "mcpServer" is replace by "server".

4. **Use the MCP Server**

   1. Open a new chat window in VS Code
   2. Select **Agent** mode
   3. Choose **Claude Sonnet 4.5 or later** model for optimal performance
   4. The MCP servers will automatically connect and provide knowledge graph access


## Quick Start

Once configured, you can immediately start querying knowledge graphs through natural language prompts in Claude Desktop or VS Code chat interface.

### Example Queries

1. **Use specific MCP servers**
   If you want to query specific MCP servers,
   use the *@* operator to select the servers.
   ```
   @spoke-sparkl
   ```
   To enable federated queries across multiple servers, you can specify more than one server name.
   ```
   @spoke-sparql @biobricks-sparql
   ```

2. **Knowledge Graph Overview**
   ```
   Provide a concise overview of the SPOKE knowledge graph, including its main purpose, data sources, and key features.
   ```

3. **Multi-Entity Analysis**
   ```
   Antibiotic contamination can contribute to antimicrobial resistance. Find locations with antibiotic contamination.
   ```

4. **Cross-Knowledge Graph Comparison**
   ```
   What type of data is available for perfluorooctanoic acid (PFOA) in SPOKE, BioBricks, and SAWGraph?
   ```

The AI assistant will automatically convert your natural language queries into appropriate SPARQL queries, execute them against the configured endpoints, and return structured, interpretable results.

## Development

### Installing from Source

If you want to run a development version:

```bash
# Clone the repository
git clone https://github.com/sbl-sdsc/mcp-proto-okn.git
cd mcp-proto-okn

# Install dependencies
uv sync
```

### Building and Publishing (maintainers only)

```bash
# Increment version number (patch, minor, major)
uv version --bump minor

# Build the package
uv build

# Publish to TestPyPI first (recommended)
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_PYPI_TOKEN_HERE

# Publish to PyPI 
uv publish --token pypi-YOUR_PYPI_TOKEN_HERE
```

## API Reference

### Available Tools

#### `query`

Executes SPARQL queries against the configured endpoint.

**Parameters:**
- `query_string` (string, required): A valid SPARQL query

**Returns:**
- JSON object containing query results

#### `get_description`

Retrieves endpoint metadata and documentation.

**Parameters:**
- None

**Returns:**
- String containing endpoint description, PI information, funding details, and related documentation links

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

This work is supported by:
- **National Science Foundation** Award [#2333819](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333819): "Proto-OKN Theme 1: Connecting Biomedical information on Earth and in Space via the SPOKE knowledge graph"

### Related Projects

- [Proto-OKN Project](https://www.proto-okn.net/) - Prototype Open Knowledge Network initiative
- [FRINK Platform](https://frink.renci.org/) - Knowledge graph hosting infrastructure  
- [Knowledge Graph Registry](https://frink.renci.org/registry/) - Catalog of available knowledge graphs
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI assistant integration standard
- [Original MCP Server SPARQL](https://github.com/ekzhu/mcp-server-sparql/) - Base implementation reference

---

*For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/sbl-sdsc/mcp-proto-okn).*
