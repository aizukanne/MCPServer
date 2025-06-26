#!/usr/bin/env python3
"""
Proper MCP Server Runner
========================

This script properly runs the MCP server with stdio communication.
MCP servers are designed to be launched by MCP clients, not run directly.
"""

import asyncio
import logging
import sys
import os

# Configure logging to stderr so it doesn't interfere with stdio protocol
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

async def run_server():
    """Run the MCP server properly."""
    try:
        # Import after logging is configured
        from main import OfficeAssistantServer
        
        logger.info("Starting MCP Office Assistant Server...")
        logger.info("Note: This server expects to communicate via stdio with an MCP client")
        
        # Create and run the server
        server = OfficeAssistantServer()
        await server.run()
        
    except Exception as e:
        logger.error(f"Server error: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)

def main():
    """Main entry point."""
    # Check if we're being run directly
    if sys.stdin.isatty():
        print("WARNING: This MCP server is designed to be run by an MCP client,", file=sys.stderr)
        print("not directly from the terminal.", file=sys.stderr)
        print("\nTo use this server:", file=sys.stderr)
        print("1. Install an MCP client (like Claude Desktop)", file=sys.stderr)
        print("2. Configure the client to use this server", file=sys.stderr)
        print("3. The client will launch this server and communicate via stdio", file=sys.stderr)
        print("\nFor testing, you can still run it, but expect errors about", file=sys.stderr)
        print("missing protocol messages on stdin.", file=sys.stderr)
        print("\nPress Ctrl+C to exit.\n", file=sys.stderr)
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()