# MCP Server Proto-OKN

A Model Context Protocol (MCP) server that provides tools for querying SPARQL endpoints, with specialized support for Proto-OKN (Prototype Open Knowledge Network) knowledge graphs hosted on the FRINK platform.

## Features

- **FRINK Integration**: Automatic detection and documentation linking for FRINK-hosted knowledge graphs
- **Proto-OKN Support**: Optimized for querying knowledge graphs in the Proto-OKN ecosystem including:
  - SPOKE (Scalable Precision Medicine Open Knowledge Engine)
  - BioBricks ICE (Chemical safety and cheminformatics)
  - DREAM-KG (Addressing homelessness with explainable AI)
  - SAWGraph (Safe Agricultural Products and Water monitoring)
  - And many other Proto-OKN knowledge graphs
- **Flexible Configuration**: Support for both FRINK and custom SPARQL endpoints
- **Automatic Documentation**: Registry links for supported knowledge graphs

## Installation

### Prerequisites

1. **Install VS Code Insiders** (required for MCP support)
   
   Download and install VS Code Insiders from [https://code.visualstudio.com/insiders/](https://code.visualstudio.com/insiders/)
   
   VS Code Insiders is needed because it includes the latest MCP (Model Context Protocol) features.

2. **Install GitHub Copilot extension** (required for MCP integration)
   
   - Open VS Code Insiders
   - Install the GitHub Copilot extension from the marketplace
   - Sign in with your GitHub account that has Copilot access
   - **Note**: You need an active GitHub Copilot subscription to use MCP features
   
   MCP servers integrate with VS Code through the Copilot Chat interface.

3. **Install uv** (Python package manager)
   
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip
   pip install uv
   ```

### Setup Instructions

1. **Clone and setup the project**

   ```bash
   git clone <repository-url>
   cd mcp-proto-okn
   uv sync
   ```

2. **Configure the MCP servers**

   This project includes a pre-configured `.vscode/mcp.json` file with multiple Proto-OKN knowledge graph endpoints. You need to update the commands to use the new `mcp-server-protookn`:

   Edit `.vscode/mcp.json` and update the server configurations:

   ```json
   {
     "servers": {
       "mcp-spoke-sparql": {
         "command": "uv",
         "args": ["run", "python", "-m", "mcp_server_protookn.server", "--endpoint", "https://frink.apps.renci.org/spoke/sparql"]
       },
       "mcp-dreamkg-sparql": {
         "command": "uv",
         "args": ["run", "python", "-m", "mcp_server_protookn.server", "--endpoint", "https://frink.apps.renci.org/dreamkg/sparql"]
       }
     }
   }
   ```

   The existing file contains configurations for all major Proto-OKN knowledge graphs. You can enable/disable specific servers by adding or removing them from the configuration.

3. **Start using the MCP server**

   - Open VS Code Insiders
   - Open a new chat window
   - The MCP servers should automatically connect and provide access to the knowledge graphs

### Quick Start: Query a Knowledge Graph

Once everything is set up, you can start querying knowledge graphs through the VS Code chat interface:

**Example prompts to try:**

1. **Explore the SPOKE knowledge graph structure:**
   ```
   What types of entities are available in the SPOKE knowledge graph?
   ```
2. **Query that combines multiple entity types:**
   ```
   Antibiotic contamination can contribute to antimicrobial resistance. Find locations with antibiotic contamination.
   ```

3. **Query across multiple KGs:**
   ```
   What type of data is available for perfluorooctanoic acid in SPOKE, BioBricks, and SAWGraph?
   ```


The chat interface will use the MCP server to execute SPARQL queries against the configured endpoints and return structured results.

### Alternative Installation Methods

#### Using uvx (standalone execution)

```bash
uvx mcp-server-protookn --endpoint https://frink.apps.renci.org/spoke/sparql
```

## Usage

### Command Line Parameters

The MCP server accepts the following command line arguments:

**Required:**
- `--endpoint`: SPARQL endpoint URL (e.g., `https://frink.apps.renci.org/spoke/sparql`)

**Optional:**
- `--description`: Custom description for the SPARQL endpoint (automatically generated for FRINK endpoints)

### Command Line

```bash
# FRINK endpoint (automatic documentation linking)
uvx mcp-server-protookn --endpoint https://frink.apps.renci.org/spoke/sparql

# Custom endpoint with description
uvx mcp-server-protookn --endpoint https://example.com/sparql --description "Custom SPARQL endpoint"
```

## Tool: `query`

Execute a SPARQL query against the configured endpoint.

**Parameters:**

- `query_string`: A valid SPARQL query string
- `description`: Custom description for the SPARQL endpoint (automatically generated for FRINK endpoints)

**Returns:**

- The query results in JSON format


## Links

- [Proto-OKN Project](https://www.proto-okn.net/)
- [FRINK Platform](https://frink.renci.org/)
- [Knowledge Graph Registry](https://frink.renci.org/registry/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Original MCP Server SPARQL](https://github.com/ekzhu/mcp-server-sparql/)
