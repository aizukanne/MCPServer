# MCP Server Project Structure (Python)

## Directory Layout
```
mcp-office-assistant/
├── pyproject.toml
├── requirements.txt
├── README.md
├── config.py                       # Environment configuration (from your original)
├── url_shortener.py               # URL shortener module (from your original)
├── main.py                        # Main MCP server entry point
├── handlers/
│   ├── __init__.py
│   ├── weather.py                 # Weather-related tools
│   ├── web_browsing.py           # Web browsing and search tools
│   ├── storage.py                # Message storage and retrieval tools
│   ├── slack_integration.py      # Slack integration tools
│   ├── odoo.py                   # Odoo ERP integration tools
│   ├── amazon.py                 # Amazon product search tools
│   ├── documents.py              # Document management tools
│   └── utilities.py              # Utility functions and math tools
├── services/
│   ├── __init__.py
│   ├── weather_service.py        # Weather service implementation
│   ├── web_service.py           # Web browsing service implementation
│   ├── storage_service.py       # Storage service implementation
│   ├── slack_service.py         # Slack service implementation
│   ├── odoo_service.py          # Odoo service implementation
│   ├── amazon_service.py        # Amazon service implementation
│   └── document_service.py      # Document service implementation
├── schemas/
│   ├── __init__.py
│   └── tool_schemas.py          # Tool schemas and type definitions
└── utils/
    ├── __init__.py
    ├── validation.py            # Input validation utilities
    ├── formatting.py           # Response formatting utilities
    └── text_processing.py      # Text processing utilities
```

## Module Organization

### Core Categories (8 handler modules):

1. **Weather Tools** (`weather.py`)
   - `get_weather_data` - Get current weather for location
   - `get_coordinates` - Get coordinates for location name

2. **Web Browsing Tools** (`web_browsing.py`)
   - `google_search` - Perform Google search with advanced operators
   - `browse_internet` - Browse and extract content from URLs
   - `shorten_url` - Create shortened URLs

3. **Storage & Messages** (`storage.py`)
   - `get_message_by_sort_id` - Retrieve specific message by ID
   - `get_messages_in_range` - Get messages within date range
   - `get_users` - Retrieve user information
   - `get_channels` - Get Slack channel information
   - `manage_mute_status` - Manage channel mute status

4. **Slack Integration** (`slack_integration.py`)
   - `send_file_to_slack` - Upload files to Slack channels
   - `update_slack_users` - Sync user data from Slack
   - `update_slack_conversations` - Sync channel data from Slack

5. **Odoo ERP Integration** (`odoo.py`)
   - `odoo_get_mapped_models` - Get available Odoo models
   - `odoo_fetch_records` - Retrieve records from Odoo
   - `odoo_create_record` - Create new records in Odoo
   - `odoo_update_record` - Update existing Odoo records
   - `odoo_delete_record` - Delete records from Odoo
   - `odoo_print_record` - Generate PDF reports from Odoo
   - `odoo_post_record` - Post records in Odoo

6. **Amazon Integration** (`amazon.py`)
   - `search_amazon_products` - Search Amazon marketplace
   - `search_and_format_products` - Search and format results

7. **Document Management** (`documents.py`)
   - `send_as_pdf` - Convert text to PDF and upload
   - `list_files` - List files in S3 bucket
   - `get_embedding` - Generate text embeddings

8. **Utilities** (`utilities.py`)
   - `solve_maths` - Execute mathematical calculations
   - `ask_openai_o1` - Query OpenAI O1 model

## Key Design Principles

1. **Separation of Concerns**: Each handler focuses on a specific domain
2. **Service Layer**: Business logic separated from MCP handlers
3. **Shared Utilities**: Common functions in utils directory
4. **Type Safety**: Python type hints and Pydantic models
5. **Error Handling**: Consistent error responses across all tools
6. **Validation**: Input validation for all tool parameters

## Dependencies

The project will require these main dependencies:
- `mcp` - MCP SDK for Python
- `boto3` - AWS services (S3, DynamoDB)
- `requests` - HTTP requests
- `aiohttp` - Async HTTP requests
- `beautifulsoup4` - HTML parsing
- `weaviate-client` - Vector database
- `openai` - OpenAI API
- `fpdf` - PDF generation
- `markdown2` - Markdown processing
- `pydantic` - Data validation
- `nltk` - Natural language processing

## Configuration

Environment variables will be managed through your existing `config.py` module, maintaining compatibility with your current setup.

## Migration Strategy

1. **Preserve Existing Logic**: Your original functions will be minimally modified
2. **Add MCP Wrappers**: Each function gets an MCP-compliant wrapper
3. **Maintain Dependencies**: Keep your existing imports and configurations
4. **Gradual Integration**: Functions can be migrated one module at a time

This structure ensures maintainability while leveraging your existing Python codebase and dependencies.