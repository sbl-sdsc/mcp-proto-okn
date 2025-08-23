# MCP Server Proto-OKN

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server providing seamless access to SPARQL endpoints with specialized support for the NSF-funded [Proto-OKN Project](https://www.proto-okn.net/) (Prototype Open Knowledge Network). This server enables intelligent querying of biomedical and scientific knowledge graphs hosted on the [FRINK](https://frink.renci.org/) platform.

## Features

- **🔗 FRINK Integration**: Automatic detection and documentation linking for FRINK-hosted knowledge graphs
- **🧬 Proto-OKN Ecosystem**: Optimized support for biomedical and scientific knowledge graphs including:
  - **SPOKE** - Scalable Precision Medicine Open Knowledge Engine
  - **BioBricks ICE** - Chemical safety and cheminformatics data
  - **DREAM-KG** - Addressing homelessness with explainable AI
  - **SAWGraph** - Safe Agricultural Products and Water monitoring
  - **Additional Proto-OKN knowledge graphs** - Expanding ecosystem of scientific data
- **⚙️ Flexible Configuration**: Support for both FRINK and custom SPARQL endpoints
- **📚 Automatic Documentation**: Registry links and metadata for supported knowledge graphs

## Architecture

![MCP Architecture](mcp_architecture.png)

The MCP Server Proto-OKN acts as a bridge between AI assistants (like Claude) and SPARQL knowledge graphs, enabling natural language queries to be converted into structured SPARQL queries and executed against scientific databases.

## Prerequisites

Before installing the MCP Server Proto-OKN, ensure you have:

- **Operating System**: macOS, Linux, or Windows
- **Client Application**: One of the following:
  - Claude Desktop with Pro or Max subscription
  - VS Code Insiders with GitHub Copilot subscription

## Installation

### Initial Setup

1. **Install uv Package Manager**

   The `uv` package manager is required for Python dependency management:

   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Alternative: via pip
   pip install uv
   ```

   > **Note**: Python installation is not required. `uv` will automatically install Python and all dependencies.

2. **Verify Installation Path** (macOS only)

   ```bash
   which uv
   ```

   If `uv` is not installed in `/usr/local/bin`, create a symbolic link for Claude Desktop compatibility:

   ```bash
   sudo ln -s $(which uv) /usr/local/bin/uv
   ```

3. **Clone and Setup Project**

   ```bash
   git clone https://github.com/sbl-sdsc/mcp-proto-okn.git
   cd mcp-proto-okn
   uv sync
   ```
4. **Create a `uv` tool**

   The tool runs in a self-contained environment managed by uv.
   ```bash
   uv tool install $HOME/path_to_git_repo/mcp-proto-okn
   uv tool list
   ```

### Claude Desktop Setup

**Recommended for most users**

1. **Download and Install Claude Desktop**

   Visit [https://claude.ai/download](https://claude.ai/download) and install Claude Desktop for your operating system.

   > **Requirements**: Claude Pro or Max subscription is required for MCP server functionality.

2. **Configure MCP Server**

   **macOS**
   ```bash
   cp claude_desktop_config.json "$HOME/Library/Application Support/Claude/"
   ```

   **Windows**
   ```bash
   copy claude_desktop_config.json  %APPDATA%\Claude\claude_desktop_config.json
   ```

   Refer to the [Claude documentation](https://modelcontextprotocol.io/quickstart/user) for details.

   > **Note**: If you have existing MCP server configurations, merge the contents instead of overwriting.

3. **Restart Claude Desktop**

   After saving the configuration file, quit Claude Desktop and restart it. The application needs to restart to load the new configuration and start the MCP server.

4. **Verify Installation**

   1. Launch Claude Desktop
   2. Click **"Connect your tools to Claude"** at the bottom of the interface
   3. Click **"Manage connectors"**
   4. Verify that `mcp-proto-okn` tools appear in the connector list

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

3. **Configure Workspace**

   1. Open VS Code Insiders
   2. File → Open Folder → Select `mcp-proto-okn` directory
   3. Open a new chat window
   4. Select **Agent** mode
   5. Choose **Claude Sonnet 4** model for optimal performance
   6. The MCP servers will automatically connect and provide knowledge graph access

## Configuration

The server comes pre-configured with 10 Proto-OKN SPARQL endpoints. You can customize the configuration by editing the appropriate files:

- **Claude Desktop**: `claude_desktop_config.json`
- **VS Code**: `.vscode/mcp.json`

### Adding Custom Endpoints

To add additional Proto-OKN endpoints or third-party SPARQL endpoints, modify the configuration file. The snippet below shows how to specify FRINK and third-party endpoints.

```json
{
  "mcpServers": {
    "mcp-spoke-sparql": {
      "command": "uv",
      "args": [
        "tool", "run", "mcp-server-protookn", 
        "--endpoint", "https://frink.apps.renci.org/spoke/sparql"
      ]
    },
    "mcp-uniprot-sparql": {
      "command": "uv",
      "args": [
        "tool", "run", "mcp-server-protookn",
        "--endpoint", "https://sparql.uniprot.org/sparql",
        "--description", "Resource for protein sequence and function information. For details: https://purl.uniprot.org/html/index-en.htm"
      ]
    }
  }
}
```

> **Note**: For VS Code configuration (`.vscode/mcp.json`), replace `mcpServers` with `servers`.

## Quick Start

Once configured, you can immediately start querying knowledge graphs through natural language prompts in Claude Desktop or VS Code chat interface.

### Example Queries

1. **Knowledge Graph Overview**
   ```
   Provide a concise overview of the SPOKE knowledge graph, including its main purpose, data sources, and key features.
   ```

2. **Multi-Entity Analysis**
   ```
   Antibiotic contamination can contribute to antimicrobial resistance. Find locations with antibiotic contamination.
   ```

3. **Cross-Knowledge Graph Comparison**
   ```
   What type of data is available for perfluorooctanoic acid in SPOKE, BioBricks, and SAWGraph?
   ```

The AI assistant will automatically convert your natural language queries into appropriate SPARQL queries, execute them against the configured endpoints, and return structured, interpretable results.

## Usage

### Command Line Interface

The MCP server can be invoked directly with the following parameters:

**Required Parameters:**
- `--endpoint` : SPARQL endpoint URL (e.g., `https://frink.apps.renci.org/spoke/sparql`)

**Optional Parameters:**
- `--description` : Custom description for the SPARQL endpoint (auto-generated for FRINK endpoints)

### Example Usage

```bash
uv tool run mcp-server-protookn --endpoint https://frink.apps.renci.org/spoke/sparql
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
  author={Rose, P.W. and Nelson, C.A. and Gebre, S.G. and Soman, K. and Grigorev, K.A. and Sanders, L.M. and Costes, S.V. and Baranzini, S.E.},
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
