#!/usr/bin/env python3
"""
Minimal MCP Server Test
=======================

Tests the bare minimum MCP server setup to isolate the issue.
"""

import asyncio
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

async def main():
    """Test minimal MCP server."""
    try:
        logger.info("Testing minimal MCP server...")
        
        # Import MCP components
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        
        # Create minimal server
        server = Server("test-server")
        
        # Log server info
        logger.info(f"Server created: {server}")
        logger.info(f"Server name: {server.name}")
        
        # Check run method
        import inspect
        run_sig = inspect.signature(server.run)
        logger.info(f"Server.run signature: {run_sig}")
        logger.info(f"Server.run parameters: {list(run_sig.parameters.keys())}")
        
        # Try different approaches
        options = InitializationOptions(
            server_name="test-server",
            server_version="1.0.0",
            capabilities={"tools": {}}
        )
        
        # Check if run expects no parameters (newer API)
        if not run_sig.parameters:
            logger.info("Attempting to run with no parameters...")
            await server.run()
        else:
            logger.info("Attempting to run with stdio streams...")
            # Try with initialization_options only
            if 'initialization_options' in run_sig.parameters and len(run_sig.parameters) == 1:
                await server.run(initialization_options=options)
            else:
                # Try with streams
                await server.run(
                    read_stream=sys.stdin.buffer,
                    write_stream=sys.stdout.buffer,
                    initialization_options=options
                )
        
    except Exception as e:
        logger.error(f"Error: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        
        # Try to understand the error better
        if "BufferedReader" in str(e):
            logger.error("\nThe issue is with BufferedReader not supporting async context manager.")
            logger.error("This suggests the MCP library expects different stream types.")
            logger.error("\nPossible solutions:")
            logger.error("1. The MCP library might need async streams, not sync BufferedReader")
            logger.error("2. There might be a helper function to wrap stdio properly")
            logger.error("3. The server might need to be initialized differently")

if __name__ == "__main__":
    logger.info("Starting test...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"stdin.isatty(): {sys.stdin.isatty()}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Test interrupted")
    except Exception as e:
        logger.error(f"Test failed: {e}")