"""
Example script to test Notion tools functionality.
"""

import asyncio
import os
import sys
import logging

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import settings
from src.tools.notion_tools import NotionTools


async def main():
    """Test the Notion tools."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Check if API key is configured
    if not settings.notion_api_key:
        logger.error("NOTION_API_KEY not configured!")
        logger.info("Please set the NOTION_API_KEY environment variable.")
        logger.info("You can get your API key from: https://www.notion.so/my-integrations")
        return
    
    # Create tools instance
    tools = NotionTools()
    
    logger.info("Testing Notion tools...")
    
    # Test getting pages
    logger.info("Getting pages...")
    pages_result = await tools.get_notion_pages(page_size=5)
    print("Pages Result:")
    print(pages_result)
    print("-" * 50)
    
    # Test search
    logger.info("Searching for pages...")
    search_result = await tools.search_notion("test", page_size=3)
    print("Search Result:")
    print(search_result)
    print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
