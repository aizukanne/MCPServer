#!/usr/bin/env python3
"""
MCP STDIO Server Runner
=======================

This provides the proper stdio handling for MCP servers.
"""

import asyncio
import sys
import logging
from typing import Any

import anyio
from anyio.streams.memory import MemoryObjectSendStream, MemoryObjectReceiveStream

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

async def stdio_to_memory_streams():
    """
    Create memory object streams that can communicate with stdio.
    This is what MCP servers expect.
    """
    # Create memory object streams
    send_stream, receive_stream = anyio.create_memory_object_stream(max_buffer_size=0)
    
    # Create tasks to bridge stdio <-> memory streams
    async def stdin_to_memory():
        """Read from stdin and send to memory stream."""
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        
        loop = asyncio.get_event_loop()
        await loop.connect_read_pipe(lambda: protocol, sys.stdin.buffer)
        
        while True:
            try:
                # Read a line from stdin
                line = await reader.readline()
                if not line:
                    break
                    
                # Parse as JSON and send to memory stream
                import json
                try:
                    message = json.loads(line.decode())
                    await send_stream.send(message)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from stdin: {line}")
                    
            except Exception as e:
                logger.error(f"Error reading stdin: {e}")
                break
    
    async def memory_to_stdout(recv_stream):
        """Read from memory stream and write to stdout."""
        async with recv_stream:
            async for message in recv_stream:
                try:
                    # Convert to JSON and write to stdout
                    import json
                    line = json.dumps(message) + '\n'
                    sys.stdout.buffer.write(line.encode())
                    sys.stdout.buffer.flush()
                except Exception as e:
                    logger.error(f"Error writing to stdout: {e}")
    
    # Start the bridge tasks
    async with anyio.create_task_group() as tg:
        tg.start_soon(stdin_to_memory)
        tg.start_soon(memory_to_stdout, receive_stream)
        
        # Return the streams for the server to use
        yield receive_stream, send_stream

async def run_mcp_server():
    """Run the MCP server with proper stdio handling."""
    from main import OfficeAssistantServer
    from mcp.server.models import InitializationOptions
    
    logger.info("Starting MCP server with stdio bridge...")
    
    # Create server
    server = OfficeAssistantServer()
    
    # Create memory streams from stdio
    async with stdio_to_memory_streams() as (read_stream, write_stream):
        # Run server with memory streams
        options = InitializationOptions(
            server_name="office-assistant",
            server_version="1.0.0",
            capabilities={"tools": {}}
        )
        
        await server.server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=options
        )

if __name__ == "__main__":
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)