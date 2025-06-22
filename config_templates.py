"""
Configuration File Templates
============================

Templates for configuration files like .env, .gitignore, and client examples.
"""


class ConfigTemplates:
    """Configuration file templates."""
    
    def get_env_template(self) -> str:
        """Get .env file template."""
        return '''# MCP Office Assistant Environment Variables
# ==========================================
# Copy this file to .env and fill in your actual values

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Weather API
OPENWEATHER_KEY=your-openweather-api-key

# Google Search
CUSTOM_SEARCH_API_KEY=your-google-custom-search-api-key
CUSTOM_SEARCH_ID=your-custom-search-engine-id

# Slack Integration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

# AWS Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-west-2

# S3 Buckets
DOCS_BUCKET_NAME=your-documents-bucket
IMAGE_BUCKET_NAME=your-images-bucket

# Odoo ERP (if using)
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your-database-name
ODOO_LOGIN=your-username
ODOO_PASSWORD=your-password
ODOO_BASE_URL=https://your-odoo-api-base.com

# Proxy (if needed)
PROXY_URL=http://your-proxy:port

# DynamoDB Tables (will be created by CloudFormation)
NAMES_TABLE=mcp-office-assistant-dev-users
CHANNELS_TABLE=mcp-office-assistant-dev-channels
'''
    
    def get_gitignore_template(self) -> str:
        """Get .gitignore file template."""
        return '''# MCP Office Assistant - Git Ignore
# =================================

# Environment files
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# AWS
.aws-sam/
samconfig.toml.backup

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# API Keys and Secrets (extra safety)
**/parameters-*.json.backup
**/*key*
**/*secret*
**/*token*

# Lambda layers (these get rebuilt)
aws-deployment/layers/dependencies/python/

# Artifacts directory (if used)
artifacts/
'''
    
    def get_js_client_template(self) -> str:
        """Get JavaScript client template."""
        return '''// MCP Office Assistant - JavaScript Client Example
// ================================================

class MCPClient {
  constructor(apiUrl, apiKey, projectId = null) {
    this.apiUrl = apiUrl.replace(/\\/$/, ''); // Remove trailing slash
    this.headers = {
      'Content-Type': 'application/json',
      'x-api-key': apiKey
    };
    
    if (projectId) {
      this.headers['X-Project-ID'] = projectId;
    }
  }

  async listTools() {
    const response = await fetch(`${this.apiUrl}/tools`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  async executeTool(toolName, args = {}) {
    const response = await fetch(`${this.apiUrl}/tools/${toolName}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(args)
    });
    return response.json();
  }

  // Convenience methods
  async getWeather(location = 'Whitehorse') {
    return this.executeTool('get_weather_data', { location_name: location });
  }

  async googleSearch(query, options = {}) {
    return this.executeTool('google_search', { search_term: query, ...options });
  }

  async searchAmazon(query, country = 'CA', options = {}) {
    return this.executeTool('search_amazon_products', { query, country, ...options });
  }

  async solveMath(code, params = {}) {
    return this.executeTool('solve_maths', { code, ...params });
  }

  async getEmbedding(text, model = 'text-embedding-ada-002') {
    return this.executeTool('get_embedding', { text, model });
  }

  async browseUrls(urls, fullText = false) {
    return this.executeTool('browse_internet', { urls, full_text: fullText });
  }
}

// Example usage (Node.js)
async function example() {
  const client = new MCPClient(
    'https://your-api-id.execute-api.us-west-2.amazonaws.com/dev',
    'your-api-key',
    'project-a'
  );

  try {
    // List tools
    const tools = await client.listTools();
    console.log('Available tools:', tools.tools?.length || 0);

    // Get weather
    const weather = await client.getWeather('Tokyo');
    console.log('Weather:', weather);

    // Math calculation
    const math = await client.solveMath('result = 10 * 5 + 2');
    console.log('Math result:', math);

    // Google search
    const search = await client.googleSearch('AI news', { after: '2024-01-01' });
    console.log('Search results:', search);

  } catch (error) {
    console.error('Error:', error);
  }
}

// Uncomment to run example
// example();

module.exports = MCPClient;
'''