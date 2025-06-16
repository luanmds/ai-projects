"""
Main entry point for the MCP server.
"""

import asyncio
import logging
import sys

from src.config import settings
from src.server import MCPServer


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
    )


async def main_async() -> None:
    """Main async entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Starting {settings.server_name} v{settings.server_version}")

    try:
        # Create and run the MCP server
        server = MCPServer()
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
