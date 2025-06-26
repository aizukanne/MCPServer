#!/usr/bin/env python3
"""
STDIO Wrapper for MCP
=====================

Provides async-compatible wrappers for stdio streams.
"""

import asyncio
import sys
from typing import AsyncIterator, Optional

class AsyncStdioReader:
    """Async wrapper for stdin that supports async context manager protocol."""
    
    def __init__(self, stream):
        self.stream = stream
        self.reader = None
        
    async def __aenter__(self):
        """Enter async context."""
        loop = asyncio.get_event_loop()
        self.reader = asyncio.StreamReader()
        
        # Create protocol
        protocol = asyncio.StreamReaderProtocol(self.reader)
        
        # Connect stdin to async reader
        await loop.connect_read_pipe(lambda: protocol, self.stream)
        
        return self.reader
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        # Cleanup if needed
        pass

class AsyncStdioWriter:
    """Async wrapper for stdout that supports async context manager protocol."""
    
    def __init__(self, stream):
        self.stream = stream
        self.writer = None
        
    async def __aenter__(self):
        """Enter async context."""
        loop = asyncio.get_event_loop()
        
        # Create transport and protocol
        transport, protocol = await loop.connect_write_pipe(
            lambda: asyncio.Protocol(), 
            self.stream
        )
        
        # Create StreamWriter
        self.writer = asyncio.StreamWriter(transport, protocol, None, loop)
        
        return self.writer
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

async def create_async_stdio_streams():
    """Create async-compatible stdio streams."""
    reader = AsyncStdioReader(sys.stdin.buffer)
    writer = AsyncStdioWriter(sys.stdout.buffer)
    
    async with reader as read_stream, writer as write_stream:
        return read_stream, write_stream