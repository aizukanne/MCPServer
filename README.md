# MCP Office Assistant Server

A Model Context Protocol (MCP) server that exposes office assistant functions to AI applications. This server provides tools for weather data, web browsing, document management, Slack integration, Odoo ERP operations, Amazon product search, and various utility functions.

## Documentation

For detailed information on how to install, use, and contribute to this project, please see our full documentation in the **[docs](docs/)** directory.

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