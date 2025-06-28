"""
Tool Schema Definitions
======================

This module contains all the JSON Schema definitions for MCP tools.
Each tool's parameters are defined with proper validation rules.
"""

from typing import Dict, Any


def get_weather_schemas() -> Dict[str, Dict[str, Any]]:
    """Get weather-related tool schemas."""
    return {
        "get_weather_data": {
            "name": "get_weather_data",
            "description": "Get current weather data for a specified location",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location to get weather for",
                        "default": "Whitehorse"
                    }
                },
                "required": []
            }
        },
        "get_coordinates": {
            "name": "get_coordinates",
            "description": "Get latitude and longitude coordinates for a location name",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location to get coordinates for"
                    }
                },
                "required": ["location_name"]
            }
        }
    }


def get_web_browsing_schemas() -> Dict[str, Dict[str, Any]]:
    """Get web browsing tool schemas."""
    return {
        "google_search": {
            "name": "google_search",
            "description": "Perform a Google search with advanced operators and return web content",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The main search query"
                    },
                    "before": {
                        "type": "string",
                        "description": "Search for content before this date (YYYY-MM-DD format)",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "after": {
                        "type": "string",
                        "description": "Search for content after this date (YYYY-MM-DD format)",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "intext": {
                        "type": "string",
                        "description": "Search for this text within the page content"
                    },
                    "allintext": {
                        "type": "string",
                        "description": "Search for all these terms within the page content"
                    },
                    "and_condition": {
                        "type": "string",
                        "description": "Additional term that must be present (AND operator)"
                    },
                    "must_have": {
                        "type": "string",
                        "description": "Exact phrase that must be present in results"
                    }
                },
                "required": ["search_term"]
            }
        },
        "browse_internet": {
            "name": "browse_internet",
            "description": "Browse and extract content from a list of URLs",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "uri"
                        },
                        "description": "List of URLs to browse and extract content from",
                        "minItems": 1
                    },
                    "full_text": {
                        "type": "boolean",
                        "description": "Whether to return full text or summarized content",
                        "default": False
                    }
                },
                "required": ["urls"]
            }
        },
        "shorten_url": {
            "name": "shorten_url",
            "description": "Create a shortened URL using the URL shortener service",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "The URL to shorten"
                    },
                    "custom_code": {
                        "type": "string",
                        "description": "Optional custom short code",
                        "pattern": "^[a-zA-Z0-9_-]+$"
                    }
                },
                "required": ["url"]
            }
        }
    }


def get_storage_schemas() -> Dict[str, Dict[str, Any]]:
    """Get storage and message management tool schemas."""
    return {
        "get_message_by_sort_id": {
            "name": "get_message_by_sort_id",
            "description": "Retrieve a specific message by its sort ID and role",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "enum": ["user", "assistant"],
                        "description": "The role of the message sender"
                    },
                    "chat_id": {
                        "type": "string",
                        "description": "The chat/channel ID"
                    },
                    "sort_id": {
                        "type": "integer",
                        "description": "The sort ID (timestamp) of the message"
                    }
                },
                "required": ["role", "chat_id", "sort_id"]
            }
        },
        "get_messages_in_range": {
            "name": "get_messages_in_range",
            "description": "Retrieve messages within a specific time range",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "The chat/channel ID"
                    },
                    "start_sort_id": {
                        "type": "integer",
                        "description": "Start timestamp for the range"
                    },
                    "end_sort_id": {
                        "type": "integer",
                        "description": "End timestamp for the range"
                    }
                },
                "required": ["chat_id", "start_sort_id", "end_sort_id"]
            }
        },
        "get_users": {
            "name": "get_users",
            "description": "Retrieve user information from the database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Optional specific user ID to retrieve"
                    }
                },
                "required": []
            }
        },
        "get_channels": {
            "name": "get_channels",
            "description": "Retrieve channel information from the database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Optional specific channel ID to retrieve"
                    }
                },
                "required": []
            }
        },
        "manage_mute_status": {
            "name": "manage_mute_status",
            "description": "Get or set the mute status for a chat/channel",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "The chat/channel ID"
                    },
                    "status": {
                        "type": ["boolean", "string", "null"],
                        "description": "New mute status (true/false) or null to just retrieve current status"
                    }
                },
                "required": ["chat_id"]
            }
        }
    }


