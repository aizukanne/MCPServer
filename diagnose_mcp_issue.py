#!/usr/bin/env python3
"""
Diagnose MCP Issue
==================

This script helps diagnose the exact issue with MCP server stdio handling.
"""

import sys
import inspect
import asyncio

def diagnose():
    """Run diagnostics on MCP library."""
    print("MCP Library Diagnostics")
    print("=" * 50)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Check MCP version
    try:
        import mcp
        print(f"\nMCP module found at: {mcp.__file__}")
        if hasattr(mcp, '__version__'):
            print(f"MCP version: {mcp.__version__}")
    except ImportError:
        print("\nERROR: MCP module not found!")
        return
    
    # Check Server class
    try:
        from mcp.server import Server
        print(f"\nServer class found: {Server}")
        
        # Check run method signature
        run_method = Server.run
        sig = inspect.signature(run_method)
        print(f"\nServer.run signature: {sig}")
        print("\nServer.run parameters:")
        for name, param in sig.parameters.items():
            print(f"  - {name}: {param}")
            
        # Check for async context manager support
        print(f"\nServer.run is coroutine: {inspect.iscoroutinefunction(run_method)}")
        
    except Exception as e:
        print(f"\nERROR checking Server: {e}")
    
    # Check for stdio helpers
    print("\n\nChecking for stdio helpers:")
    stdio_modules = [
        'mcp.stdio_server',
        'mcp.server.stdio',
        'mcp.stdio',
        'mcp.server.stdio_server',
    ]
    
    for module_name in stdio_modules:
        try:
            module = __import__(module_name, fromlist=[''])
            print(f"✓ Found: {module_name}")
            # List contents
            attrs = [attr for attr in dir(module) if not attr.startswith('_')]
            if attrs:
                print(f"  Contents: {', '.join(attrs[:5])}...")
        except ImportError:
            print(f"✗ Not found: {module_name}")
    
    # Check what the library expects for streams
    print("\n\nChecking stream handling:")
    try:
        from mcp.shared.session import Session
        print(f"Session class found: {Session}")
        
        # Look for _receive_loop method that's failing
        if hasattr(Session, '_receive_loop'):
            method = Session._receive_loop
            print(f"\nSession._receive_loop found")
            print(f"Is coroutine: {inspect.iscoroutinefunction(method)}")
            
            # Try to get source to understand what it expects
            try:
                import textwrap
                source = inspect.getsource(method)
                # Show first few lines
                lines = source.split('\n')[:10]
                print("\nFirst few lines of _receive_loop:")
                for line in lines:
                    print(f"  {line}")
            except:
                print("Could not get source code")
                
    except Exception as e:
        print(f"\nERROR checking Session: {e}")
    
    # Test BufferedReader async context manager
    print("\n\nTesting BufferedReader:")
    import io
    br = sys.stdin.buffer
    print(f"Type: {type(br)}")
    print(f"Has __aenter__: {hasattr(br, '__aenter__')}")
    print(f"Has __aexit__: {hasattr(br, '__aexit__')}")
    
    # Suggest solution
    print("\n\nDIAGNOSIS SUMMARY:")
    print("=" * 50)
    print("The error occurs because MCP is trying to use sys.stdin.buffer")
    print("as an async context manager, but BufferedReader doesn't support")
    print("the async context manager protocol (__aenter__/__aexit__).")
    print("\nThis suggests MCP expects async-compatible stream objects,")
    print("not the standard BufferedReader/BufferedWriter from sys.stdin/stdout.")

if __name__ == "__main__":
    diagnose()