# MCP Proto-OKN Server

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://badge.fury.io/py/mcp-proto-okn.svg?cachebust=1)](https://badge.fury.io/py/mcp-proto-okn)

A Model Context Protocol (MCP) server providing seamless access to SPARQL endpoints with specialized support for the NSF-funded [Proto-OKN Project](https://www.proto-okn.net/) (Prototype Open Knowledge Network). This server enables querying the scientific knowledge graphs hosted on the [FRINK](https://frink.renci.org/) platform. In addition, third-party SPARQL endpoints can be queried.

## Features

- **🔗 FRINK Integration**: Automatic detection and documentation linking for FRINK-hosted knowledge graphs
- **🕸️ Proto-OKN Knowledge Graphs**: Optimized support for biomedical and scientific knowledge graphs, including:
    - 🧬 Biology & Health
    - 🌱 Environment
    - ⚖️ Justice
    - 🛠️ Technology & Manufacturing
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

### Select and Configure MCP Tools (Claude Desktop)

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

## Example Queries

1. **Knowledge Graph Overviews & Class Diagrams**

Use @kg_name to refer to a specific knowledge graph in chat (for example, @spoke-genelab).
Each link below points to a chat transcript that demonstrates how to generate a knowledge-graph overview and class diagram for a given Proto-OKN Theme 1 KG. The examples are grouped by domain area.

| 🧬 Biology & Health | 🌱 Environment | ⚖️ Justice | 🛠️ Technology & Manufacturing | Other
|--------------------|---------------|-----------|-------------------------------|-------------|
| [biobricks-aopwiki](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-aopwiki_overview.md) | [sawgraph](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/sawgraph_overview.md) | [ruralkg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/ruralkg_overview.md) | [securechainkg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/securechainkg_overview.md) | [nasa-gesdisc-kg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/nasa-gesdisc-kg_overview.md) |
| [biobricks-ice](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-ice_overview.md) | [fiokg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/fiokg_overview.md) | [scales](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/scales_overview.md) | [sudokn](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/sudokn_overview.md) |
| [biobricks-mesh](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-mesh_overview.md) | [geoconnex](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/geoconnex_overview.md) | [nikg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/nikg_overview.md) |  |
| [biobricks-pubchem-annotations](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-pubchem-annotations_overview.md) | [spatialkg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spatialkg_overview.md) | [dreamkg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/dreamkg_overview.md) |  |
| [biobricks-tox21](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-tox21_overview.md) | [hydrologykg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/hydrologykg_overview.md) |  |  |
| [biobricks-toxcast](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks-toxcast_overview.md) | [ufokn](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/ufokn_overview.md) |  |  |
| [spoke-genelab](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke-genelab_overview.md) | [wildlifekn](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/wildlifekn_overview.md) |  |  |
| [spoke-okn](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke-okn_overview.md) | [climatemodelskg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/climatemodelskg_overview.md) |  |  |
|  | [sockg](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/sockg_overview.md) |  |  |

2. **Spaceflight Missions (spoke-genelab)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke-genelab_breakdown.md)
   
3. **Spaceflight Gene Expression Analysis (spoke-genelab, spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_spaceflight_analysis.md)

4. **Spaceflight Gene Expression with Literature Analysis (spoke-genelab, spoke-okn, PubMed)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/osd-161-sonnet-4.5.md)

5. **Disease Prevalence in the US (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/us_county_disease_prevalence.md)

6. **Disease Prevalence - Socio-Economic Factors Correlation (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/disease_socio_economic_correlation.md)

7. **Contamination at Superfund Sites (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/superfund-contaminants.md)

8. **PFOA in Drinking Water (spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke_okn_pfoa_drinking_water.md)

9. **Data about PFOA (spoke-okn, biobricks-toxcast)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/pfoa_data_spoke_okn_biobricks_toxcast.md)

10. **Biological Targets for PFOA (biobricks-toxcast)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/biobricks_toxcast_PFOA_targets.md)

11. **Criminal Justice Patterns (scales)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/scales_criminal_justice_analysis.md)

12. **Drug Possession Charges (scales)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/scales_drug_possession.md)

13. **Environmental Justice (sawgraph, scales, spatialkg, spoke-okn)**

    [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/environmental-justice-kg-analysis.md)

14. **Rural Health Access (ruralkg, dreamkg, spoke-okn)**

    [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/rural-health-access-mapping.md)

15. **Michigan Flooding Event (ufokn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/ufokn_michigan_flood.md)

16. **Flooding and Socio-Economic Factors (ufokn, spatialkg, spoke-okn)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/flooding-socioeconomic-correlation.md)

17. **Philadelphia Area Incidents (nikg)**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/nikg_philadelphia_incidents.md)

18. **Cross-KG Geolocation Analysis**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/cross-kg-geolocation-analysis.md)
   
19. **Cross-KG Chemical Compound Analysis**

   [Chat transcript](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/cross-kg-compound-analysis.md)


## Building and Publishing (maintainers only)

[Instructions for building, testing, and publishing the mcp-proto-okn package on PyPI](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/build_publish.md)


## API Reference and Query Analysis System

[mcp-proto-okn server API](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/api.md)

## Troubleshooting

**MCP server not appearing in Claude Desktop:**
- Ensure you've completely quit and restarted Claude Desktop (not just closed the window)
- Check that your JSON configuration is valid (attach your config file to a chat and ask it to fix any errors)
- Verify that `uvx` is installed and accessible in your PATH (which uvx)

**Connection errors:**
- Verify the SPARQL endpoint URL is correct and accessible
- Some endpoints may have rate limits or temporary downtime

**Performance issues:**
- Complex SPARQL queries may take time to execute
- Consider breaking down complex queries into smaller parts

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Citation

If you use MCP Server Proto-OKN in your research, please cite the following works:

```bibtex
@software{rose2025mcp-proto-okn,
  title={MCP Server Proto-OKN},
  author={Rose, P.W. and Nelson, C.A. and Saravia-Butler, A.M. and Shi, Y. and Baranzini, S.E.},
  year={2025},
  url={https://github.com/sbl-sdsc/mcp-proto-okn}
}

@software{rose2025spoke-genelab,
  title={NASA SPOKE-GeneLab Knowledge Graph},
  author={Rose, P.W. and Nelson, C.A. and Gebre, S.G. and Saravia-Butler, A.M. and Soman, K. and Grigorev, K.A. and Sanders, L.M. and Costes, S.V. and Baranzini, S.E.},
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
