"""
Lambda Handler Functions for MCP Office Assistant
=================================================

Main Lambda functions for handling MCP tool requests via API Gateway.
"""

import json
import logging
import os
import traceback
from typing import Any, Dict

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Import handlers (these will be in the Lambda package)
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
from utils.formatting import format_error_response


def create_response(status_code: int, body: Any, headers: Dict[str, str] = None) -> Dict[str, Any]:
    """Create API Gateway response."""
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body) if not isinstance(body, str) else body
    }


def extract_project_id(event: Dict[str, Any]) -> str:
    """Extract project ID from API key or headers."""
    # Try to get project ID from headers first
    headers = event.get('headers', {})
    project_id = headers.get('X-Project-ID') or headers.get('x-project-id')
    
    if project_id:
        return project_id
    
    # Fallback: extract from API key context (if available)
    request_context = event.get('requestContext', {})
    identity = request_context.get('identity', {})
    api_key_id = identity.get('apiKeyId')
    
    if api_key_id:
        # Map API key IDs to project names
        # This would be populated from CloudFormation outputs or Parameter Store
        api_key_mapping = {
            # These would be populated dynamically
        }
        return api_key_mapping.get(api_key_id, 'default')
    
    return 'default'


def list_tools_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for listing available MCP tools.
    
    GET /tools
    """
    try:
        logger.info("Listing available tools")
        
        # Get project ID for potential customization
        project_id = extract_project_id(event)
        logger.info(f"Request from project: {project_id}")
        
        # Get all tool schemas
        tool_schemas = get_all_tool_schemas()
        
        # Format tools list
        tools = []
        for tool_name, schema in tool_schemas.items():
            tools.append({
                'name': schema['name'],
                'description': schema['description'],
                'inputSchema': schema['inputSchema']
            })
        
        response_body = {
            'status': 'success',
            'tools': tools,
            'total_tools': len(tools),
            'project_id': project_id
        }
        
        logger.info(f"Listed {len(tools)} tools successfully")
        return create_response(200, response_body)
        
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        logger.error(traceback.format_exc())
        
        error_response = {
            'status': 'error',
            'error': {
                'type': 'InternalError',
                'message': 'Failed to list tools'
            }
        }
        return create_response(500, error_response)


def tool_executor_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for executing MCP tools.
    
    POST /tools/{tool_name}
    """
    try:
        # Extract tool name from path
        path_params = event.get('pathParameters', {})
        tool_name = path_params.get('tool_name')
        
        if not tool_name:
            return create_response(400, {
                'status': 'error',
                'error': {
                    'type': 'BadRequest',
                    'message': 'Tool name is required'
                }
            })
        
        # Extract arguments from body
        body = event.get('body', '{}')
        if isinstance(body, str):
            try:
                arguments = json.loads(body)
            except json.JSONDecodeError:
                return create_response(400, {
                    'status': 'error',
                    'error': {
                        'type': 'BadRequest',
                        'message': 'Invalid JSON in request body'
                    }
                })
        else:
            arguments = body or {}
        
        # Get project ID
        project_id = extract_project_id(event)
        
        logger.info(f"Executing tool: {tool_name} for project: {project_id}")
        logger.info(f"Arguments: {arguments}")
        
        # Validate tool exists
        tool_schemas = get_all_tool_schemas()
        if tool_name not in tool_schemas:
            return create_response(404, {
                'status': 'error',
                'error': {
                    'type': 'NotFound',
                    'message': f'Tool {tool_name} not found'
                }
            })
        
        # Validate arguments
        schema = tool_schemas[tool_name]
        validation_result = validate_tool_arguments(arguments, schema['inputSchema'])
        
        if not validation_result['valid']:
            return create_response(400, {
                'status': 'error',
                'error': {
                    'type': 'ValidationError',
                    'message': 'Invalid arguments',
                    'details': validation_result['errors']
                }
            })
        
        # Add project context to arguments
        arguments['_project_id'] = project_id
        arguments['_lambda_context'] = {
            'function_name': context.function_name,
            'request_id': context.aws_request_id
        }
        
        # Route to appropriate handler and execute
        result = route_and_execute_tool(tool_name, arguments)
        
        logger.info(f"Tool {tool_name} executed successfully")
        
        # Parse result if it's a JSON string
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                # If it's not valid JSON, wrap it
                result = {
                    'status': 'success',
                    'data': result
                }
        
        return create_response(200, result)
        
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        logger.error(traceback.format_exc())
        
        error_response = {
            'status': 'error',
            'error': {
                'type': 'InternalError',
                'message': f'Failed to execute tool: {str(e)}'
            }
        }
        return create_response(500, error_response)


