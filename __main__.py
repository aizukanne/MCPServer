#!/usr/bin/env python3
"""
MCP Server Package Entry Point
==============================

This allows the package to be run with `python -m mcp_office_assistant`.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import and run the MCP stdio server
    import mcp.server.stdio
    from main import OfficeAssistantServer
    
    # Create server instance
    server = OfficeAssistantServer()
    
    # Run with MCP's stdio handler
    mcp.server.stdio.run_stdio_server(server.server)