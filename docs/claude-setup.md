# Setup Claude Desktop and Add mcp-proto-okn Server

### Download and Install Claude Desktop

   Visit [https://claude.ai/download](https://claude.ai/download) and install Claude Desktop for your operating system.

   > **Requirements**: Claude Pro or Max subscription is required for MCP server functionality.

------------------------------------------------------------------------

### Add proto-okn Remote MCP Server

1. Launch Claude Desktop and navigate to Claude->Settings

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/claude-settings.png"
     alt="Claude settings"
     width="250">

2. Select ```Connectors``` from the Settings menu and click ```Add custom connector```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/claude-connectors.png"
     alt="Claude connectors"
     width="500">

3. Enter the name ```proto-okn``` and the URL ```https://frink.apps.renci.org/mcp/proto-okn/mcp```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/claude-add-proto-okn.png"
     alt="Claude add proto-okn"
     width="500">

4. Once ```proto-okn``` was added, click on ```Configure``` and set tool permissions to ```Always allow```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/claude-configure.png"
     alt="Claude configure"
     width="500">

------------------------------------------------------------------------

### Run an Example Query

1. Create a new chat, click on the ```+``` sign, and toggle ```proto-okn``` service on.

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/claude-select-proto-okn.png"
     alt="Claude select proto-okn"
     width="500"> 

2. Toggle "Web search" off.

3. Run an example query:

```Generate a table of all Proto-OKN Knowledge Graphs with two columns: “KG Name” and “Description.”```

------------------------------------------------------------------------

## Troubleshooting

### Connector Not Appearing

-   Restart Claude Desktop
-   Confirm you are logged into a Pro or Max subscription
-   Re-add the custom connector

### Permission Errors

-   Ensure tool permissions are set to "Always allow"
-   Confirm proto-okn is toggled on in the chat session

### Empty or Unexpected Results

-   Verify Web search is turned OFF
-   Confirm proto-okn is enabled in the current chat