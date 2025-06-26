# MCP Office Assistant Server

A Model Context Protocol (MCP) server that exposes office assistant functions to AI applications. This server provides tools for weather data, web browsing, document management, Slack integration, Odoo ERP operations, Amazon product search, and various utility functions.

## Features

### Weather Tools
- Get current weather data for any location
- Retrieve geographical coordinates for location names

### Web Browsing Tools
- Perform Google searches with advanced operators
- Browse and extract content from multiple URLs
- URL shortening service

### Storage & Messages
- Retrieve messages by ID or date range
- User and channel management
- Mute status management for channels

### Slack Integration
- File uploads to Slack channels
- User and conversation synchronization

### Odoo ERP Integration
- Fetch, create, update, and delete records
- Generate PDF reports
- Post records (workflow actions)

### Amazon Integration
- Product search across multiple marketplaces
- Formatted product results with pricing and ratings

### Document Management
- Convert text to PDF and upload to Slack
- File listing from S3 buckets
- Text embedding generation

### Utilities
- Mathematical calculations with Python code execution
- OpenAI O1 model queries for advanced reasoning

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-office-assistant
   ```

2. **Install dependencies:**
   ```bash
   # First, install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with the following variables:
   ```bash
   # Weather API
   OPENWEATHER_KEY=your_openweather_api_key
   
   # Google Search
   CUSTOM_SEARCH_API_KEY=your_google_custom_search_api_key
   CUSTOM_SEARCH_ID=your_custom_search_engine_id
   
   # OpenAI
   OPENAI_API_KEY=your_openai_api_key
   
   # AWS Configuration (for S3 and DynamoDB)
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_DEFAULT_REGION=your_aws_region
   
   # Slack
   SLACK_BOT_TOKEN=your_slack_bot_token
   
   # Odoo (if using ERP integration)
   ODOO_URL=your_odoo_instance_url
   ODOO_DB=your_odoo_database
   ODOO_LOGIN=your_odoo_username
   ODOO_PASSWORD=your_odoo_password
   ```

4. **Configure your existing modules:**
   - Ensure your `config.py` file is properly configured
   - Make sure your `url_shortener.py` module is available
   - Set up Weaviate, DynamoDB tables, and other dependencies as needed

## Usage

### Starting the Server

```bash
python main.py
```

The server will start and listen for MCP connections.

### Using with AI Applications

Configure your AI application to connect to the MCP server. The server exposes the following tools:

#### Weather Tools
- `get_weather_data(location_name?)` - Get weather for a location
- `get_coordinates(location_name)` - Get lat/lon coordinates

#### Web Tools
- `google_search(search_term, before?, after?, intext?, allintext?, and_condition?, must_have?)` - Advanced Google search
- `browse_internet(urls, full_text?)` - Extract content from URLs
- `shorten_url(url, custom_code?)` - Create shortened URLs

#### Storage Tools
- `get_message_by_sort_id(role, chat_id, sort_id)` - Retrieve specific message
- `get_messages_in_range(chat_id, start_sort_id, end_sort_id)` - Get messages in time range
- `get_users(user_id?)` - Get user information
- `get_channels(id?)` - Get channel information
- `manage_mute_status(chat_id, status?)` - Manage channel mute status

#### Slack Tools
- `send_file_to_slack(file_path, chat_id, title, ts?)` - Upload files to Slack
- `update_slack_users()` - Sync user data from Slack
- `update_slack_conversations()` - Sync channel data from Slack

#### Odoo Tools
- `odoo_get_mapped_models(include_fields?, model_name?)` - Get available models
- `odoo_fetch_records(external_model, filters?)` - Retrieve records
- `odoo_create_record(external_model, record_data)` - Create new record
- `odoo_update_record(external_model, record_id, **fields)` - Update record
- `odoo_delete_record(external_model, record_id)` - Delete record
- `odoo_print_record(model_name, record_id)` - Generate PDF report
- `odoo_post_record(external_model, record_id)` - Post record

#### Amazon Tools
- `search_amazon_products(query, country?, page?, sort_by?, product_condition?, is_prime?, deals_and_discounts?)` - Search products
- `search_and_format_products(query, country?, max_products?, **options)` - Search and format results

#### Document Tools
- `send_as_pdf(text, chat_id, title, ts?)` - Convert text to PDF and upload
- `list_files(folder_prefix?)` - List files in S3 bucket
- `get_embedding(text, model?)` - Generate text embeddings

#### Utility Tools
- `solve_maths(code, **params)` - Execute Python math calculations
- `ask_openai_o1(prompt)` - Query OpenAI O1 model

## Project Structure

```
mcp-office-assistant/
├── main.py                     # Main MCP server entry point
├── config.py                   # Environment configuration
├── url_shortener.py           # URL shortener module
├── handlers/                   # MCP tool handlers
│   ├── weather.py
│   ├── web_browsing.py
│   ├── storage.py
│   ├── slack_integration.py
│   ├── odoo.py
│   ├── amazon.py
│   ├── documents.py
│   └── utilities.py
├── services/                   # Business logic services
│   ├── weather_service.py
│   ├── web_service.py
│   ├── storage_service.py
│   ├── slack_service.py
│   ├── odoo_service.py
│   ├── amazon_service.py
│   ├── document_service.py
│   └── utilities_service.py
├── schemas/                    # Tool schemas and types
│   └── tool_schemas.py
├── utils/                      # Utility modules
│   ├── validation.py
│   ├── formatting.py
│   └── text_processing.py
└── README.md
```

## Development

### Adding New Tools

1. **Define the schema** in `schemas/tool_schemas.py`
2. **Create a handler** in the appropriate handler module
3. **Implement the service logic** in the corresponding service module
4. **Add the tool routing** in `main.py`

### Error Handling

All tools return consistent JSON responses with status indicators:
- Success responses include `"status": "success"` and data
- Error responses include `"status": "error"` and error details

### Validation

Input validation is performed using JSON Schema validation in `utils/validation.py`. All tools validate their inputs before processing.

## Security Considerations

- Input sanitization prevents injection attacks
- File path validation prevents directory traversal
- Code execution is limited to safe mathematical operations
- All external API calls include proper error handling

## Dependencies

- `mcp` - Model Context Protocol SDK
- `boto3` - AWS services
- `requests` / `aiohttp` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `weaviate-client` - Vector database
- `openai` - OpenAI API
- `fpdf` - PDF generation
- `nltk` - Natural language processing

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the logs for detailed error messages
- Ensure all environment variables are properly configured
- Verify that external services (AWS, Slack, etc.) are accessible