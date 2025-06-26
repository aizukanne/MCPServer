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
    # Import MCP's stdio server runner
    from mcp.server.stdio import run_stdio_server
    from main import OfficeAssistantServer
    
    # Create server instance
    server = OfficeAssistantServer()
    
    # Use MCP's built-in stdio server runner
    # This handles all the stream conversion automatically
    run_stdio_server(server.server)