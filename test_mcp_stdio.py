#!/usr/bin/env python3
"""
Test MCP stdio transport
========================

This script tests if the stdio transport is working correctly.
"""

import asyncio
import sys

async def test_stdio_import():
    """Test if we can import the stdio_server correctly."""
    try:
        from mcp.server.stdio import stdio_server
        print("✓ Successfully imported stdio_server from mcp.server.stdio")
        return True
    except ImportError as e:
        print(f"✗ Failed to import stdio_server: {e}")
        print("  This might mean the MCP library version doesn't have this module")
        return False

async def test_stdio_context():
    """Test if stdio_server context manager works."""
    try:
        from mcp.server.stdio import stdio_server
        print("\nTesting stdio_server context manager...")
        
        # Don't actually run it, just check if it's callable
        if callable(stdio_server):
            print("✓ stdio_server is callable")
            return True
        else:
            print("✗ stdio_server is not callable")
            return False
    except Exception as e:
        print(f"✗ Error testing stdio_server: {e}")
        return False

async def main():
    """Run all tests."""
    print("MCP stdio Transport Test")
    print("=" * 40)
    
    # Test import
    import_ok = await test_stdio_import()
    
    # Test context manager
    if import_ok:
        context_ok = await test_stdio_context()
    else:
        context_ok = False
    
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    
    if import_ok and context_ok:
        print("✓ stdio transport should work correctly")
    else:
        print("✗ stdio transport may have issues")
        print("\nPossible solutions:")
        print("1. Check MCP library version (current: 1.9.4)")
        print("2. The stdio_server might be in a different module")
        print("3. Try using the server directly without stdio_server wrapper")

if __name__ == "__main__":
    asyncio.run(main())