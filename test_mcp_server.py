#!/usr/bin/env python3
"""Test script to diagnose MCP server issues."""

import asyncio
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def test_basic_server():
    """Test basic MCP server functionality."""
    logger.info("Testing basic MCP server setup...")
    
    try:
        # Test importing MCP modules
        logger.info("Importing MCP modules...")
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        logger.info("✓ MCP modules imported successfully")
        
        # Test creating server instance
        logger.info("Creating server instance...")
        server = Server("test-server")
        logger.info("✓ Server instance created")
        
        # Test initialization options
        logger.info("Creating initialization options...")
        options = InitializationOptions(
            server_name="test-server",
            server_version="1.0.0",
            capabilities={
                "tools": {}
            }
        )
        logger.info("✓ Initialization options created")
        
        # Check if we're in a proper stdio environment
        logger.info("Checking stdio environment...")
        if hasattr(sys.stdin, 'buffer'):
            logger.info("✓ stdin.buffer available")
        else:
            logger.error("✗ stdin.buffer not available")
            
        if hasattr(sys.stdout, 'buffer'):
            logger.info("✓ stdout.buffer available")
        else:
            logger.error("✗ stdout.buffer not available")
            
        # Test if we can access the streams
        logger.info("Testing stream access...")
        try:
            read_stream = sys.stdin.buffer
            write_stream = sys.stdout.buffer
            logger.info("✓ Streams accessible")
        except Exception as e:
            logger.error(f"✗ Error accessing streams: {e}")
            
        return True
        
    except Exception as e:
        logger.error(f"✗ Test failed: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return False

async def test_handler_imports():
    """Test if all handlers can be imported."""
    logger.info("\nTesting handler imports...")
    
    handlers = [
        "handlers.weather",
        "handlers.web_browsing", 
        "handlers.storage",
        "handlers.slack_integration",
        "handlers.odoo",
        "handlers.amazon",
        "handlers.documents",
        "handlers.utilities"
    ]
    
    all_good = True
    for handler in handlers:
        try:
            __import__(handler)
            logger.info(f"✓ {handler} imported successfully")
        except Exception as e:
            logger.error(f"✗ Failed to import {handler}: {e}")
            all_good = False
            
    return all_good

async def test_minimal_server():
    """Test a minimal MCP server setup."""
    logger.info("\nTesting minimal server setup...")
    
    try:
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        
        # Create minimal server
        server = Server("minimal-test")
        
        # Set up a simple handler
        @server.list_tools()
        async def handle_list_tools():
            return []
            
        logger.info("✓ Minimal server setup complete")
        
        # Don't actually run the server, just test setup
        return True
        
    except Exception as e:
        logger.error(f"✗ Minimal server test failed: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return False

async def main():
    """Run all tests."""
    logger.info("Starting MCP Server diagnostics...\n")
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    
    # Check if we're running in a terminal
    logger.info(f"Is TTY: {sys.stdin.isatty()}")
    logger.info(f"Environment: {os.environ.get('TERM', 'Not set')}")
    
    tests = [
        test_basic_server,
        test_handler_imports,
        test_minimal_server
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
        
    # Summary
    logger.info("\n" + "="*50)
    logger.info("DIAGNOSTIC SUMMARY")
    logger.info("="*50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        logger.info(f"✓ All tests passed ({passed}/{total})")
    else:
        logger.error(f"✗ Some tests failed ({passed}/{total} passed)")
        
    # Additional info
    logger.info("\nNOTE: MCP servers are designed to run as stdio servers.")
    logger.info("They expect to be launched by an MCP client that provides")
    logger.info("the stdin/stdout streams for communication.")
    logger.info("\nIf running directly, you may see TaskGroup errors because")
    logger.info("the server is trying to read from stdin which may not have")
    logger.info("the expected MCP protocol messages.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))