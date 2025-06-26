#!/usr/bin/env python3
"""
MCP Server Starter
==================

Start the MCP server without calling run() directly.
"""

import asyncio
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Main entry point."""
    # Import server components
    from main import OfficeAssistantServer
    
    # Create server but don't run it
    server = OfficeAssistantServer()
    
    logger.info("MCP Server initialized")
    logger.info(f"Server name: {server.server.name}")
    logger.info(f"Tools available: {len(server.tool_handlers)}")
    
    # The MCP Inspector should handle running the server
    # We just need to keep the process alive
    logger.info("Server ready for MCP client connection...")
    
    # Keep the server alive
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Server stopped")

if __name__ == "__main__":
    # Check if we should show usage
    if sys.stdin.isatty():
        print("This server should be run via MCP Inspector:", file=sys.stderr)
        print("npx @modelcontextprotocol/inspector python mcp_start.py", file=sys.stderr)
    
    asyncio.run(main())