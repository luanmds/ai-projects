"""
Notion API tools for MCP server.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError

from src.config import settings


logger = logging.getLogger(__name__)


class NotionTools:
    """Tools for interacting with Notion API."""

    def __init__(self):
        """Initialize Notion client."""
        if not settings.notion_api_key:
            logger.warning("Notion API key not configured")
            self.client = None
        else:
            self.client = Client(
                auth=settings.notion_api_key,
                notion_version=settings.notion_version,
            )

    def _check_client(self) -> None:
        """Check if Notion client is initialized."""
        if not self.client:
            raise Exception(
                "Notion API key not configured. Please set NOTION_API_KEY environment variable."
            )

    def _format_page_info(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Format page information for display."""
        title = "Untitled"
        
        # Extract title from properties
        if "properties" in page:
            for prop_name, prop_value in page["properties"].items():
                if prop_value.get("type") == "title" and prop_value.get("title"):
                    title_parts = []
                    for text_obj in prop_value["title"]:
                        if "text" in text_obj and "content" in text_obj["text"]:
                            title_parts.append(text_obj["text"]["content"])
                    if title_parts:
                        title = "".join(title_parts)
                    break

        return {
            "id": page["id"],
            "title": title,
            "url": page["url"],
            "created_time": page["created_time"],
            "last_edited_time": page["last_edited_time"],
            "archived": page.get("archived", False),
            "properties": page.get("properties", {}),
        }

    def _format_block_content(self, block: Dict[str, Any], level: int = 0) -> str:
        """Format block content for display."""
        indent = "  " * level
        block_type = block.get("type", "unknown")
        
        if block_type == "paragraph":
            text = self._extract_rich_text(block.get("paragraph", {}).get("rich_text", []))
            return f"{indent}• {text}" if text else ""
        
        elif block_type == "heading_1":
            text = self._extract_rich_text(block.get("heading_1", {}).get("rich_text", []))
            return f"{indent}# {text}"
        
        elif block_type == "heading_2":
            text = self._extract_rich_text(block.get("heading_2", {}).get("rich_text", []))
            return f"{indent}## {text}"
        
        elif block_type == "heading_3":
            text = self._extract_rich_text(block.get("heading_3", {}).get("rich_text", []))
            return f"{indent}### {text}"
        
        elif block_type == "bulleted_list_item":
            text = self._extract_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
            return f"{indent}- {text}"
        
        elif block_type == "numbered_list_item":
            text = self._extract_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
            return f"{indent}1. {text}"
        
        elif block_type == "to_do":
            text = self._extract_rich_text(block.get("to_do", {}).get("rich_text", []))
            checked = block.get("to_do", {}).get("checked", False)
            checkbox = "[x]" if checked else "[ ]"
            return f"{indent}{checkbox} {text}"
        
        elif block_type == "toggle":
            text = self._extract_rich_text(block.get("toggle", {}).get("rich_text", []))
            return f"{indent}▼ {text}"
        
        elif block_type == "quote":
            text = self._extract_rich_text(block.get("quote", {}).get("rich_text", []))
            return f"{indent}> {text}"
        
        elif block_type == "code":
            language = block.get("code", {}).get("language", "")
            text = self._extract_rich_text(block.get("code", {}).get("rich_text", []))
            return f"{indent}```{language}\n{text}\n{indent}```"
        
        elif block_type == "divider":
            return f"{indent}---"
        
        else:
            return f"{indent}[{block_type.upper()}]"

    def _extract_rich_text(self, rich_text_list: List[Dict[str, Any]]) -> str:
        """Extract plain text from rich text objects."""
        text_parts = []
        for text_obj in rich_text_list:
            if "text" in text_obj and "content" in text_obj["text"]:
                text_parts.append(text_obj["text"]["content"])
        return "".join(text_parts)

    async def get_notion_pages(self, query: Optional[str] = None, page_size: int = 10) -> str:
        """Get pages from Notion workspace."""
        self._check_client()
        
        try:
            if query:
                # Use search API if query is provided
                response = self.client.search(
                    query=query,
                    page_size=min(page_size, 100),
                    filter={"property": "object", "value": "page"}
                )
            else:
                # Use search without query to get all pages
                response = self.client.search(
                    page_size=min(page_size, 100),
                    filter={"property": "object", "value": "page"}
                )
            
            pages = response.get("results", [])
            
            if not pages:
                return "No pages found."
            
            result = f"Found {len(pages)} page(s):\n\n"
            
            for i, page in enumerate(pages, 1):
                page_info = self._format_page_info(page)
                result += f"{i}. **{page_info['title']}**\n"
                result += f"   - ID: {page_info['id']}\n"
                result += f"   - URL: {page_info['url']}\n"
                result += f"   - Created: {page_info['created_time']}\n"
                result += f"   - Last edited: {page_info['last_edited_time']}\n"
                if page_info['archived']:
                    result += f"   - Status: Archived\n"
                result += "\n"
            
            return result
            
        except APIResponseError as e:
            logger.error(f"Notion API error: {e}")
            return f"Error accessing Notion API: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"

    async def get_page_content(self, page_id: str, include_children: bool = True) -> str:
        """Get content from a specific Notion page."""
        self._check_client()
        
        try:
            # First, get the page information
            page = self.client.pages.retrieve(page_id)
            page_info = self._format_page_info(page)
            
            result = f"**{page_info['title']}**\n"
            result += f"URL: {page_info['url']}\n"
            result += f"Created: {page_info['created_time']}\n"
            result += f"Last edited: {page_info['last_edited_time']}\n\n"
            
            # Get page content (blocks)
            blocks = self._get_page_blocks(page_id, include_children)
            
            if blocks:
                result += "**Content:**\n\n"
                for block_text in blocks:
                    if block_text.strip():
                        result += block_text + "\n"
            else:
                result += "This page has no content blocks."
            
            return result
            
        except APIResponseError as e:
            logger.error(f"Notion API error: {e}")
            return f"Error accessing Notion API: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"

    def _get_page_blocks(self, page_id: str, include_children: bool = True, level: int = 0) -> List[str]:
        """Recursively get all blocks from a page."""
        blocks_text = []
        
        try:
            response = self.client.blocks.children.list(block_id=page_id, page_size=100)
            blocks = response.get("results", [])
            
            for block in blocks:
                block_text = self._format_block_content(block, level)
                if block_text:
                    blocks_text.append(block_text)
                
                # If block has children and we want to include them
                if include_children and block.get("has_children", False):
                    child_blocks = self._get_page_blocks(block["id"], include_children, level + 1)
                    blocks_text.extend(child_blocks)
            
        except APIResponseError as e:
            logger.error(f"Error getting blocks for {page_id}: {e}")
            blocks_text.append(f"Error getting blocks: {e}")
        
        return blocks_text

    async def search_notion(self, query: str, filter_options: Optional[Dict] = None, page_size: int = 10) -> str:
        """Search for pages and databases in Notion."""
        self._check_client()
        
        try:
            search_params = {
                "query": query,
                "page_size": min(page_size, 100),
            }
            
            if filter_options:
                search_params["filter"] = filter_options
            
            response = self.client.search(**search_params)
            results = response.get("results", [])
            
            if not results:
                return f"No results found for query: '{query}'"
            
            result = f"Found {len(results)} result(s) for '{query}':\n\n"
            
            for i, item in enumerate(results, 1):
                if item["object"] == "page":
                    page_info = self._format_page_info(item)
                    result += f"{i}. **[PAGE] {page_info['title']}**\n"
                    result += f"   - ID: {page_info['id']}\n"
                    result += f"   - URL: {page_info['url']}\n"
                elif item["object"] == "database":
                    title = item.get("title", [])
                    db_title = "Untitled Database"
                    if title:
                        db_title = self._extract_rich_text(title)
                    result += f"{i}. **[DATABASE] {db_title}**\n"
                    result += f"   - ID: {item['id']}\n"
                    result += f"   - URL: {item['url']}\n"
                
                result += f"   - Created: {item['created_time']}\n"
                result += f"   - Last edited: {item['last_edited_time']}\n\n"
            
            return result
            
        except APIResponseError as e:
            logger.error(f"Notion API error: {e}")
            return f"Error searching Notion: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"

    async def get_database_pages(
        self, 
        database_id: str, 
        page_size: int = 10,
        filter_conditions: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None
    ) -> str:
        """Get pages from a specific Notion database."""
        self._check_client()
        
        try:
            query_params = {
                "database_id": database_id,
                "page_size": min(page_size, 100),
            }
            
            if filter_conditions:
                query_params["filter"] = filter_conditions
            
            if sorts:
                query_params["sorts"] = sorts
            
            response = self.client.databases.query(**query_params)
            pages = response.get("results", [])
            
            if not pages:
                return f"No pages found in database {database_id}"
            
            result = f"Found {len(pages)} page(s) in database:\n\n"
            
            for i, page in enumerate(pages, 1):
                page_info = self._format_page_info(page)
                result += f"{i}. **{page_info['title']}**\n"
                result += f"   - ID: {page_info['id']}\n"
                result += f"   - URL: {page_info['url']}\n"
                result += f"   - Created: {page_info['created_time']}\n"
                result += f"   - Last edited: {page_info['last_edited_time']}\n"
                
                # Show some properties
                if page_info['properties']:
                    result += f"   - Properties: {len(page_info['properties'])} properties\n"
                
                result += "\n"
            
            return result
            
        except APIResponseError as e:
            logger.error(f"Notion API error: {e}")
            return f"Error accessing database: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"
