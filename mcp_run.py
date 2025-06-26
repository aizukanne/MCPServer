#!/usr/bin/env python3
"""
MCP Server Runner
=================

This runs the MCP server using the SDK's built-in stdio handling.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import required modules
    import asyncio
    from mcp.server.stdio import stdio_server
    from main import OfficeAssistantServer
    
    # Create server instance
    server = OfficeAssistantServer()
    
    # Use MCP's built-in stdio server runner
    # This handles all the stream conversion automatically
    asyncio.run(stdio_server(server.server))