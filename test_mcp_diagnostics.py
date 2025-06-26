#!/usr/bin/env python3
"""
MCP Server Diagnostics Script
============================

This script helps diagnose issues with the MCP server setup.
"""

import sys
import os
import subprocess
import json
import asyncio
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("=== Checking Dependencies ===")
    
    required_packages = [
        "mcp",
        "boto3",
        "requests",
        "aiohttp",
        "beautifulsoup4",
        "weaviate-client",
        "openai",
        "fpdf",
        "markdown2",
        "nltk",
        "lxml",
        "python-dotenv"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    return missing

def check_fpdf_version():
    """Check the installed fpdf version."""
    print("\n=== Checking FPDF Version ===")
    try:
        import fpdf
        if hasattr(fpdf, '__version__'):
            print(f"FPDF version: {fpdf.__version__}")
        else:
            print("FPDF version: Unable to determine (likely 1.7.2)")
        
        # Test basic functionality
        from fpdf import FPDF
        pdf = FPDF()
        print("✓ FPDF import successful")
        return True
    except Exception as e:
        print(f"✗ FPDF error: {e}")
        return False

def check_environment():
    """Check environment variables."""
    print("\n=== Checking Environment ===")
    
    env_vars = [
        "OPENAI_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "WEAVIATE_URL",
        "WEAVIATE_API_KEY"
    ]
    
    missing_env = []
    for var in env_vars:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is NOT set")
            missing_env.append(var)
    
    return missing_env

def check_mcp_client_config():
    """Check if MCP client configuration exists."""
    print("\n=== Checking MCP Client Configuration ===")
    
    # Common MCP client config locations
    config_paths = [
        Path.home() / ".config" / "claude" / "claude_desktop_config.json",
        Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
        Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    ]
    
    config_found = False
    for path in config_paths:
        if path.exists():
            print(f"✓ Found MCP config at: {path}")
            config_found = True
            
            # Check if our server is configured
            try:
                with open(path, 'r') as f:
                    config = json.load(f)
                    if "mcpServers" in config:
                        if any("office-assistant" in str(server) for server in config["mcpServers"].values()):
                            print("✓ Office Assistant server is configured")
                        else:
                            print("✗ Office Assistant server is NOT configured in MCP client")
            except Exception as e:
                print(f"⚠ Could not parse config: {e}")
    
    if not config_found:
        print("✗ No MCP client configuration found")
        print("  You need to configure the MCP server in your MCP client (e.g., Claude Desktop)")
    
    return config_found

def test_stdio_communication():
    """Test if stdio communication works."""
    print("\n=== Testing STDIO Communication ===")
    
    print(f"stdin type: {type(sys.stdin)}")
    print(f"stdin.buffer type: {type(sys.stdin.buffer)}")
    print(f"stdin is a tty: {sys.stdin.isatty()}")
    print(f"stdout is a tty: {sys.stdout.isatty()}")
    
    if sys.stdin.isatty():
        print("⚠ Running from terminal - stdio will not work as expected")
        print("  MCP servers must be run by an MCP client, not directly")
    else:
        print("✓ Not running from terminal - stdio should work")

async def test_server_import():
    """Test if the server can be imported."""
    print("\n=== Testing Server Import ===")
    
    try:
        from main import OfficeAssistantServer
        print("✓ Server import successful")
        
        # Try to create server instance
        server = OfficeAssistantServer()
        print("✓ Server instance created")
        
        # Check handlers
        print(f"  Handlers loaded: {len(server.handlers)}")
        print(f"  Tools available: {len(server.tool_handlers)}")
        
        return True
    except Exception as e:
        print(f"✗ Server import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostics."""
    print("MCP Office Assistant Server Diagnostics")
    print("=" * 40)
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Check FPDF specifically
    fpdf_ok = check_fpdf_version()
    
    # Check environment
    missing_env = check_environment()
    
    # Check MCP client config
    config_exists = check_mcp_client_config()
    
    # Test stdio
    test_stdio_communication()
    
    # Test server import
    asyncio.run(test_server_import())
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    
    if missing_deps:
        print(f"✗ Missing dependencies: {', '.join(missing_deps)}")
        print("  Run: pip install -r requirements.txt")
    else:
        print("✓ All dependencies installed")
    
    if not fpdf_ok:
        print("✗ FPDF issues detected")
    else:
        print("✓ FPDF working correctly")
    
    if missing_env:
        print(f"✗ Missing environment variables: {', '.join(missing_env)}")
        print("  Copy .env.example to .env and fill in values")
    else:
        print("✓ All environment variables set")
    
    if not config_exists:
        print("✗ MCP client not configured")
        print("  Configure the server in your MCP client")
    else:
        print("✓ MCP client configuration found")
    
    if sys.stdin.isatty():
        print("⚠ Running from terminal - use MCP client instead")
    
    print("\nFor more information, see integration_guide.md")

if __name__ == "__main__":
    main()