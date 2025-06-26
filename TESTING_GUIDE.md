# MCP Server Testing Guide

## Overview

The MCP server has been fixed to work properly with the MCP Python SDK v1.9.4. The key issue was that we were trying to call `server.run()` directly with stdio streams, but the MCP SDK expects to handle the stdio setup itself.

## What Was Fixed

1. **Removed direct server.run() calls** - The MCP SDK handles this internally
2. **Created proper entry points** that use `mcp.server.stdio.run_stdio_server()`
3. **Fixed Python version requirements** to >=3.10 (required by MCP)
4. **Fixed FPDF version** to 1.7.2

## How to Test

### Option 1: Using index.py (Recommended)

```bash
HOST=0.0.0.0 ALLOWED_ORIGINS=http://10.192.231.192:6274 npx @modelcontextprotocol/inspector .venv/bin/python index.py
```

### Option 2: Using __main__.py

```bash
HOST=0.0.0.0 ALLOWED_ORIGINS=http://10.192.231.192:6274 npx @modelcontextprotocol/inspector .venv/bin/python __main__.py
```

### Option 3: Using mcp_run.py

```bash
HOST=0.0.0.0 ALLOWED_ORIGINS=http://10.192.231.192:6274 npx @modelcontextprotocol/inspector .venv/bin/python mcp_run.py
```

## What Should Happen

1. The server should start without the `BufferedReader` error
2. You should see log messages about the server starting
3. The MCP Inspector web interface should show your available tools
4. You should be able to test the tools through the Inspector

## If You Still Get Errors

1. **Check mcp.server.stdio exists**:
   ```bash
   .venv/bin/python -c "import mcp.server.stdio; print(dir(mcp.server.stdio))"
   ```

2. **Verify MCP version**:
   ```bash
   .venv/bin/pip show mcp
   ```

3. **Check Python version**:
   ```bash
   .venv/bin/python --version
   ```
   Should be 3.10 or higher.

## Understanding the Fix

The MCP Python SDK expects to:
1. Handle stdio communication itself
2. Convert stdio to the `MemoryObjectStream` types it needs internally
3. Manage the async context managers

By using `mcp.server.stdio.run_stdio_server()`, we let the SDK handle all of this complexity.

## Files to Use

- **index.py** - Main entry point (recommended)
- **__main__.py** - Package entry point
- **mcp_run.py** - Alternative entry point

## Files to Ignore

These were created during debugging and can be ignored:
- run_mcp_server.py (old approach)
- stdio_wrapper.py (not needed)
- All test_*.py files
- mcp_server_*.py files

## Next Steps

1. Test with one of the entry points above
2. If successful, clean up the extra files
3. Update your MCP client configuration to use the working entry point