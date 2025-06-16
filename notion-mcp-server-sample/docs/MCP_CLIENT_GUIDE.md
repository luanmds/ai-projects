# MCP Client Integration Guide

This guide explains how to integrate the Notion MCP Server with various MCP clients.

## Quick Start

1. **Setup the server:**
   ```bash
   bash setup.sh
   ```

2. **Configure your Notion API key:**
   ```bash
   # Edit .env file
   NOTION_API_KEY=your_notion_integration_token_here
   ```

3. **Test the server:**
   ```bash
   bash run.sh
   ```

## MCP Client Configuration

### Claude Desktop

1. **Find your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude-desktop/claude_desktop_config.json`

2. **Add the Notion MCP server:**
   ```json
   {
     "mcpServers": {
       "notion": {
         "command": "bash",
         "args": ["run.sh"],
         "cwd": "/absolute/path/to/notion-mcp-server-sample",
         "env": {
           "NOTION_API_KEY": "your_notion_api_key_here"
         }
       }
     }
   }
   ```

3. **Replace `/absolute/path/to/notion-mcp-server-sample`** with the actual path to this project directory.

4. **Replace `your_notion_api_key_here`** with your actual Notion integration token.

5. **Restart Claude Desktop** to load the new configuration.

### Other MCP Clients

For other MCP clients, use these connection details:

**Command:**
```bash
bash run.sh
```

**Working Directory:**
```
/path/to/notion-mcp-server-sample
```

**Environment Variables:**
```
NOTION_API_KEY=your_notion_api_key_here
```

## Available Tools

Once connected, you'll have access to these tools:

### 1. `get_notion_pages`
Retrieve pages from your Notion workspace.

**Parameters:**
- `query` (optional): Search query for pages
- `page_size` (optional): Number of pages to retrieve (1-100, default: 10)

**Example usage:**
- "Get my recent Notion pages"
- "Find pages about 'project planning'"

### 2. `get_page_content`
Get full content from a specific Notion page.

**Parameters:**
- `page_id` (required): The Notion page ID
- `include_children` (optional): Include nested blocks (default: true)

**Example usage:**
- "Show me the content of this Notion page: [page-id]"
- "Extract all text from my meeting notes page"

### 3. `search_notion`
Search across pages and databases in your workspace.

**Parameters:**
- `query` (required): Search terms
- `filter` (optional): Limit to pages or databases
- `page_size` (optional): Number of results (1-100, default: 10)

**Example usage:**
- "Search for 'quarterly review' in my Notion"
- "Find all databases related to 'customers'"

### 4. `get_database_pages`
Query pages from a specific Notion database.

**Parameters:**
- `database_id` (required): The database ID
- `page_size` (optional): Number of pages (1-100, default: 10)
- `filter` (optional): Filter conditions
- `sorts` (optional): Sort conditions

**Example usage:**
- "Show me all tasks from my project database"
- "Get recent entries from my CRM database"

## Troubleshooting

### Common Issues

1. **"Server not responding"**
   - Check that the server starts correctly: `bash run.sh`
   - Verify your Notion API key is configured in `.env`

2. **"Permission denied" errors**
   - Make sure scripts are executable: `chmod +x run.sh setup.sh`
   - Ensure the working directory path is correct

3. **"No pages found"**
   - Verify your Notion integration has access to pages
   - Share pages with your integration in Notion

4. **"API key not configured"**
   - Check that `NOTION_API_KEY` is set in `.env` file
   - Verify the API key is valid and not expired

### Getting Your Notion API Key

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "Create new integration"
3. Give it a name (e.g., "MCP Server")
4. Copy the "Internal Integration Token"
5. Share your Notion pages with the integration:
   - Open any Notion page
   - Click "•••" menu (top right)
   - Go to "Add connections"  
   - Select your integration

### Testing the Connection

You can test the server manually:

```bash
# Test server startup
bash run.sh

# Test with example client
python example_client.py

# Test tools directly
python test_notion.py
```

## Advanced Configuration

### Custom Environment Variables

You can set additional configuration in your `.env` file:

```bash
# Required
NOTION_API_KEY=your_api_key_here

# Optional
NOTION_VERSION=2022-06-28
LOG_LEVEL=INFO
SERVER_NAME=My Notion MCP Server
```

### Running as a Service

For production use, consider running the server as a system service or in a container.

### Security Notes

- Keep your Notion API key secure
- Only grant the integration access to necessary pages
- Consider using environment-specific API keys for different deployments

## Support

If you encounter issues:

1. Check the server logs when running `bash run.sh`  
2. Verify your Notion integration setup
3. Test with the provided example scripts
4. Review the Notion API documentation: https://developers.notion.com/docs

## Examples

### Basic Usage with Claude

Once configured with Claude Desktop, you can use natural language:

- "Show me my recent Notion pages"
- "What's in my project planning page?"
- "Search for meeting notes from last week"
- "Get all tasks from my project database"

The MCP server will automatically handle the API calls and return formatted results.
