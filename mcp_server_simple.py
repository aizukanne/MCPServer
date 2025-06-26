#!/usr/bin/env python3
"""
Simple MCP Server
=================

Minimal MCP server to test the correct pattern.
"""

import asyncio
import sys
import logging
from mcp.server import Server
from mcp.server.models import InitializationOptions

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)

async def run():
    """Run a minimal MCP server."""
    # Create a minimal server
    server = Server("test-server")
    
    # Log what we're doing
    logging.info("Starting minimal MCP server...")
    
    # The server expects to be called with proper streams from the MCP client
    # When run via MCP Inspector, it should provide the correct stream types
    
    # For now, let's see what happens with a minimal setup
    options = InitializationOptions(
        server_name="test-server",
        server_version="1.0.0",
        capabilities={}
    )
    
    # This will fail with regular stdio, but the error will tell us what's expected
    await server.run(
        read_stream=sys.stdin.buffer,
        write_stream=sys.stdout.buffer,
        initialization_options=options
    )

if __name__ == "__main__":
    # When run directly, show usage
    if sys.stdin.isatty():
        print("This server should be run via MCP Inspector:", file=sys.stderr)
        print("npx @modelcontextprotocol/inspector python mcp_server_simple.py", file=sys.stderr)
        print("\nThe error below shows what the MCP library expects:", file=sys.stderr)
    
    # Run and let the error show what's needed
    asyncio.run(run())