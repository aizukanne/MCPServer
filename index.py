#!/usr/bin/env python3
"""
MCP Server Entry Point
======================

This is the correct entry point for MCP servers using the Python SDK.
"""

import asyncio
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from main import OfficeAssistantServer

async def main():
    """Main entry point."""
    # Create the server instance
    office_server = OfficeAssistantServer()
    
    # Create initialization options
    init_options = InitializationOptions(
        server_name="office-assistant",
        server_version="1.0.0",
        capabilities={"tools": {}}
    )
    
    # stdio_server is likely an async context manager
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # Run the server with the streams
        await office_server.server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=init_options
        )

if __name__ == "__main__":
    asyncio.run(main())