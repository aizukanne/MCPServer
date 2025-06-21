# MCP Office Assistant - Complete Setup Guide

This guide will walk you through setting up the complete MCP Office Assistant server.

## Prerequisites

- Python 3.8 or higher
- Your existing `config.py` and `url_shortener.py` files
- Access to AWS, Slack, OpenAI, and other external services

## Step 1: Project Structure Setup

Create the following directory structure and copy the files from the artifacts:

```
mcp-office-assistant/
├── main.py                     # Main MCP server entry point
├── config.py                   # Your existing config file
├── url_shortener.py           # Your existing URL shortener
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── SETUP.md                   # This file
├── handlers/
│   ├── __init__.py            # Empty file
│   ├── weather.py
│   ├── web_browsing.py
│   ├── storage.py
│   ├── slack_integration.py
│   ├── odoo.py
│   ├── amazon.py
│   ├── documents.py
│   └── utilities.py
├── services/
│   ├── __init__.py            # Empty file
│   ├── weather_service.py
│   ├── web_service.py
│   ├── storage_service.py
│   ├── slack_service.py
│   ├── odoo_service.py
│   ├── amazon_service.py
│   ├── document_service.py
│   └── utilities_service.py
├── schemas/
│   ├── __init__.py            # Empty file
│   └── tool_schemas.py
└── utils/
    ├── __init__.py            # Empty file
    ├── validation.py
    ├── formatting.py
    └── text_processing.py
```

## Step 2: Create Empty __init__.py Files

Create empty `__init__.py` files in each directory:

```bash
touch handlers/__init__.py
touch services/__init__.py
touch schemas/__init__.py
touch utils/__init__.py
```

## Step 3: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If you encounter issues, install individually:
pip install mcp>=0.9.0
pip install boto3>=1.26.0
pip install requests>=2.28.0
pip install aiohttp>=3.8.0
pip install beautifulsoup4>=4.11.0
pip install weaviate-client>=3.15.0
pip install openai>=1.0.0
pip install fpdf>=2.5.0
pip install markdown2>=2.4.0
pip install pydantic>=2.0.0
pip install nltk>=3.8.0
pip install lxml>=4.9.0
pip install python-dotenv>=1.0.0
```

## Step 4: Environment Configuration

Create a `.env` file in the project root with your credentials:

```bash
# Weather API
OPENWEATHER_KEY=your_openweather_api_key

# Google Search
CUSTOM_SEARCH_API_KEY=your_google_custom_search_api_key
CUSTOM_SEARCH_ID=your_custom_search_engine_id

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# AWS Configuration
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

## Step 5: Update Your Existing Config

Make sure your `config.py` file exports all the necessary variables. It should include:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
openweather_api_key = os.getenv('OPENWEATHER_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
slack_bot_token = os.getenv('SLACK_BOT_TOKEN')

# AWS Configuration
docs_bucket_name = os.getenv('DOCS_BUCKET_NAME')
image_bucket_name = os.getenv('IMAGE_BUCKET_NAME')

# Database tables (DynamoDB)
names_table = None  # Initialize with boto3.resource('dynamodb').Table('your_table')
channels_table = None  # Initialize with boto3.resource('dynamodb').Table('your_table')

# Weaviate client
weaviate_client = None  # Initialize with your Weaviate configuration

# OpenAI client
import openai
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Odoo configuration
odoo_url = os.getenv('ODOO_URL')
odoo_db = os.getenv('ODOO_DB')
odoo_login = os.getenv('ODOO_LOGIN')
odoo_password = os.getenv('ODOO_PASSWORD')
base_url = os.getenv('ODOO_BASE_URL')

# Other configuration
proxy_url = os.getenv('PROXY_URL')
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more user agents as needed
]
```

## Step 6: Set Up External Services

### AWS Services
1. **S3 Buckets**: Create buckets for document storage
2. **DynamoDB Tables**: Set up tables for user and channel data
3. **IAM Permissions**: Ensure your AWS credentials have access to S3 and DynamoDB

### Weaviate Vector Database
1. Set up Weaviate instance (cloud or self-hosted)
2. Create collections for UserMessages and AssistantMessages
3. Configure connection in your config.py

### Slack App
1. Create a Slack app in your workspace
2. Add bot token scopes: `files:write`, `channels:read`, `users:read`, `chat:write`
3. Install app to workspace and get bot token

### OpenAI API
1. Get API key from OpenAI platform
2. Ensure you have access to embedding models and O1 models

## Step 7: Test Individual Components

Test each service individually:

```python
# Test weather service
python -c "
import asyncio
from services.weather_service import WeatherService
ws = WeatherService()
print(asyncio.run(ws.get_weather_data('London')))
"

# Test web service
python -c "
import asyncio
from services.web_service import WebService
ws = WebService()
print(asyncio.run(ws.browse_internet(['https://example.com'])))
"
```

## Step 8: Run the MCP Server

```bash
python main.py
```

The server should start and display:
```
INFO - Starting Office Assistant MCP Server...
INFO - Listed X tools
```

## Step 9: Connect AI Application

Configure your AI application (Claude Desktop, etc.) to connect to the MCP server. Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "office-assistant": {
      "command": "python",
      "args": ["/path/to/mcp-office-assistant/main.py"]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all `__init__.py` files are created and your Python path is correct

2. **Missing Dependencies**: Install missing packages with pip

3. **Configuration Errors**: Verify all environment variables are set correctly

4. **Service Connection Issues**: Check API keys and network connectivity

### Debugging

Enable debug logging by modifying `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

### Testing Individual Tools

You can test individual tools by importing and calling them directly:

```python
import asyncio
from handlers.weather import WeatherHandler

handler = WeatherHandler()
result = asyncio.run(handler.get_weather_data("New York"))
print(result)
```

## Verification Checklist

- [ ] All files copied to correct locations
- [ ] Dependencies installed successfully
- [ ] Environment variables configured
- [ ] External services accessible
- [ ] MCP server starts without errors
- [ ] Individual tools can be tested
- [ ] AI application connects successfully

## Support

If you encounter issues:

1. Check the logs for detailed error messages
2. Verify all environment variables are set
3. Test external service connectivity
4. Ensure your original `config.py` and `url_shortener.py` work independently

## Next Steps

Once everything is working:

1. **Monitor Performance**: Watch logs for any issues
2. **Add More Tools**: Follow the patterns to add new functionality
3. **Optimize**: Fine-tune timeouts and error handling
4. **Scale**: Consider containerization for production deployment

The MCP server is now ready to provide AI applications with access to all your office assistant functions!