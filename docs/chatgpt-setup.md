# Add mcp-proto-okn Server to ChatGPT Web App

> **Requirements**:
> 
> ChatGPT with a subscription
> 
> Use the ChatGPT web app (https://chatgpt.com/)
> 
> ChatGPT desktop does not support MCP services

### Add proto-okn Remote MCP Server

1. Open ChatGPT

Go to: https://chatgpt.com and sign in to your account.

2. Locate Your Profile Menu

In the **bottom-left corner** of the screen, click on your **profile name or avatar**.

3. From the menu that appears, click ```Settings```.

4. Click on ```Apps``` and then click on ```Advanced settings```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/chatgpt-adv-settings.png"
     alt="ChatGPT advanced settings"
     width="500">

5. Toggle on ```Developer mode```

MCP services only work in developer mode!

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/chatgpt-dev-mode.png"
     alt="ChatGPT Developer mode"
     width="500">

6. Click ```Create app`` and enter the data shown below (MCP Server URL: https://frink.apps.renci.org/mcp/proto-okn/mcp)

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/chatgpt-add-proto-app.png"
     alt="ChatGTP add Proto-OKN service"
     width="500">

------------------------------------------------------------------------

### Run an Example Query

1. Create a new chat, click on the ```+``` sign, ```... More >``` and select ```proto-okn```

<img src="https://raw.githubusercontent.com/sbl-sdsc/mcp-proto-okn/main/docs/images/chatgpt-add-proto-okn.png"
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