def get_slack_schemas() -> Dict[str, Dict[str, Any]]:
    """Get Slack integration tool schemas."""
    return {
        "send_file_to_slack": {
            "name": "send_file_to_slack",
            "description": "Upload a file to a Slack channel",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file or URL to upload"
                    },
                    "chat_id": {
                        "type": "string",
                        "description": "Slack channel ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the file"
                    },
                    "ts": {
                        "type": "string",
                        "description": "Optional thread timestamp for threaded upload"
                    }
                },
                "required": ["file_path", "chat_id", "title"]
            }
        },
        "update_slack_users": {
            "name": "update_slack_users",
            "description": "Sync user data from Slack workspace",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        "update_slack_conversations": {
            "name": "update_slack_conversations",
            "description": "Sync channel/conversation data from Slack workspace",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }


def get_odoo_schemas() -> Dict[str, Dict[str, Any]]:
    """Get Odoo ERP integration tool schemas."""
    return {
        "odoo_get_mapped_models": {
            "name": "odoo_get_mapped_models",
            "description": "Get available mapped models from Odoo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "include_fields": {
                        "type": "boolean",
                        "description": "Whether to include field mappings",
                        "default": True
                    },
                    "model_name": {
                        "type": "string",
                        "description": "Optional filter for specific model name"
                    }
                },
                "required": []
            }
        },
        "odoo_fetch_records": {
            "name": "odoo_fetch_records",
            "description": "Retrieve records from an Odoo model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "external_model": {
                        "type": "string",
                        "description": "External model name in Odoo"
                    },
                    "filters": {
                        "type": "array",
                        "description": "Optional Odoo domain filters",
                        "items": {
                            "type": "array"
                        }
                    }
                },
                "required": ["external_model"]
            }
        },
        "odoo_create_record": {
            "name": "odoo_create_record",
            "description": "Create a new record in Odoo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "external_model": {
                        "type": "string",
                        "description": "External model name in Odoo"
                    },
                    "record_data": {
                        "type": "object",
                        "description": "Data for the new record",
                        "additionalProperties": True
                    }
                },
                "required": ["external_model", "record_data"]
            }
        },
        "odoo_update_record": {
            "name": "odoo_update_record",
            "description": "Update an existing record in Odoo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "external_model": {
                        "type": "string",
                        "description": "External model name in Odoo"
                    },
                    "record_id": {
                        "type": "integer",
                        "description": "ID of the record to update"
                    }
                },
                "required": ["external_model", "record_id"],
                "additionalProperties": True
            }
        },
        "odoo_delete_record": {
            "name": "odoo_delete_record",
            "description": "Delete a record from Odoo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "external_model": {
                        "type": "string",
                        "description": "External model name in Odoo"
                    },
                    "record_id": {
                        "type": "integer",
                        "description": "ID of the record to delete"
                    }
                },
                "required": ["external_model", "record_id"]
            }
        },
        "odoo_print_record": {
            "name": "odoo_print_record",
            "description": "Generate a PDF report for an Odoo record",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "Technical name of the Odoo model"
                    },
                    "record_id": {
                        "type": "integer",
                        "description": "ID of the record to print"
                    }
                },
                "required": ["model_name", "record_id"]
            }
        },
        "odoo_post_record": {
            "name": "odoo_post_record",
            "description": "Post a record in Odoo (change status to posted)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "external_model": {
                        "type": "string",
                        "description": "External model name in Odoo"
                    },
                    "record_id": {
                        "type": "integer",
                        "description": "ID of the record to post"
                    }
                },
                "required": ["external_model", "record_id"]
            }
        }
    }


