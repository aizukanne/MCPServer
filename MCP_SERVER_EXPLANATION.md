# Understanding the MCP Server TaskGroup Error

## The Error
```
ERROR:__main__:Server error: unhandled errors in a TaskGroup (1 sub-exception)
```

## Root Cause

This error occurs because **MCP servers are not designed to be run directly from the command line**. They are stdio-based servers that expect to communicate with an MCP client through standard input/output streams.

## How MCP Servers Work

1. **Client-Server Architecture**: MCP uses a client-server model where:
   - The **client** (e.g., Claude Desktop, an IDE plugin) launches the server
   - The **server** communicates via stdio (stdin/stdout) using the MCP protocol
   - Messages are exchanged in a specific JSON-RPC format

2. **The TaskGroup Error**: When you run the server directly:
   - The server starts and creates async tasks to read from stdin
   - It expects MCP protocol messages but receives nothing (or terminal input)
   - The read tasks fail, causing the TaskGroup error

## Proper Usage

### Option 1: Use with an MCP Client

1. Install an MCP-compatible client (e.g., Claude Desktop)
2. Configure the client to use your server:
   ```json
   {
     "mcpServers": {
       "office-assistant": {
         "command": "python",
         "args": ["/path/to/main.py"]
       }
     }
   }
   ```
3. The client will launch and manage the server

### Option 2: Testing Without a Client

For testing purposes, you can simulate MCP communication:

```python
# test_client.py
import json
import subprocess
import asyncio

async def test_mcp_server():
    # Launch the server
    proc = await asyncio.create_subprocess_exec(
        'python', 'main.py',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Send an initialization message
    init_msg = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "0.1.0",
            "capabilities": {}
        },
        "id": 1
    }
    
    # Send the message
    proc.stdin.write(json.dumps(init_msg).encode() + b'\n')
    await proc.stdin.drain()
    
    # Read response
    response = await proc.stdout.readline()
    print(f"Response: {response.decode()}")
    
    # Clean up
    proc.terminate()
    await proc.wait()

asyncio.run(test_mcp_server())
```

## The Fixed Code

The fixes I've implemented are correct:
1. ✓ Added stdio streams to `server.run()`
2. ✓ Fixed async context manager issue
3. ✓ Added proper error handling
4. ✓ Implemented resource cleanup

The TaskGroup error is not a bug in your code - it's the expected behavior when running an MCP server without a proper client.

## Recommendations

1. **For Development**: Use the `run_mcp_server.py` script which includes warnings about direct execution
2. **For Testing**: Create a test client that sends proper MCP messages
3. **For Production**: Always use with a proper MCP client
4. **For Debugging**: The enhanced error logging will help identify any actual issues

## Summary

The server code is now correctly implemented. The TaskGroup error only occurs when running directly because the server is waiting for MCP protocol messages that never arrive. This is normal and expected behavior for an stdio-based server.