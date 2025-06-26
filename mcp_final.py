#!/usr/bin/env python3
"""
MCP Server - Final Working Version
==================================

This implements the MCP server correctly based on the SDK.
"""

import asyncio
import sys
import logging
from contextlib import asynccontextmanager

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Import server components
from main import OfficeAssistantServer
from mcp.server.models import InitializationOptions

# Import the stdio_server from mcp.server.stdio
from mcp.server.stdio import stdio_server

async def run_server():
    """Run the MCP server with stdio transport."""
    # Create server instance
    office_server = OfficeAssistantServer()
    
    # Create initialization options
    init_options = InitializationOptions(
        server_name="office-assistant",
        server_version="1.0.0",
        capabilities={"tools": {}}
    )
    
    # Use stdio_server as an async context manager
    # It provides the proper stream types for the MCP server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Starting MCP server with stdio transport...")
        
        # Run the server with the streams from stdio_server
        await office_server.server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=init_options
        )

if __name__ == "__main__":
    # Run the server
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)