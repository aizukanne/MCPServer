#!/usr/bin/env python3
"""
MCP Server Main Entry Point
===========================

This is the entry point that MCP Inspector expects.
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import OfficeAssistantServer

# Create the server instance
server = OfficeAssistantServer()

# The MCP Inspector will handle stdio setup and call this
if __name__ == "__main__":
    asyncio.run(server.run())