def route_and_execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Any:
    """Route tool execution to appropriate handler."""
    
    # Initialize handlers
    handlers = {
        'weather': WeatherHandler(),
        'web_browsing': WebBrowsingHandler(),
        'storage': StorageHandler(),
        'slack': SlackHandler(),
        'odoo': OdooHandler(),
        'amazon': AmazonHandler(),
        'documents': DocumentHandler(),
        'utilities': UtilitiesHandler(),
    }
    
    # Weather tools
    if tool_name == "get_weather_data":
        return handlers['weather'].get_weather_data(
            arguments.get("location_name", "Whitehorse")
        )
    elif tool_name == "get_coordinates":
        return handlers['weather'].get_coordinates(
            arguments["location_name"]
        )
    
    # Web browsing tools
    elif tool_name == "google_search":
        return handlers['web_browsing'].google_search(
            search_term=arguments["search_term"],
            before=arguments.get("before"),
            after=arguments.get("after"),
            intext=arguments.get("intext"),
            allintext=arguments.get("allintext"),
            and_condition=arguments.get("and_condition"),
            must_have=arguments.get("must_have")
        )
    elif tool_name == "browse_internet":
        return handlers['web_browsing'].browse_internet(
            urls=arguments["urls"],
            full_text=arguments.get("full_text", False)
        )
    elif tool_name == "shorten_url":
        return handlers['web_browsing'].shorten_url(
            url=arguments["url"],
            custom_code=arguments.get("custom_code")
        )
    
    # Storage tools
    elif tool_name == "get_message_by_sort_id":
        return handlers['storage'].get_message_by_sort_id(
            role=arguments["role"],
            chat_id=arguments["chat_id"],
            sort_id=arguments["sort_id"]
        )
    elif tool_name == "get_messages_in_range":
        return handlers['storage'].get_messages_in_range(
            chat_id=arguments["chat_id"],
            start_sort_id=arguments["start_sort_id"],
            end_sort_id=arguments["end_sort_id"]
        )
    elif tool_name == "get_users":
        return handlers['storage'].get_users(
            user_id=arguments.get("user_id")
        )
    elif tool_name == "get_channels":
        return handlers['storage'].get_channels(
            id=arguments.get("id")
        )
    elif tool_name == "manage_mute_status":
        return handlers['storage'].manage_mute_status(
            chat_id=arguments["chat_id"],
            status=arguments.get("status")
        )
    
    # Slack tools
    elif tool_name == "send_file_to_slack":
        return handlers['slack'].send_file_to_slack(
            file_path=arguments["file_path"],
            chat_id=arguments["chat_id"],
            title=arguments["title"],
            ts=arguments.get("ts")
        )
    elif tool_name == "update_slack_users":
        return handlers['slack'].update_slack_users()
    elif tool_name == "update_slack_conversations":
        return handlers['slack'].update_slack_conversations()
    
    # Odoo tools
    elif tool_name == "odoo_get_mapped_models":
        return handlers['odoo'].get_mapped_models(
            include_fields=arguments.get("include_fields", True),
            model_name=arguments.get("model_name")
        )
    elif tool_name == "odoo_fetch_records":
        return handlers['odoo'].fetch_records(
            external_model=arguments["external_model"],
            filters=arguments.get("filters")
        )
    elif tool_name == "odoo_create_record":
        return handlers['odoo'].create_record(
            external_model=arguments["external_model"],
            record_data=arguments["record_data"]
        )
    elif tool_name == "odoo_update_record":
        return handlers['odoo'].update_record(
            external_model=arguments["external_model"],
            record_id=arguments["record_id"],
            **{k: v for k, v in arguments.items() 
               if k not in ["external_model", "record_id", "_project_id", "_lambda_context"]}
        )
    elif tool_name == "odoo_delete_record":
        return handlers['odoo'].delete_record(
            external_model=arguments["external_model"],
            record_id=arguments["record_id"]
        )
    elif tool_name == "odoo_print_record":
        return handlers['odoo'].print_record(
            model_name=arguments["model_name"],
            record_id=arguments["record_id"]
        )
    elif tool_name == "odoo_post_record":
        return handlers['odoo'].post_record(
            external_model=arguments["external_model"],
            record_id=arguments["record_id"]
        )
    
    # Amazon tools
    elif tool_name == "search_amazon_products":
        return handlers['amazon'].search_products(
            query=arguments["query"],
            country=arguments.get("country", "CA"),
            page=arguments.get("page", 1),
            sort_by=arguments.get("sort_by", "RELEVANCE"),
            product_condition=arguments.get("product_condition", "NEW"),
            is_prime=arguments.get("is_prime", False),
            deals_and_discounts=arguments.get("deals_and_discounts", "NONE")
        )
    elif tool_name == "search_and_format_products":
        return handlers['amazon'].search_and_format_products(
            query=arguments["query"],
            country=arguments.get("country", "CA"),
            max_products=arguments.get("max_products", 5),
            **{k: v for k, v in arguments.items() 
               if k not in ["query", "country", "max_products", "_project_id", "_lambda_context"]}
        )
    
    # Document tools
    elif tool_name == "send_as_pdf":
        return handlers['documents'].send_as_pdf(
            text=arguments["text"],
            chat_id=arguments["chat_id"],
            title=arguments["title"],
            ts=arguments.get("ts")
        )
    elif tool_name == "list_files":
        return handlers['documents'].list_files(
            folder_prefix=arguments.get("folder_prefix", "uploads")
        )
    elif tool_name == "get_embedding":
        return handlers['documents'].get_embedding(
            text=arguments["text"],
            model=arguments.get("model", "text-embedding-ada-002")
        )
    
    # Utility tools
    elif tool_name == "solve_maths":
        return handlers['utilities'].solve_maths(
            code=arguments["code"],
            **{k: v for k, v in arguments.items() 
               if k not in ["code", "_project_id", "_lambda_context"]}
        )
    elif tool_name == "ask_openai_reasoning":
        return handlers['utilities'].ask_openai_reasoning(
            prompt=arguments["prompt"]
        )
    
    else:
        raise ValueError(f"Unhandled tool: {tool_name}")


# Additional handler for OPTIONS requests (CORS preflight)
def options_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Handle CORS preflight requests."""
    return create_response(200, '', {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Project-ID',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    })