#!/usr/bin/env python3
"""
Check MCP Module Structure
==========================

This script explores what's available in the MCP module.
"""

import sys
import importlib
import pkgutil

def explore_module(module_name, max_depth=3, current_depth=0):
    """Recursively explore a module's structure."""
    indent = "  " * current_depth
    
    try:
        module = importlib.import_module(module_name)
        print(f"{indent}{module_name}")
        
        if current_depth < max_depth and hasattr(module, '__path__'):
            # It's a package, explore submodules
            for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
                submodule_name = f"{module_name}.{modname}"
                explore_module(submodule_name, max_depth, current_depth + 1)
        
        # List important attributes
        if current_depth <= 1:
            attrs = [attr for attr in dir(module) if not attr.startswith('_')]
            if attrs:
                print(f"{indent}  Attributes: {', '.join(attrs[:10])}")
                if len(attrs) > 10:
                    print(f"{indent}  ... and {len(attrs) - 10} more")
                    
    except ImportError as e:
        print(f"{indent}{module_name} - Import Error: {e}")

def main():
    print("MCP Module Structure")
    print("=" * 50)
    
    # Check main MCP module
    try:
        import mcp
        print(f"\nMCP module found at: {mcp.__file__}")
        if hasattr(mcp, '__version__'):
            print(f"Version: {mcp.__version__}")
    except ImportError:
        print("MCP module not found!")
        return
    
    print("\nExploring MCP module structure:")
    explore_module('mcp', max_depth=2)
    
    print("\n\nChecking for stdio-related functions:")
    stdio_candidates = [
        'mcp.stdio_server',
        'mcp.server.stdio',
        'mcp.server.stdio_server',
        'mcp.stdio',
        'mcp.run_stdio_server',
        'mcp.server.run_stdio',
    ]
    
    for candidate in stdio_candidates:
        try:
            parts = candidate.split('.')
            module_name = '.'.join(parts[:-1])
            func_name = parts[-1]
            
            module = importlib.import_module(module_name)
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                print(f"✓ Found: {candidate} - {type(func)}")
            else:
                print(f"✗ Not found: {candidate}")
        except ImportError:
            print(f"✗ Module not found: {module_name}")
    
    print("\n\nChecking Server class methods:")
    try:
        from mcp.server import Server
        methods = [m for m in dir(Server) if not m.startswith('_') and callable(getattr(Server, m))]
        print(f"Server methods: {', '.join(methods)}")
    except ImportError:
        print("Could not import Server class")

if __name__ == "__main__":
    main()