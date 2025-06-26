#!/usr/bin/env python3
"""Check what's in mcp.server.stdio"""

try:
    import mcp.server.stdio
    print("Available in mcp.server.stdio:")
    for name in dir(mcp.server.stdio):
        if not name.startswith('_'):
            print(f"  {name}")
except Exception as e:
    print(f"Error: {e}")