#!/usr/bin/env python3
"""
MCP Server with Proper STDIO Handling
=====================================

This implements the correct pattern for MCP servers.
"""

import sys
from main import OfficeAssistantServer

# For MCP servers, we need to use the stdio transport
# that comes with the MCP Python SDK
if __name__ == "__main__":
    import mcp.server.stdio
    
    # Create the server instance
    server_instance = OfficeAssistantServer()
    
    # Run with stdio transport
    # This is the standard pattern from MCP SDK examples
    mcp.server.stdio.run_stdio_server(server_instance.server)