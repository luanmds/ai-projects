# Notion MCP Server Sample

A Model Context Protocol (MCP) server implementation for Notion API integration.

## Overview

This MCP server provides tools to interact with Notion workspaces, allowing AI assistants to:

- Retrieve pages from Notion workspaces
- Get page content including blocks and formatting
- Search across pages and databases
- Query database pages with filters and sorting

## Features

- **Get Notion Pages**: Retrieve pages from your workspace with optional search queries
- **Get Page Content**: Extract full content from specific pages including nested blocks
- **Search Notion**: Search across pages and databases in your workspace  
- **Rich Content Parsing**: Properly formats different block types (paragraphs, headings, lists, code, etc.)
- **Async Support**: Full asynchronous operation support
- **Type Safety**: Built with Pydantic for robust type validation

## Installation

### Prerequisites

- Python 3.8 or higher
- A Notion account and integration token

### Setup Steps

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd notion-mcp-server-sample
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your Notion integration:**
   - Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Click "Create new integration"
   - Give it a name (e.g., "MCP Server")
   - Copy the "Internal Integration Token"

5. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Notion API key:
# NOTION_API_KEY=your_notion_integration_token_here
```

6. **Share pages with your integration:**
   - Open any Notion page you want the MCP server to access
   - Click the "•••" menu (top right)
   - Go to "Add connections"
   - Search for and select your integration

## Usage

### Running the MCP Server

The server runs as an MCP server using stdio transport:

```bash
python -m src.main
```

### Testing the Tools

You can test the Notion tools directly:

```bash
python test_notion.py
```

### Available Tools

#### 1. `get_notion_pages`
Retrieve pages from your Notion workspace.

**Parameters:**
- `query` (optional): Search query for pages
- `page_size` (optional): Number of pages to retrieve (default: 10, max: 100)

**Example:**
```json
{
  "query": "meeting notes",
  "page_size": 5
}
```

#### 2. `get_page_content`
Get content from a specific Notion page.

**Parameters:**
- `page_id` (required): The ID of the Notion page
- `include_children` (optional): Whether to include child blocks recursively (default: true)

**Example:**
```json
{
  "page_id": "1429989f-e8ac-4eff-bc8f-57f56486db54",
  "include_children": true
}
```

#### 3. `search_notion`
Search for pages and databases in Notion.

**Parameters:**
- `query` (required): Search query string
- `filter` (optional): Filter options for search
- `page_size` (optional): Number of results to return (default: 10, max: 100)

**Example:**
```json
{
  "query": "project documentation",
  "filter": {
    "property": "object",
    "value": "page"
  },
  "page_size": 10
}
```

#### 4. `get_database_pages`
Get pages from a specific Notion database.

**Parameters:**
- `database_id` (required): The ID of the Notion database
- `page_size` (optional): Number of pages to retrieve (default: 10, max: 100)
- `filter` (optional): Filter conditions for database query
- `sorts` (optional): Sort conditions for database query

**Example:**
```json
{
  "database_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "page_size": 20,
  "sorts": [
    {
      "property": "Created",
      "direction": "descending"
    }
  ]
}
```

### Finding Page and Database IDs

There are several ways to find Notion page and database IDs:

1. **From the URL:**
   - Open the page/database in Notion
   - Copy the URL
   - The ID is the 32-character string at the end
   - Format it as: `8-4-4-4-12` (add hyphens)
   - Example: `1429989fe8ac4effbc8f57f56486db54` → `1429989f-e8ac-4eff-bc8f-57f56486db54`

2. **Use the search tool:**
   - The `search_notion` and `get_notion_pages` tools return page IDs
   - Use these to discover available pages and databases

## Configuration

The server can be configured through environment variables:

- `NOTION_API_KEY`: Your Notion integration token (required)
- `NOTION_VERSION`: Notion API version (default: "2022-06-28")
- `SERVER_NAME`: Name of the MCP server (default: "Notion MCP Server")
- `LOG_LEVEL`: Logging level (default: "INFO")

## Content Formatting

The server formats different Notion block types:

- **Paragraphs**: Prefixed with "•"
- **Headings**: Formatted as Markdown headers (#, ##, ###)
- **Lists**: Bulleted (-) and numbered (1.) lists
- **To-do items**: Checkbox format ([ ] or [x])
- **Code blocks**: Formatted with language and code fences
- **Quotes**: Prefixed with ">"
- **Toggles**: Prefixed with "▼"

## Error Handling

The server includes comprehensive error handling:

- **API Key Missing**: Clear error message with setup instructions
- **Notion API Errors**: Detailed error reporting from Notion API
- **Permission Errors**: Guidance on sharing pages with the integration
- **Rate Limiting**: Proper handling of Notion API rate limits

## Development

### Project Structure

```
src/
├── __init__.py
├── main.py              # Entry point
├── server.py            # MCP server implementation
├── config.py            # Configuration management
└── tools/
    ├── __init__.py
    └── notion_tools.py  # Notion API tools
```

## Troubleshooting

### Common Issues

1. **"Notion API key not configured"**
   - Make sure `NOTION_API_KEY` is set in your environment
   - Check that the API key is valid and not expired

2. **"Error accessing Notion API: Unauthorized"**
   - Verify your API key is correct
   - Make sure your integration has access to the pages you're trying to access

3. **"No results found"**
   - Check that pages are shared with your integration
   - Try different search terms or broader queries

4. **Import errors when running**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're running from the correct directory

### Getting Help

- Check the [Notion API documentation](https://developers.notion.com/docs)
- Review the [MCP specification](https://modelcontextprotocol.io/)
- Look at the example usage in `test_notion.py`

## License

MIT License - see LICENSE file for details.
