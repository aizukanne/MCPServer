# MCP Office Assistant - Complete Integration Guide

This guide shows you exactly how to integrate all the new AWS Lambda deployment files with your existing MCP Office Assistant project.

## 📁 Complete Project Structure

Here's the final directory structure with all files organized:

```
mcp-office-assistant/
├── 📄 README.md                           # Main project documentation
├── 📄 SETUP.md                            # Original local setup guide  
├── 📄 INTEGRATION_GUIDE.md                # This file
├── 📄 pyproject.toml                      # Python package configuration
├── 📄 requirements.txt                    # Python dependencies
├── 📄 config.py                           # Your existing configuration
├── 📄 url_shortener.py                    # Your existing URL shortener
├── 📄 main.py                             # Original MCP server (local)
│
├── 📁 aws-deployment/                     # AWS Lambda deployment files
│   ├── 📄 AWS_DEPLOYMENT_GUIDE.md         # AWS deployment documentation
│   ├── 📄 deploy.sh                       # Deployment script
│   ├── 📄 samconfig.toml                  # SAM configuration
│   │
│   ├── 📁 cloudformation/                 # CloudFormation templates
│   │   ├── 📄 mcp-infrastructure.yaml     # Main infrastructure template
│   │   ├── 📄 parameters-dev.json         # Development parameters
│   │   ├── 📄 parameters-staging.json     # Staging parameters
│   │   └── 📄 parameters-prod.json        # Production parameters
│   │
│   ├── 📁 src/                            # Lambda source code
│   │   ├── 📄 lambda_handlers.py          # Main Lambda handlers
│   │   ├── 📄 specialized_handlers.py     # Specialized handlers
│   │   ├── 📄 config.py                   # Copy of your config
│   │   ├── 📄 url_shortener.py            # Copy of your URL shortener
│   │   │
│   │   ├── 📁 handlers/                   # Copy of handlers
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 weather.py
│   │   │   ├── 📄 web_browsing.py
│   │   │   ├── 📄 storage.py
│   │   │   ├── 📄 slack_integration.py
│   │   │   ├── 📄 odoo.py
│   │   │   ├── 📄 amazon.py
│   │   │   ├── 📄 documents.py
│   │   │   └── 📄 utilities.py
│   │   │
│   │   ├── 📁 services/                   # Copy of services
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 weather_service.py
│   │   │   ├── 📄 web_service.py
│   │   │   ├── 📄 storage_service.py
│   │   │   ├── 📄 slack_service.py
│   │   │   ├── 📄 odoo_service.py
│   │   │   ├── 📄 amazon_service.py
│   │   │   ├── 📄 document_service.py
│   │   │   └── 📄 utilities_service.py
│   │   │
│   │   ├── 📁 schemas/                    # Copy of schemas
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 tool_schemas.py
│   │   │
│   │   └── 📁 utils/                      # Copy of utils
│   │       ├── 📄 __init__.py
│   │       ├── 📄 validation.py
│   │       ├── 📄 formatting.py
│   │       └── 📄 text_processing.py
│   │
│   ├── 📁 layers/                         # Lambda layers (auto-generated)
│   │   └── 📁 dependencies/
│   │       ├── 📄 requirements.txt
│   │       └── 📁 python/                 # Installed packages
│   │
│   ├── 📁 examples/                       # Client examples
│   │   ├── 📄 client.py                   # Python client
│   │   ├── 📄 client.js                   # JavaScript client
│   │   └── 📄 test_api.sh                 # Shell script tests
│   │
│   └── 📁 scripts/                        # Utility scripts
│       ├── 📄 setup_environment.sh        # Environment setup
│       ├── 📄 test_deployment.py          # Deployment tests
│       └── 📄 cleanup.sh                  # Cleanup script
│
├── 📁 handlers/                           # Original MCP handlers
│   ├── 📄 __init__.py
│   ├── 📄 weather.py
│   ├── 📄 web_browsing.py
│   ├── 📄 storage.py
│   ├── 📄 slack_integration.py
│   ├── 📄 odoo.py
│   ├── 📄 amazon.py
│   ├── 📄 documents.py
│   └── 📄 utilities.py
│
├── 📁 services/                           # Original service implementations
│   ├── 📄 __init__.py
│   ├── 📄 weather_service.py
│   ├── 📄 web_service.py
│   ├── 📄 storage_service.py
│   ├── 📄 slack_service.py
│   ├── 📄 odoo_service.py
│   ├── 📄 amazon_service.py
│   ├── 📄 document_service.py
│   └── 📄 utilities_service.py
│
├── 📁 schemas/                            # Tool schemas
│   ├── 📄 __init__.py
│   └── 📄 tool_schemas.py
│
├── 📁 utils/                              # Utility functions
│   ├── 📄 __init__.py
│   ├── 📄 validation.py
│   ├── 📄 formatting.py
│   └── 📄 text_processing.py
│
└── 📁 docs/                               # Documentation
    ├── 📄 API_REFERENCE.md                # API documentation
    ├── 📄 TROUBLESHOOTING.md              # Common issues
    └── 📄 CHANGELOG.md                    # Version history
```

