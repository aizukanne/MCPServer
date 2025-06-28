#!/usr/bin/env python3
"""
MCP Office Assistant Server
==========================

Main entry point for the Model Context Protocol (MCP) server that exposes
office assistant functions to AI applications.
"""

import asyncio
import logging
import sys
from typing import Any, Dict, List

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Import all handlers
from handlers.weather import WeatherHandler
from handlers.web_browsing import WebBrowsingHandler
from handlers.storage import StorageHandler
from handlers.slack_integration import SlackHandler
from handlers.odoo import OdooHandler
from handlers.amazon import AmazonHandler
from handlers.documents import DocumentHandler
from handlers.utilities import UtilitiesHandler

# Import schemas
from schemas.tool_schemas import get_all_tool_schemas

# Import utilities
from utils.validation import validate_tool_arguments
from utils.formatting import format_error_response, format_success_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OfficeAssistantServer:
    """Main MCP server for office assistant functions."""
    
    def __init__(self):
        """Initialize the server with all handlers."""
        try:
            logger.info("Initializing MCP Server...")
            self.server = Server("office-assistant")
            logger.info("Server instance created")
            
            self.handlers = self._initialize_handlers()
            logger.info(f"Initialized {len(self.handlers)} handlers")
            
            self.tool_schemas = get_all_tool_schemas()
            logger.info(f"Loaded {len(self.tool_schemas)} tool schemas")
            
            self._setup_handlers()
            logger.info("Handler setup complete")
        except Exception as e:
            logger.error(f"Error during server initialization: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise
    
    def _initialize_handlers(self) -> Dict[str, Any]:
        """Initialize all function handlers."""
        return {
            "weather": WeatherHandler(),
            "web_browsing": WebBrowsingHandler(),
            "storage": StorageHandler(),
            "slack": SlackHandler(),
            "odoo": OdooHandler(),
            "amazon": AmazonHandler(),
            "documents": DocumentHandler(),
            "utilities": UtilitiesHandler(),
        }
    
    def _setup_handlers(self) -> None:
        """Set up MCP request handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools."""
            try:
                tools = []
                for schema in self.tool_schemas.values():
                    tools.append(Tool(
                        name=schema["name"],
                        description=schema["description"],
                        inputSchema=schema["inputSchema"]
                    ))
                logger.info(f"Listed {len(tools)} tools")
                return tools
            except Exception as e:
                logger.error(f"Error listing tools: {e}")
                raise
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str,
            arguments: Dict[str, Any] | None = None
        ) -> List[TextContent]:
            """Handle tool execution requests."""
            try:
                logger.info(f"Calling tool: {name} with arguments: {arguments}")
                
                # Validate tool exists
                if name not in self.tool_schemas:
                    error_msg = f"Unknown tool: {name}"
                    logger.error(error_msg)
                    return [TextContent(
                        type="text",
                        text=format_error_response(error_msg)
                    )]
                
                # Validate arguments
                schema = self.tool_schemas[name]
                validation_result = validate_tool_arguments(
                    arguments or {}, 
                    schema["inputSchema"]
                )
                
                if not validation_result["valid"]:
                    error_msg = f"Invalid arguments: {validation_result['errors']}"
                    logger.error(error_msg)
                    return [TextContent(
                        type="text",
                        text=format_error_response(error_msg)
                    )]
                
                # Route to appropriate handler
                result = await self._route_tool_call(name, arguments or {})
                
                logger.info(f"Tool {name} executed successfully")
                return [TextContent(
                    type="text",
                    text=format_success_response(result)
                )]
                
            except Exception as e:
                error_msg = f"Error executing tool {name}: {str(e)}"
                logger.error(error_msg)
                return [TextContent(
                    type="text",
                    text=format_error_response(error_msg)
                )]
    
    async def _route_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Route tool calls to appropriate handlers."""
        
        # Weather tools
        if tool_name == "get_weather_data":
            return await self.handlers["weather"].get_weather_data(
                arguments.get("location_name", "Whitehorse")
            )
        elif tool_name == "get_coordinates":
            return await self.handlers["weather"].get_coordinates(
                arguments["location_name"]
            )
        
        # Web browsing tools
        elif tool_name == "google_search":
            return await self.handlers["web_browsing"].google_search(
                search_term=arguments["search_term"],
                before=arguments.get("before"),
                after=arguments.get("after"),
                intext=arguments.get("intext"),
                allintext=arguments.get("allintext"),
                and_condition=arguments.get("and_condition"),
                must_have=arguments.get("must_have")
            )
        elif tool_name == "browse_internet":
            return await self.handlers["web_browsing"].browse_internet(
                urls=arguments["urls"],
                full_text=arguments.get("full_text", False)
            )
        elif tool_name == "shorten_url":
            return await self.handlers["web_browsing"].shorten_url(
                url=arguments["url"],
                custom_code=arguments.get("custom_code")
            )
        
        # Storage tools
        elif tool_name == "get_message_by_sort_id":
            return await self.handlers["storage"].get_message_by_sort_id(
                role=arguments["role"],
                chat_id=arguments["chat_id"],
                sort_id=arguments["sort_id"]
            )
        elif tool_name == "get_messages_in_range":
            return await self.handlers["storage"].get_messages_in_range(
                chat_id=arguments["chat_id"],
                start_sort_id=arguments["start_sort_id"],
                end_sort_id=arguments["end_sort_id"]
            )
        elif tool_name == "get_users":
            return await self.handlers["storage"].get_users(
                user_id=arguments.get("user_id")
            )
        elif tool_name == "get_channels":
            return await self.handlers["storage"].get_channels(
                id=arguments.get("id")
            )
        elif tool_name == "manage_mute_status":
            return await self.handlers["storage"].manage_mute_status(
                chat_id=arguments["chat_id"],
                status=arguments.get("status")
            )
        
        # Slack tools
        elif tool_name == "send_file_to_slack":
            return await self.handlers["slack"].send_file_to_slack(
                file_path=arguments["file_path"],
                chat_id=arguments["chat_id"],
                title=arguments["title"],
                ts=arguments.get("ts")
            )
        elif tool_name == "update_slack_users":
            return await self.handlers["slack"].update_slack_users()
        elif tool_name == "update_slack_conversations":
            return await self.handlers["slack"].update_slack_conversations()
        
        # Odoo tools
        elif tool_name == "odoo_get_mapped_models":
            return await self.handlers["odoo"].get_mapped_models(
                include_fields=arguments.get("include_fields", True),
                model_name=arguments.get("model_name")
            )
        elif tool_name == "odoo_fetch_records":
            return await self.handlers["odoo"].fetch_records(
                external_model=arguments["external_model"],
                filters=arguments.get("filters")
            )
        elif tool_name == "odoo_create_record":
            return await self.handlers["odoo"].create_record(
                external_model=arguments["external_model"],
                record_data=arguments["record_data"]
            )
        elif tool_name == "odoo_update_record":
            return await self.handlers["odoo"].update_record(
                external_model=arguments["external_model"],
                record_id=arguments["record_id"],
                **{k: v for k, v in arguments.items() 
                   if k not in ["external_model", "record_id"]}
            )
        elif tool_name == "odoo_delete_record":
            return await self.handlers["odoo"].delete_record(
                external_model=arguments["external_model"],
                record_id=arguments["record_id"]
            )
        elif tool_name == "odoo_print_record":
            return await self.handlers["odoo"].print_record(
                model_name=arguments["model_name"],
                record_id=arguments["record_id"]
            )
        elif tool_name == "odoo_post_record":
            return await self.handlers["odoo"].post_record(
                external_model=arguments["external_model"],
                record_id=arguments["record_id"]
            )
        
        # Amazon tools
        elif tool_name == "search_amazon_products":
            return await self.handlers["amazon"].search_products(
                query=arguments["query"],
                country=arguments.get("country", "CA"),
                page=arguments.get("page", 1),
                sort_by=arguments.get("sort_by", "RELEVANCE"),
                product_condition=arguments.get("product_condition", "NEW"),
                is_prime=arguments.get("is_prime", False),
                deals_and_discounts=arguments.get("deals_and_discounts", "NONE")
            )
        elif tool_name == "search_and_format_products":
            return await self.handlers["amazon"].search_and_format_products(
                query=arguments["query"],
                country=arguments.get("country", "CA"),
                max_products=arguments.get("max_products", 5),
                **{k: v for k, v in arguments.items() 
                   if k not in ["query", "country", "max_products"]}
            )
        
        # Document tools
        elif tool_name == "send_as_pdf":
            return await self.handlers["documents"].send_as_pdf(
                text=arguments["text"],
                chat_id=arguments["chat_id"],
                title=arguments["title"],
                ts=arguments.get("ts")
            )
        elif tool_name == "list_files":
            return await self.handlers["documents"].list_files(
                folder_prefix=arguments.get("folder_prefix", "uploads")
            )
        elif tool_name == "get_embedding":
            return await self.handlers["documents"].get_embedding(
                text=arguments["text"],
                model=arguments.get("model", "text-embedding-ada-002")
            )
        
        # Utility tools
        elif tool_name == "solve_maths":
            return await self.handlers["utilities"].solve_maths(
                code=arguments["code"],
                **{k: v for k, v in arguments.items() if k != "code"}
            )
        elif tool_name == "ask_openai_reasoning":
            return await self.handlers["utilities"].ask_openai_reasoning(
                prompt=arguments["prompt"]
            )
        
        else:
            raise ValueError(f"Unhandled tool: {tool_name}")
    
    def get_server(self) -> Server:
        """Get the MCP server instance."""
        return self.server


# This module should be imported and used by an MCP runner
# It should not be run directly
if __name__ == "__main__":
    logger.error("This module should not be run directly!")
    logger.error("Use one of the MCP server runners instead:")
    logger.error("  - python index.py")
    logger.error("  - python mcp_run.py")
    logger.error("Or run via MCP Inspector:")
    logger.error("  - npx @modelcontextprotocol/inspector python index.py")
    sys.exit(1)