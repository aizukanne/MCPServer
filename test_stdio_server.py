#!/usr/bin/env python3
"""
Test stdio_server usage
=======================

Figure out how to use mcp.server.stdio.stdio_server correctly.
"""

import asyncio
import inspect
import mcp.server.stdio

# Check what stdio_server is
print(f"stdio_server type: {type(mcp.server.stdio.stdio_server)}")
print(f"Is coroutine function: {inspect.iscoroutinefunction(mcp.server.stdio.stdio_server)}")
print(f"Is async generator: {inspect.isasyncgenfunction(mcp.server.stdio.stdio_server)}")

# Check its signature
sig = inspect.signature(mcp.server.stdio.stdio_server)
print(f"Signature: {sig}")

# Check if it's a context manager
print(f"Has __aenter__: {hasattr(mcp.server.stdio.stdio_server, '__aenter__')}")
print(f"Has __enter__: {hasattr(mcp.server.stdio.stdio_server, '__enter__')}")

# List all attributes
attrs = [attr for attr in dir(mcp.server.stdio.stdio_server) if not attr.startswith('_')]
print(f"Attributes: {attrs}")

# Check the module for other functions
print("\nOther functions in mcp.server.stdio:")
for name in dir(mcp.server.stdio):
    if not name.startswith('_'):
        obj = getattr(mcp.server.stdio, name)
        print(f"  {name}: {type(obj)}")