## 🚀 Step-by-Step Integration Process

### Step 1: Create Directory Structure

```bash
# Navigate to your existing project
cd mcp-office-assistant

# Create AWS deployment directory
mkdir -p aws-deployment/{cloudformation,src,layers/dependencies,examples,scripts}

# Create empty __init__.py files for AWS deployment
touch aws-deployment/src/handlers/__init__.py
touch aws-deployment/src/services/__init__.py  
touch aws-deployment/src/schemas/__init__.py
touch aws-deployment/src/utils/__init__.py
```

### Step 2: Copy Core Files

Create these files in your project root (if you haven't already):

**📄 Create/Update `handlers/__init__.py`:**
```python
# Empty file - just ensures Python treats this as a package
```

**📄 Create/Update `services/__init__.py`:**
```python
# Empty file - just ensures Python treats this as a package
```

**📄 Create/Update `schemas/__init__.py`:**
```python
# Empty file - just ensures Python treats this as a package
```

**📄 Create/Update `utils/__init__.py`:**
```python
# Empty file - just ensures Python treats this as a package
```

### Step 3: AWS Deployment Files

Save each artifact to the correct location:

#### CloudFormation Template
```bash
# Save to: aws-deployment/cloudformation/mcp-infrastructure.yaml
# Content: Use the CloudFormation template artifact
```

#### Lambda Handlers
```bash
# Save to: aws-deployment/src/lambda_handlers.py
# Content: Use the lambda_handlers.py artifact

# Save to: aws-deployment/src/specialized_handlers.py  
# Content: Use the specialized_handlers.py artifact
```

#### Deployment Scripts
```bash
# Save to: aws-deployment/deploy.sh
# Content: Use the deploy.sh artifact
chmod +x aws-deployment/deploy.sh

# Save to: aws-deployment/samconfig.toml
# Content: Use the samconfig.toml artifact
```

#### Documentation
```bash
# Save to: aws-deployment/AWS_DEPLOYMENT_GUIDE.md
# Content: Use the AWS deployment guide artifact

# Save to: INTEGRATION_GUIDE.md (this file)
# Content: This integration guide
```

#### Client Examples
```bash
# Save to: aws-deployment/examples/client.py
# Content: Use the client.py artifact
```

### Step 4: Copy Your Source Code to AWS Directory

```bash
# Copy your existing files to AWS deployment src
cp config.py aws-deployment/src/
cp url_shortener.py aws-deployment/src/

# Copy all handlers, services, schemas, and utils
cp -r handlers aws-deployment/src/
cp -r services aws-deployment/src/
cp -r schemas aws-deployment/src/
cp -r utils aws-deployment/src/
```

### Step 5: Create Parameter Files

**📄 Create `aws-deployment/cloudformation/parameters-dev.json`:**
```json
[
  {
    "ParameterKey": "Environment",
    "ParameterValue": "dev"
  },
  {
    "ParameterKey": "ProjectName", 
    "ParameterValue": "mcp-office-assistant"
  },
  {
    "ParameterKey": "AllowedOrigins",
    "ParameterValue": "*"
  },
  {
    "ParameterKey": "OpenAIApiKey",
    "ParameterValue": "REPLACE_WITH_YOUR_OPENAI_API_KEY"
  },
  {
    "ParameterKey": "SlackBotToken",
    "ParameterValue": "REPLACE_WITH_YOUR_SLACK_BOT_TOKEN"
  },
  {
    "ParameterKey": "OpenWeatherApiKey",
    "ParameterValue": "REPLACE_WITH_YOUR_OPENWEATHER_API_KEY"
  },
  {
    "ParameterKey": "GoogleSearchApiKey",
    "ParameterValue": "REPLACE_WITH_YOUR_GOOGLE_SEARCH_API_KEY"
  },
  {
    "ParameterKey": "GoogleSearchEngineId",
    "ParameterValue": "REPLACE_WITH_YOUR_SEARCH_ENGINE_ID"
  }
]
```

**📄 Create `aws-deployment/cloudformation/parameters-prod.json`:**
```json
[
  {
    "ParameterKey": "Environment",
    "ParameterValue": "prod"
  },
  {
    "ParameterKey": "ProjectName", 
    "ParameterValue": "mcp-office-assistant"
  },
  {
    "ParameterKey": "AllowedOrigins",
    "ParameterValue": "https://yourdomain.com,https://app.yourdomain.com"
  },
  {
    "ParameterKey": "OpenAIApiKey",
    "ParameterValue": "REPLACE_WITH_PRODUCTION_OPENAI_API_KEY"
  },
  {
    "ParameterKey": "SlackBotToken",
    "ParameterValue": "REPLACE_WITH_PRODUCTION_SLACK_BOT_TOKEN"
  },
  {
    "ParameterKey": "OpenWeatherApiKey",
    "ParameterValue": "REPLACE_WITH_PRODUCTION_OPENWEATHER_API_KEY"
  },
  {
    "ParameterKey": "GoogleSearchApiKey",
    "ParameterValue": "REPLACE_WITH_PRODUCTION_GOOGLE_SEARCH_API_KEY"
  },
  {
    "ParameterKey": "GoogleSearchEngineId",
    "ParameterValue": "REPLACE_WITH_PRODUCTION_SEARCH_ENGINE_ID"
  }
]
```

### Step 6: Create Additional Utility Scripts

**📄 Create `aws-deployment/scripts/setup_environment.sh`:**
```bash
#!/bin/bash

echo "Setting up AWS deployment environment..."

# Check prerequisites
command -v aws >/dev/null 2>&1 || { echo "AWS CLI required but not installed. Aborting." >&2; exit 1; }
command -v sam >/dev/null 2>&1 || { echo "SAM CLI required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required but not installed. Aborting." >&2; exit 1; }

# Check AWS credentials
aws sts get-caller-identity >/dev/null 2>&1 || { echo "AWS credentials not configured. Run 'aws configure' first." >&2; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install dependencies using uv
uv pip install aws-sam-cli boto3 requests

echo "Environment setup complete!"
echo "Next steps:"
echo "1. Update parameter files with your API keys"
echo "2. Run: cd aws-deployment && ./deploy.sh dev us-west-2 deploy"
```

**📄 Create `aws-deployment/examples/test_api.sh`:**
```bash
#!/bin/bash

# Test script for the deployed MCP API
API_URL="$1"
API_KEY="$2"

if [ -z "$API_URL" ] || [ -z "$API_KEY" ]; then
    echo "Usage: $0 <API_URL> <API_KEY>"
    echo "Example: $0 https://abc123.execute-api.us-west-2.amazonaws.com/dev your-api-key"
    exit 1
fi

echo "Testing MCP Office Assistant API"
echo "================================"

# Test 1: List tools
echo "1. Listing available tools..."
curl -s -X GET "$API_URL/tools" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" | jq .

echo -e "\n2. Testing weather tool..."
curl -s -X POST "$API_URL/tools/get_weather_data" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location_name": "London"}' | jq .

echo -e "\n3. Testing math tool..."
curl -s -X POST "$API_URL/tools/solve_maths" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "result = 2 + 2"}' | jq .

echo -e "\nAPI tests completed!"
```

**📄 Create `aws-deployment/scripts/cleanup.sh`:**
```bash
#!/bin/bash

ENVIRONMENT=${1:-dev}
REGION=${2:-us-west-2}

echo "Cleaning up MCP Office Assistant deployment..."
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

STACK_NAME="mcp-office-assistant-$ENVIRONMENT"

# Get S3 bucket name and empty it
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucket`].OutputValue' \
  --output text \
  --region $REGION 2>/dev/null)

