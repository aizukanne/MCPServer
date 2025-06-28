# Adding New Tools

This guide explains how to add new tools to the MCP Office Assistant Server.

## 1. Define the Schema

First, define the input and output schemas for your new tool in `schemas/tool_schemas.py`. This ensures that all data passed to and from your tool is properly validated.

## 2. Create a Handler

Next, create a handler function in the appropriate handler module within the `handlers/` directory. This function will be responsible for receiving requests from the MCP server and calling the corresponding service.

## 3. Implement the Service Logic

Implement the core logic for your tool in a new function within the corresponding service module in the `services/` directory. This is where the actual work of the tool is performed.

## 4. Add the Tool Routing

Finally, add the tool routing in `main.py` to connect the tool name to its handler function. This makes the tool accessible to the MCP server.