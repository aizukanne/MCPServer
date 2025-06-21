"""
Response Formatting Utilities
=============================

This module provides utilities for formatting MCP responses consistently.
"""

import json
import traceback
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Union


def decimal_default(obj: Any) -> Any:
    """JSON serializer for Decimal objects."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def format_success_response(result: Any) -> str:
    """
    Format a successful tool execution result.
    
    Args:
        result: The result to format
        
    Returns:
        Formatted JSON string
    """
    try:
        # Handle different result types
        if isinstance(result, str):
            # If it's already a string, check if it's valid JSON
            try:
                json.loads(result)
                return result
            except json.JSONDecodeError:
                # Not JSON, wrap it
                response = {
                    "status": "success",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
        elif isinstance(result, dict):
            # If it's a dict, add metadata if not present
            if "status" not in result:
                response = {
                    "status": "success",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            else:
                response = result
        elif isinstance(result, list):
            response = {
                "status": "success",
                "data": result,
                "count": len(result),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            response = {
                "status": "success",
                "data": result,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting response: {str(e)}")


def format_error_response(error: Union[str, Exception], include_traceback: bool = False) -> str:
    """
    Format an error response.
    
    Args:
        error: The error message or exception
        include_traceback: Whether to include full traceback
        
    Returns:
        Formatted JSON string
    """
    try:
        if isinstance(error, Exception):
            error_message = str(error)
            error_type = type(error).__name__
        else:
            error_message = str(error)
            error_type = "Error"
        
        response = {
            "status": "error",
            "error": {
                "type": error_type,
                "message": error_message
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if include_traceback and isinstance(error, Exception):
            response["error"]["traceback"] = traceback.format_exc()
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        # Fallback error formatting
        return json.dumps({
            "status": "error",
            "error": {
                "type": "FormattingError",
                "message": f"Error formatting error response: {str(e)}"
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }, indent=2)


def format_validation_error(errors: List[str]) -> str:
    """
    Format validation errors.
    
    Args:
        errors: List of validation error messages
        
    Returns:
        Formatted JSON string
    """
    response = {
        "status": "error",
        "error": {
            "type": "ValidationError",
            "message": "Input validation failed",
            "details": errors
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return json.dumps(response, indent=2)


def format_weather_response(weather_data: Dict[str, Any]) -> str:
    """Format weather data response."""
    if isinstance(weather_data, str):
        # Error message
        return format_error_response(weather_data)
    
    try:
        current = weather_data.get("current", {})
        
        formatted = {
            "status": "success",
            "data": {
                "temperature": f"{current.get('temp', 'N/A')}°C",
                "feels_like": f"{current.get('feels_like', 'N/A')}°C",
                "humidity": f"{current.get('humidity', 'N/A')}%",
                "pressure": f"{current.get('pressure', 'N/A')} hPa",
                "visibility": f"{current.get('visibility', 'N/A')} km",
                "uv_index": current.get('uvi', 'N/A'),
                "wind_speed": f"{current.get('wind_speed', 'N/A')} m/s",
                "wind_direction": f"{current.get('wind_deg', 'N/A')}°",
                "weather": current.get('weather', [{}])[0].get('description', 'N/A'),
                "timestamp": datetime.fromtimestamp(current.get('dt', 0)).isoformat() if current.get('dt') else None
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return json.dumps(formatted, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting weather data: {str(e)}")


def format_web_content_response(web_content: List[Dict[str, Any]]) -> str:
    """Format web browsing response."""
    try:
        formatted_content = []
        
        for item in web_content:
            if item.get("type") == "text":
                text_data = item.get("text", {})
                if isinstance(text_data, dict):
                    if "error" in text_data:
                        formatted_content.append({
                            "type": "error",
                            "url": text_data.get("url", "unknown"),
                            "error": text_data["error"]
                        })
                    else:
                        formatted_content.append({
                            "type": "content",
                            "url": text_data.get("url", "unknown"),
                            "summary": text_data.get("summary_or_full_text", ""),
                            "author": text_data.get("author", "Unknown"),
                            "date_published": text_data.get("date_published", "Unknown"),
                            "s3_url": text_data.get("s3_url")
                        })
                else:
                    formatted_content.append({
                        "type": "content",
                        "data": text_data
                    })
            elif item.get("type") == "image_url":
                formatted_content.append({
                    "type": "image",
                    "url": item.get("image_url", {}).get("url", "")
                })
        
        response = {
            "status": "success",
            "data": {
                "content": formatted_content,
                "total_items": len(formatted_content)
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting web content: {str(e)}")


def format_search_response(search_results: Any) -> str:
    """Format Google search response."""
    try:
        if isinstance(search_results, list):
            # Web content format
            return format_web_content_response(search_results)
        elif isinstance(search_results, str):
            # Error or simple response
            try:
                parsed = json.loads(search_results)
                return format_success_response(parsed)
            except json.JSONDecodeError:
                return format_success_response(search_results)
        else:
            return format_success_response(search_results)
            
    except Exception as e:
        return format_error_response(f"Error formatting search results: {str(e)}")


def format_database_response(data: Any, operation: str = "query") -> str:
    """Format database operation response."""
    try:
        if data is None:
            response = {
                "status": "success",
                "data": None,
                "operation": operation,
                "message": "No data found",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        elif isinstance(data, list):
            response = {
                "status": "success",
                "data": data,
                "operation": operation,
                "count": len(data),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            response = {
                "status": "success",
                "data": data,
                "operation": operation,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting database response: {str(e)}")


def format_file_operation_response(result: Any, operation: str = "file_operation") -> str:
    """Format file operation response."""
    try:
        if isinstance(result, str):
            # Check if it's a status message
            if result.startswith("Success:") or result.startswith("Failure:"):
                success = result.startswith("Success:")
                message = result.split(":", 1)[1].strip() if ":" in result else result
                
                response = {
                    "status": "success" if success else "error",
                    "operation": operation,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            else:
                response = {
                    "status": "success",
                    "operation": operation,
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
        else:
            response = {
                "status": "success",
                "operation": operation,
                "data": result,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting file operation response: {str(e)}")


def format_amazon_products_response(products_data: Any) -> str:
    """Format Amazon products search response."""
    try:
        if isinstance(products_data, str):
            # Formatted string response
            response = {
                "status": "success",
                "data": {
                    "formatted_results": products_data
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        elif isinstance(products_data, dict):
            if products_data.get("status") == "ERROR":
                return format_error_response(products_data.get("message", "Amazon search failed"))
            
            # Raw API response
            data = products_data.get("data", {})
            products = data.get("products", [])
            
            formatted_products = []
            for product in products:
                formatted_products.append({
                    "title": product.get("product_title", ""),
                    "price": product.get("product_price", ""),
                    "rating": product.get("product_star_rating", ""),
                    "num_ratings": product.get("product_num_ratings", 0),
                    "url": product.get("product_url", ""),
                    "is_best_seller": product.get("is_best_seller", False),
                    "is_amazon_choice": product.get("is_amazon_choice", False),
                    "delivery": product.get("delivery", "")
                })
            
            response = {
                "status": "success",
                "data": {
                    "total_products": data.get("total_products", 0),
                    "products": formatted_products,
                    "query_info": {
                        "search_query": data.get("search_query", ""),
                        "country": data.get("country", "")
                    }
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            response = {
                "status": "success",
                "data": products_data,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting Amazon products response: {str(e)}")


def format_odoo_response(odoo_data: Any, operation: str = "odoo_operation") -> str:
    """Format Odoo operation response."""
    try:
        if isinstance(odoo_data, dict) and "error" in odoo_data:
            return format_error_response(odoo_data["error"])
        
        response = {
            "status": "success",
            "operation": operation,
            "data": odoo_data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting Odoo response: {str(e)}")


def format_math_response(math_result: Dict[str, Any]) -> str:
    """Format mathematical calculation response."""
    try:
        if math_result.get("status") == "error":
            return format_error_response(math_result.get("message", "Math calculation failed"))
        
        response = {
            "status": "success",
            "operation": "mathematical_calculation",
            "data": {
                "execution_status": math_result.get("status"),
                "result": math_result.get("result", {}),
                "variables": list(math_result.get("result", {}).keys()) if isinstance(math_result.get("result"), dict) else []
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting math response: {str(e)}")


def format_openai_response(openai_result: Any) -> str:
    """Format OpenAI API response."""
    try:
        if openai_result is None:
            return format_error_response("OpenAI request failed")
        
        # Parse JSON if it's a string
        if isinstance(openai_result, str):
            try:
                parsed_result = json.loads(openai_result)
            except json.JSONDecodeError:
                parsed_result = openai_result
        else:
            parsed_result = openai_result
        
        response = {
            "status": "success",
            "operation": "openai_query",
            "data": {
                "response": parsed_result
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return json.dumps(response, default=decimal_default, indent=2)
        
    except Exception as e:
        return format_error_response(f"Error formatting OpenAI response: {str(e)}")


def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def format_summary(data: Any, title: str = "Summary") -> str:
    """
    Format data as a summary.
    
    Args:
        data: Data to summarize
        title: Summary title
        
    Returns:
        Formatted summary string
    """
    try:
        summary_lines = [f"## {title}", ""]
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    summary_lines.append(f"**{key}**: {type(value).__name__} with {len(value)} items")
                else:
                    summary_lines.append(f"**{key}**: {value}")
        elif isinstance(data, list):
            summary_lines.append(f"List with {len(data)} items")
            for i, item in enumerate(data[:5]):  # Show first 5 items
                if isinstance(item, dict):
                    summary_lines.append(f"{i+1}. {type(item).__name__} with {len(item)} properties")
                else:
                    summary_lines.append(f"{i+1}. {truncate_text(str(item), 100)}")
            if len(data) > 5:
                summary_lines.append(f"... and {len(data) - 5} more items")
        else:
            summary_lines.append(truncate_text(str(data), 500))
        
        return "\n".join(summary_lines)
        
    except Exception as e:
        return f"Error creating summary: {str(e)}"