#!/usr/bin/env python3
"""
Alternative MCP Server Runner
=============================

This script uses the standard MCP pattern for running servers.
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
    """Main entry point using standard MCP pattern."""
    try:
        # Import after logging is configured
        from main import OfficeAssistantServer
        from mcp import stdio_server
        
        logger.info("Starting MCP Office Assistant Server (Alternative)...")
        
        # Create server instance
        server = OfficeAssistantServer()
        
        # Use MCP's stdio_server helper
        async with stdio_server() as streams:
            logger.info("Running server with MCP stdio helper...")
            await server.server.run(*streams)
            
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Trying direct approach...")
        
        # Fallback to direct approach
        from main import OfficeAssistantServer
        server = OfficeAssistantServer()
        await server.run()
        
    except Exception as e:
        logger.error(f"Server error: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if we're being run directly
    if sys.stdin.isatty():
        print("WARNING: This MCP server is designed to be run by an MCP client,", file=sys.stderr)
        print("not directly from the terminal.", file=sys.stderr)
        print("\nTo use this server:", file=sys.stderr)
        print("1. Install an MCP client (like Claude Desktop)", file=sys.stderr)
        print("2. Configure the client to use this server", file=sys.stderr)
        print("3. The client will launch this server and communicate via stdio", file=sys.stderr)
        print("\nFor testing with MCP Inspector:", file=sys.stderr)
        print("npx @modelcontextprotocol/inspector python run_mcp_server_alt.py", file=sys.stderr)
        print("\nPress Ctrl+C to exit.\n", file=sys.stderr)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)