if [ ! -z "$BUCKET_NAME" ]; then
  echo "Emptying S3 bucket: $BUCKET_NAME"
  aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION
fi

# Delete CloudFormation stack
echo "Deleting CloudFormation stack: $STACK_NAME"
aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION

echo "Cleanup initiated. Stack deletion may take several minutes."
```

### Step 7: Update Your Main README

**📄 Update your main `README.md`:**
```markdown
# MCP Office Assistant

A comprehensive office assistant with both local MCP server and AWS Lambda deployment options.

## 🏗️ Architecture Options

### Option 1: Local MCP Server
- Direct MCP protocol support
- WebSocket connections
- Local development and testing
- See [SETUP.md](SETUP.md) for local setup

### Option 2: AWS Lambda Deployment  
- REST API via API Gateway
- Auto-scaling and cost-effective
- Multi-project support
- See [aws-deployment/AWS_DEPLOYMENT_GUIDE.md](aws-deployment/AWS_DEPLOYMENT_GUIDE.md)

## 🚀 Quick Start

### Local Development
```bash
python main.py
```

### AWS Deployment
```bash
cd aws-deployment
./deploy.sh dev us-west-2 deploy
```

## 📁 Project Structure

- `/handlers/` - MCP tool handlers
- `/services/` - Business logic services  
- `/schemas/` - Tool schemas and validation
- `/utils/` - Utility functions
- `/aws-deployment/` - AWS Lambda deployment files
- `/docs/` - Documentation