def get_amazon_schemas() -> Dict[str, Dict[str, Any]]:
    """Get Amazon integration tool schemas."""
    return {
        "search_amazon_products": {
            "name": "search_amazon_products",
            "description": "Search for products on Amazon marketplace",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term for Amazon products"
                    },
                    "country": {
                        "type": "string",
                        "description": "Amazon marketplace country code",
                        "default": "CA",
                        "enum": ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number of results",
                        "default": 1,
                        "minimum": 1
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "How to sort the results",
                        "default": "RELEVANCE",
                        "enum": ["RELEVANCE", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW", "RATING", "NEWEST"]
                    },
                    "product_condition": {
                        "type": "string",
                        "description": "Product condition filter",
                        "default": "NEW",
                        "enum": ["NEW", "USED", "REFURBISHED"]
                    },
                    "is_prime": {
                        "type": "boolean",
                        "description": "Filter for Amazon Prime eligible products",
                        "default": False
                    },
                    "deals_and_discounts": {
                        "type": "string",
                        "description": "Filter for deals and discounts",
                        "default": "NONE",
                        "enum": ["NONE", "TODAY_DEALS", "ON_SALE"]
                    }
                },
                "required": ["query"]
            }
        },
        "search_and_format_products": {
            "name": "search_and_format_products",
            "description": "Search Amazon products and return formatted results",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term for Amazon products"
                    },
                    "country": {
                        "type": "string",
                        "description": "Amazon marketplace country code",
                        "default": "CA"
                    },
                    "max_products": {
                        "type": "integer",
                        "description": "Maximum number of products to show",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"],
                "additionalProperties": True
            }
        }
    }


def get_document_schemas() -> Dict[str, Dict[str, Any]]:
    """Get document management tool schemas."""
    return {
        "send_as_pdf": {
            "name": "send_as_pdf",
            "description": "Convert text to PDF and upload to Slack",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to convert to PDF"
                    },
                    "chat_id": {
                        "type": "string",
                        "description": "Slack channel ID to upload to"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the PDF document"
                    },
                    "ts": {
                        "type": "string",
                        "description": "Optional thread timestamp for threaded upload"
                    }
                },
                "required": ["text", "chat_id", "title"]
            }
        },
        "list_files": {
            "name": "list_files",
            "description": "List files in S3 bucket folder",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "folder_prefix": {
                        "type": "string",
                        "description": "Folder prefix to list files from",
                        "default": "uploads"
                    }
                },
                "required": []
            }
        },
        "get_embedding": {
            "name": "get_embedding",
            "description": "Generate text embedding using OpenAI",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to generate embedding for"
                    },
                    "model": {
                        "type": "string",
                        "description": "OpenAI embedding model to use",
                        "default": "text-embedding-ada-002"
                    }
                },
                "required": ["text"]
            }
        }
    }


def get_utility_schemas() -> Dict[str, Dict[str, Any]]:
    """Get utility tool schemas."""
    return {
        "solve_maths": {
            "name": "solve_maths",
            "description": "Execute Python code for mathematical calculations",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute for calculations"
                    }
                },
                "required": ["code"],
                "additionalProperties": True
            }
        },
        "ask_openai_reasoning": {
            "name": "ask_openai_reasoning",
            "description": "Query OpenAI's latest deep reasoning model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt to send to OpenAI O1 model"
                    }
                },
                "required": ["prompt"]
            }
        }
    }


def get_all_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """Get all tool schemas combined."""
    schemas = {}
    schemas.update(get_weather_schemas())
    schemas.update(get_web_browsing_schemas())
    schemas.update(get_storage_schemas())
    schemas.update(get_slack_schemas())
    schemas.update(get_odoo_schemas())
    schemas.update(get_amazon_schemas())
    schemas.update(get_document_schemas())
    schemas.update(get_utility_schemas())
    return schemas