#!/usr/bin/env python3
"""
MCP Server Runner with Proper STDIO
===================================

This script runs the MCP server using the SDK's built-in stdio handling.
"""

import asyncio
import logging
import sys

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point."""
    try:
        # Import MCP SDK stdio handler
        from mcp.server.stdio import stdio_server
        from main import OfficeAssistantServer
        
        logger.info("Starting MCP Office Assistant Server with SDK stdio...")
        
        # Create server instance
        server = OfficeAssistantServer()
        
        # Use the SDK's stdio_server
        async with stdio_server() as streams:
            # The stdio_server provides the proper stream types
            await server.server.run(*streams)
            
    except ImportError as e:
        logger.error(f"Import error: {e}")
        
        # Try alternative approach
        try:
            from mcp import run_stdio_server
            from main import OfficeAssistantServer
            
            logger.info("Using alternative stdio approach...")
            server = OfficeAssistantServer()
            
            # Use the convenience function if available
            await run_stdio_server(server.server)
            
        except ImportError:
            logger.error("No stdio helpers found in MCP SDK")
            logger.error("Falling back to direct approach...")
            
            from main import OfficeAssistantServer
            server = OfficeAssistantServer()
            await server.run()
            
    except Exception as e:
        logger.error(f"Server error: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    if sys.stdin.isatty():
        print("WARNING: This MCP server should be run by an MCP client.", file=sys.stderr)
        print("\nUsage:", file=sys.stderr)
        print("  MCP Inspector: npx @modelcontextprotocol/inspector python run_mcp_stdio.py", file=sys.stderr)
        print("  Claude Desktop: Configure in settings", file=sys.stderr)
        print("\nPress Ctrl+C to exit.\n", file=sys.stderr)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)