## 🔧 Configuration

Both deployment options use the same `config.py` file for configuration.

## 📚 Documentation

- [Local Setup Guide](SETUP.md) - Set up MCP server locally
- [AWS Deployment Guide](aws-deployment/AWS_DEPLOYMENT_GUIDE.md) - Deploy to AWS Lambda
- [Integration Guide](INTEGRATION_GUIDE.md) - File organization and integration
- [API Reference](docs/API_REFERENCE.md) - Tool documentation

## 🛠️ Available Tools

### Weather Tools
- `get_weather_data` - Current weather for any location
- `get_coordinates` - Get lat/lon coordinates

### Web Browsing Tools  
- `google_search` - Advanced Google search
- `browse_internet` - Extract content from URLs
- `shorten_url` - URL shortening service

### Storage & Messages
- `get_messages_*` - Message retrieval and management
- `get_users` / `get_channels` - User and channel data

### Integrations
- **Slack**: File uploads, user sync
- **Odoo ERP**: Complete ERP integration
- **Amazon**: Product search
- **OpenAI**: Embeddings and O1 model

### Utilities
- `solve_maths` - Mathematical calculations
- `send_as_pdf` - Document generation
- `list_files` - File management

## 🔑 Environment Variables

Required for both deployment options:
```bash
OPENAI_API_KEY=your_openai_key
SLACK_BOT_TOKEN=your_slack_token
OPENWEATHER_KEY=your_weather_key
CUSTOM_SEARCH_API_KEY=your_google_key
CUSTOM_SEARCH_ID=your_search_engine_id
```
```

## 📋 Final Checklist

Before deploying, ensure you have:

- [ ] ✅ All files copied to correct locations
- [ ] ✅ API keys updated in parameter files
- [ ] ✅ AWS CLI configured with proper credentials
- [ ] ✅ SAM CLI installed
- [ ] ✅ Python dependencies installed
- [ ] ✅ Your original `config.py` and `url_shortener.py` working
- [ ] ✅ All `__init__.py` files created in directories
- [ ] ✅ Deployment script made executable (`chmod +x`)

## 🎯 Next Steps

### For Local Development:
```bash
# Test your local MCP server first
python main.py
```

### For AWS Deployment:
```bash
# Navigate to AWS deployment directory
cd aws-deployment

# Update your API keys in parameter files
nano cloudformation/parameters-dev.json

# Set up environment
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Deploy to AWS
./deploy.sh dev us-west-2 deploy

# Test the deployment
python examples/client.py
```

## 🔄 Development Workflow

1. **Develop locally** using the MCP server (`main.py`)
2. **Test changes** with your AI application
3. **Copy updates** to `aws-deployment/src/` 
4. **Deploy to staging** (`./deploy.sh staging`)
5. **Test staging** environment
6. **Deploy to production** (`./deploy.sh prod`)

Your project now supports both local development and scalable AWS deployment! 🚀