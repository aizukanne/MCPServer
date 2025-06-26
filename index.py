#!/usr/bin/env python3
"""
MCP Server Entry Point
======================

This is the correct entry point for MCP servers using the Python SDK.
"""

import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Import our server implementation
from main import OfficeAssistantServer

# Create the server instance
office_server = OfficeAssistantServer()

# Run the server using MCP's stdio transport
# This is the standard pattern for MCP Python servers
mcp.server.stdio.run_stdio_server(office_server.server)