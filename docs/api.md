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
  - Available classes (node types)
  - Relationships/predicates (edges between nodes)
  - Edge properties (properties that exist on relationships themselves, such as log2fc, p-values, etc.)
  - Properties with labels and descriptions (when available)

**Schema Structure:**
The schema distinguishes between:
- **Node classes**: Entity types (e.g., Gene, Study, Assay)
- **Edge predicates**: Relationships between nodes (e.g., MEASURED_IN, ASSOCIATED_WITH)
- **Edge properties**: Data stored on relationships themselves (accessed via RDF reification)

#### `query`
Executes SPARQL queries against the configured endpoint with intelligent query analysis.

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
- Includes automatic query analysis warnings for:
  - LIMIT clauses without ORDER BY (suggests ordering to get meaningful results)
  - Incorrect access to edge properties (guides toward RDF reification pattern)

**Query Analysis Features:**
The tool automatically analyzes queries and provides warnings/suggestions:
- **LIMIT without ORDER BY**: When a query uses LIMIT but no ORDER BY, the tool warns that results will be arbitrary and suggests an appropriate ORDER BY clause based on query context
- **Edge property access**: When a query references predicates that have edge properties but doesn't use the RDF reification pattern, provides guidance on proper access patterns

**Edge Properties Access Pattern:**
For relationships with associated data (edge properties), use the RDF reification pattern:
```sparql
?stmt rdf:subject ?source ;
      rdf:predicate schema:RELATIONSHIP_NAME ;
      rdf:object ?target ;
      schema:property_name ?value .
```

#### `clean_mermaid_diagram`
Cleans Mermaid class diagrams by removing unwanted elements that cause rendering issues.

**Parameters:**
- `mermaid_content` (string, required): The raw Mermaid class diagram content

**Returns:**
- Cleaned Mermaid content with the following transformations:
  - All note statements removed (would render as unreadable yellow boxes)
  - Empty curly braces removed from class definitions (both single-line and multi-line formats)
  - Strings after newline characters truncated (e.g., "ClassName\nextra" becomes "ClassName")
  - Vertical bars (|) removed as they're not allowed in class diagrams

**Use Case:**
This tool is essential for creating clean, renderable Mermaid diagrams from knowledge graph schemas. It should always be called after generating a draft diagram and before presenting the final visualization.

#### `create_chat_transcript`
Generates a prompt for creating a formatted markdown chat transcript.

**Parameters:**
- None

**Returns:**
- A detailed prompt string with instructions for creating a chat transcript in markdown format, including:
  - Formatting guidelines for user prompts and assistant responses
  - Instructions for inline inclusion of visualizations and mermaid diagrams
  - File naming conventions and save location (~/Downloads/)
  - Footer template with version information

**Use Case:**
Helps create well-formatted documentation of chat sessions exploring knowledge graphs, including queries, visualizations, and insights.

#### `visualize_schema`
Generates a comprehensive prompt for creating a Mermaid class diagram visualization of the knowledge graph schema.

**Parameters:**
- None

**Returns:**
- A detailed prompt string with step-by-step instructions for:
  - Retrieving and analyzing the schema
  - Identifying node classes, edge predicates, and edge properties
  - Generating a draft Mermaid class diagram
  - **Mandatory cleaning step** using `clean_mermaid_diagram` tool
  - Presenting the cleaned diagram inline and as a .mermaid file
  - Proper handling of edges with properties (as intermediary classes)

**Critical Workflow:**
1. Call `get_schema()` to retrieve schema data
2. Analyze schema to identify nodes, edges, and edge properties
3. Generate draft Mermaid diagram
4. **MUST call `clean_mermaid_diagram`** to clean the draft
5. Present only the cleaned output
6. Save to `/mnt/user-data/outputs/<kg_name>-schema.mermaid`
7. Call `present_files` to share with user

**Edge Property Visualization:**
Edges with properties are represented as intermediary classes:
```mermaid
class RELATIONSHIP_NAME {
    float property1
    float property2
}
Assay --> RELATIONSHIP_NAME
RELATIONSHIP_NAME --> Gene
```

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

---
### Query Analysis System

The server includes an intelligent query analyzer that helps improve query quality:

**Features:**
- **LIMIT Analysis**: Detects queries with LIMIT but no ORDER BY and suggests appropriate ordering
- **Edge Property Detection**: Identifies when queries attempt to access edge properties without using proper RDF reification patterns
- **Variable Analysis**: Automatically suggests ORDER BY clauses based on variable names and context

**Automatic Suggestions:**
The analyzer prioritizes suggestions based on:
1. Numeric variable names (concentration, count, p_value, log2fc, etc.)
2. Context-appropriate sorting
3. First non-subject variable as fallback

**Edge Property Warnings:**
When a query references predicates known to have edge properties but doesn't use the reification pattern, the tool provides:
- List of predicates with edge properties being accessed
- Explanation of edge properties concept
- Template for correct RDF reification access pattern
- Reference to schema's edge_properties section
