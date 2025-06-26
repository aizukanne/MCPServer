#!/usr/bin/env python3
"""
MCP Server Entry Point
======================

This is the main entry point for the MCP server.
It should be run by an MCP client (like MCP Inspector or Claude Desktop).
"""

import asyncio
import sys
from main import OfficeAssistantServer

# The MCP SDK handles all the stdio setup when run through a client
server = OfficeAssistantServer()

# This is the standard pattern for MCP servers
# The client will handle creating the proper streams
asyncio.run(server.run())