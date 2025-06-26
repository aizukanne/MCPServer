# MCP Server Installation Troubleshooting Guide

## Common Installation Issues

### 1. Import Errors on Startup

If you encounter errors like:
```
TypeError: NoneType takes no arguments
WARNING:root:Config module not available, storage operations will not work
```

This indicates missing Python dependencies.

### 2. Required Dependencies

The application requires the following Python packages to be installed:

#### Core Dependencies (from requirements.txt):
- `mcp>=0.9.0` - MCP Server framework
- `openai>=1.0.0` - OpenAI API client
- `boto3>=1.26.0` - AWS SDK
- `weaviate-client>=3.15.0` - Vector database client
- `slack-sdk>=3.19.0` - Slack integration
- `semantic-router>=0.0.20` - Semantic routing for AI
- `fpdf==1.7.2` - PDF generation
- `markdown2>=2.4.0` - Markdown processing

### 3. Installation Steps

1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python3 diagnose_imports.py
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in required values:
   ```bash
   cp .env.example .env
   ```

### 4. Environment Variables

The application requires several environment variables to be set:

- `OPENAI_API_KEY` - Required for OpenAI services
- `SLACK_BOT_TOKEN` - Required for Slack integration
- `WEAVIATE_API_KEY` - Required for Weaviate vector database
- `WEAVIATE_URL` - Weaviate instance URL
- Other service-specific keys as needed

### 5. Troubleshooting Steps

If the application still fails to start:

1. **Check Python version:**
   ```bash
   python3 --version
   ```
   Ensure you're using Python 3.8 or higher.

2. **Check installed packages:**
   ```bash
   pip list | grep -E "openai|fpdf|slack-sdk|semantic-router|weaviate-client|mcp"
   ```

3. **Run the diagnostic script:**
   ```bash
   python3 diagnose_imports.py
   ```

4. **Check for import errors in isolation:**
   ```bash
   python3 -c "import fpdf; print('fpdf OK')"
   python3 -c "import openai; print('openai OK')"
   python3 -c "import slack_sdk; print('slack_sdk OK')"
   python3 -c "import semantic_router; print('semantic_router OK')"
   ```

### 6. Common Solutions

#### Missing fpdf module:
```bash
pip install fpdf==1.7.2
```

#### Missing semantic-router:
```bash
pip install semantic-router
```

#### Missing slack-sdk:
```bash
pip install slack-sdk
```

#### Virtual Environment Issues:
If you're using a virtual environment, ensure it's activated:
```bash
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 7. Clean Installation

For a clean installation from scratch:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python3 diagnose_imports.py

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
python3 main.py
```

### 8. AWS Deployment Specific

If deploying to AWS Lambda, ensure the Lambda layer includes all dependencies:
```bash
cd aws-deployment
./deploy.sh
```

The deployment script should handle dependency packaging automatically.

## Still Having Issues?

If you continue to experience problems:

1. Check the `docs/TROUBLESHOOTING.md` for more detailed troubleshooting
2. Ensure all API keys and credentials are correctly set in `.env`
3. Check that all required AWS resources are properly configured
4. Review the application logs for more specific error messages