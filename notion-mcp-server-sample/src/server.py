"""
MCP Server implementation for Notion integration.
"""

import logging

from mcp import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)

from src.config import settings
from src.tools.notion_tools import NotionTools


logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Server for Notion integration."""

    def __init__(self):
        """Initialize the MCP server."""
        self.app = Server("notion-mcp-server")
        self.notion_tools = NotionTools()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP handlers."""

        @self.app.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            logger.info("Listing available tools")
            return [
                Tool(
                    name="get_notion_pages",
                    description="Retrieve pages from Notion workspace",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for pages (optional)",
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of pages to retrieve (default: 10, max: 100)",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 10,
                            },
                        },
                        "additionalProperties": False,
                    },
                ),
                Tool(
                    name="get_page_content",
                    description="Get content (blocks) from a specific Notion page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "string",
                                "description": "The ID of the Notion page to retrieve content from",
                            },
                            "include_children": {
                                "type": "boolean",
                                "description": "Whether to include child blocks recursively (default: true)",
                                "default": True,
                            },
                        },
                        "required": ["page_id"],
                        "additionalProperties": False,
                    },
                ),
                Tool(
                    name="search_notion",
                    description="Search for pages and databases in Notion",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query string",
                            },
                            "filter": {
                                "type": "object",
                                "description": "Filter options for search",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "enum": ["page", "database"],
                                        "description": "Type of object to search for",
                                    },
                                    "property": {
                                        "type": "string",
                                        "enum": ["object"],
                                        "description": "Property to filter by",
                                    },
                                },
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of results to return (default: 10, max: 100)",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                ),
                Tool(
                    name="get_database_pages",
                    description="Get pages from a specific Notion database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database_id": {
                                "type": "string",
                                "description": "The ID of the Notion database",
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of pages to retrieve (default: 10, max: 100)",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 10,
                            },
                            "filter": {
                                "type": "object",
                                "description": "Filter conditions for database query",
                            },
                            "sorts": {
                                "type": "array",
                                "description": "Sort conditions for database query",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "property": {"type": "string"},
                                        "direction": {
                                            "type": "string",
                                            "enum": ["ascending", "descending"],
                                        },
                                    },
                                },
                            },
                        },
                        "required": ["database_id"],
                        "additionalProperties": False,
                    },
                ),
            ]

        @self.app.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            logger.info(f"Calling tool: {name} with arguments: {arguments}")

            try:
                if name == "get_notion_pages":
                    result = await self.notion_tools.get_notion_pages(
                        query=arguments.get("query"),
                        page_size=arguments.get("page_size", 10),
                    )
                elif name == "get_page_content":
                    result = await self.notion_tools.get_page_content(
                        page_id=arguments["page_id"],
                        include_children=arguments.get("include_children", True),
                    )
                elif name == "search_notion":
                    result = await self.notion_tools.search_notion(
                        query=arguments["query"],
                        filter_options=arguments.get("filter"),
                        page_size=arguments.get("page_size", 10),
                    )
                elif name == "get_database_pages":
                    result = await self.notion_tools.get_database_pages(
                        database_id=arguments["database_id"],
                        page_size=arguments.get("page_size", 10),
                        filter_conditions=arguments.get("filter"),
                        sorts=arguments.get("sorts"),
                    )
                else:
                    raise McpError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=result)]

            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                raise McpError(f"Tool execution failed: {str(e)}")

    async def run(self) -> None:
        """Run the MCP server."""
        logger.info(f"Starting {settings.server_name} v{settings.server_version}")
        
        # Check if Notion API key is configured
        if not settings.notion_api_key:
            logger.warning(
                "NOTION_API_KEY not configured. Some tools may not work properly. "
                "Please set the NOTION_API_KEY environment variable."
            )
        
        # Start the server using stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream, 
                write_stream, 
                self.app.create_initialization_options()
            )
