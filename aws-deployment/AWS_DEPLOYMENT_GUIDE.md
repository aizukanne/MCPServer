# AWS Lambda Deployment Guide
## MCP Office Assistant

This guide will walk you through deploying your MCP Office Assistant to AWS Lambda with API Gateway for multi-project access.

## 📋 Prerequisites

### Required Tools
```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# SAM CLI  
pip install aws-sam-cli

# Configure AWS credentials
aws configure
```

### Required Permissions
Your AWS user/role needs these permissions:
- CloudFormation (full access)
- Lambda (full access)
- API Gateway (full access)
- S3 (full access)
- DynamoDB (full access)
- IAM (create/attach roles and policies)
- Parameter Store (read/write)

## 🏗️ Project Structure Setup

### 1. Organize Your Files

```bash
# Create the deployment structure
mkdir -p aws-deployment && cd aws-deployment

# Copy your existing files
cp ../config.py .
cp ../url_shortener.py .
cp -r ../handlers .
cp -r ../services .
cp -r ../schemas .
cp -r ../utils .

# Create deployment directories
mkdir -p cloudformation
mkdir -p src
mkdir -p layers/dependencies
mkdir -p examples
mkdir -p scripts
```

### 2. Copy CloudFormation Template

Save the CloudFormation template as `cloudformation/mcp-infrastructure.yaml`.

### 3. Copy Lambda Handlers

Save the Lambda handlers as:
- `src/lambda_handlers.py`
- `src/specialized_handlers.py`

### 4. Copy Client Example

Save the client example as `examples/client.py`.

## 🚀 Deployment Steps

### Step 1: Prepare Environment

```bash
# Make deployment script executable
chmod +x deploy.sh

# Create environment-specific parameter file
mkdir -p cloudformation
```

### Step 2: Configure API Keys

Create `cloudformation/parameters-dev.json`:

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
    "ParameterValue": "sk-your-openai-key-here"
  },
  {
    "ParameterKey": "SlackBotToken",
    "ParameterValue": "xoxb-your-slack-bot-token"
  },
  {
    "ParameterKey": "OpenWeatherApiKey",
    "ParameterValue": "your-openweather-api-key"
  },
  {
    "ParameterKey": "GoogleSearchApiKey",
    "ParameterValue": "your-google-search-api-key"
  },
  {
    "ParameterKey": "GoogleSearchEngineId",
    "ParameterValue": "your-search-engine-id"
  }
]
```

### Step 3: Deploy Infrastructure

```bash
# Deploy to development environment
./deploy.sh dev us-west-2 deploy

# Or deploy to production
./deploy.sh prod us-west-2 deploy
```

### Step 4: Test Deployment

```bash
# Run automated tests
./deploy.sh dev us-west-2 test

# Or test manually with the client
python examples/client.py
```

## 🔧 Manual Deployment (Alternative)

If you prefer manual deployment:

### 1. Install Dependencies

```bash
# Create Lambda layer
mkdir -p layers/dependencies/python
pip install -r requirements.txt -t layers/dependencies/python/

# Remove unnecessary files
find layers/dependencies/python/ -name "*.pyc" -delete
find layers/dependencies/python/ -type d -name "__pycache__" -exec rm -rf {} +
```

### 2. Package with SAM

```bash
# Build the application
sam build --template cloudformation/mcp-infrastructure.yaml

# Deploy the application  
sam deploy \
  --template-file .aws-sam/build/template.yaml \
  --stack-name mcp-office-assistant-dev \
  --parameter-overrides file://cloudformation/parameters-dev.json \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region us-west-2 \
  --resolve-s3
```

## 📊 Post-Deployment Configuration

### 1. Get Deployment Outputs

```bash
# Get API Gateway URL
aws cloudformation describe-stacks \
  --stack-name mcp-office-assistant-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
  --output text

# Get API Keys
aws cloudformation describe-stacks \
  --stack-name mcp-office-assistant-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ProjectAApiKey`].OutputValue' \
  --output text
```

### 2. Configure Multiple Projects

Each project gets its own API key. You can create additional keys:

```bash
# Create additional API key
aws apigateway create-api-key \
  --name "mcp-project-c" \
  --description "API Key for Project C" \
  --enabled

# Associate with usage plan
aws apigateway create-usage-plan-key \
  --usage-plan-id <usage-plan-id> \
  --key-id <new-api-key-id> \
  --key-type API_KEY
```

## 🌐 Client Integration

### Python Client

```python
from examples.client import MCPClient

# Initialize client
client = MCPClient(
    api_url="https://your-api-id.execute-api.us-west-2.amazonaws.com/dev",
    api_key="your-api-key",
    project_id="project-a"
)

# Use the tools
weather = client.get_weather("New York")
search_results = client.google_search("AI news")
products = client.search_amazon("laptop")
```

### cURL Examples

```bash
# List tools
curl -X GET "https://your-api-id.execute-api.us-west-2.amazonaws.com/dev/tools" \
  -H "x-api-key: your-api-key"

# Execute weather tool
curl -X POST "https://your-api-id.execute-api.us-west-2.amazonaws.com/dev/tools/get_weather_data" \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"location_name": "Tokyo"}'

# Execute search tool
curl -X POST "https://your-api-id.execute-api.us-west-2.amazonaws.com/dev/tools/google_search" \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"search_term": "machine learning", "after": "2024-01-01"}'
```

### JavaScript/Node.js Client

```javascript
class MCPClient {
  constructor(apiUrl, apiKey, projectId = null) {
    this.apiUrl = apiUrl;
    this.headers = {
      'Content-Type': 'application/json',
      'x-api-key': apiKey
    };
    if (projectId) {
      this.headers['X-Project-ID'] = projectId;
    }
  }

  async executetool(toolName, args = {}) {
    const response = await fetch(`${this.apiUrl}/tools/${toolName}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(args)
    });
    return response.json();
  }

  async getWeather(location = 'Whitehorse') {
    return this.executeTool('get_weather_data', { location_name: location });
  }

  async googleSearch(query, options = {}) {
    return this.executeTool('google_search', { search_term: query, ...options });
  }
}

// Usage
const client = new MCPClient(
  'https://your-api-id.execute-api.us-west-2.amazonaws.com/dev',
  'your-api-key',
  'project-a'
);

const weather = await client.getWeather('London');
console.log(weather);
```

## 📈 Monitoring and Logging

### CloudWatch Logs

Your Lambda functions automatically log to CloudWatch:

```bash
# View logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/mcp-office-assistant"

# Tail logs in real-time
aws logs tail /aws/lambda/mcp-office-assistant-dev-tool-executor --follow
```

### API Gateway Metrics

Monitor API usage in CloudWatch:
- Request count
- Latency
- Error rates
- Cache hits/misses

### Custom Dashboards

Create CloudWatch dashboards to monitor:
- Lambda function performance
- API Gateway metrics
- DynamoDB read/write capacity
- S3 bucket usage

## 🔒 Security Best Practices

### API Key Management

```bash
# Rotate API keys regularly
aws apigateway create-api-key --name "mcp-project-a-new" --enabled

# Disable old keys
aws apigateway update-api-key --api-key <old-key-id> --patch-ops op=replace,path=/enabled,value=false
```

### Parameter Store Encryption

All sensitive parameters are stored encrypted in Parameter Store:

```bash
# Update encrypted parameter
aws ssm put-parameter \
  --name "/mcp-office-assistant/dev/openai-api-key" \
  --value "new-api-key" \
  --type "SecureString" \
  --overwrite
```

### IAM Least Privilege

The Lambda execution role has minimal required permissions. Review and audit regularly.

## 💰 Cost Optimization

### Lambda Pricing

- **Requests**: $0.20 per 1M requests
- **Compute**: $0.0000166667 per GB-second
- **Typical cost**: ~$0.50-$5.00 per month for moderate usage

### API Gateway Pricing

- **REST API**: $3.50 per million API calls
- **Caching**: Additional cost for response caching

### DynamoDB Pricing

- **On-demand**: $1.25 per million read requests, $1.25 per million write requests
- **Provisioned**: Lower cost for predictable workloads

### Cost Monitoring

Set up billing alerts:

```bash
# Create billing alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "MCP-High-Costs" \
  --alarm-description "Alert when costs exceed $10" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --threshold 10.0 \
  --comparison-operator GreaterThanThreshold
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy MCP Office Assistant

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install SAM CLI
        run: pip install aws-sam-cli
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2
      
      - name: Deploy to AWS
        run: |
          sam build
          sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

## 🛠️ Troubleshooting

### Common Issues

1. **Lambda Timeout**
   ```bash
   # Increase timeout in CloudFormation template
   Timeout: 900  # 15 minutes
   ```

2. **Memory Issues**
   ```bash
   # Increase memory allocation
   MemorySize: 1024  # 1GB
   ```

3. **API Gateway Errors**
   ```bash
   # Check CloudWatch logs
   aws logs tail /aws/apigateway/mcp-office-assistant-dev --follow
   ```

4. **Permission Errors**
   ```bash
   # Check IAM role permissions
   aws iam get-role-policy --role-name mcp-office-assistant-dev-execution-role --policy-name MCPResourceAccess
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Local Testing

Test Lambda functions locally:

```bash
# Start API Gateway locally
sam local start-api

# Test specific function
sam local invoke ListToolsFunction -e events/list-tools.json
```

## 🔄 Updates and Maintenance

### Updating Code

```bash
# Deploy code changes
./deploy.sh dev us-west-2 deploy

# Deploy to production
./deploy.sh prod us-west-2 deploy
```

### Database Migrations

For schema changes:

```bash
# Backup DynamoDB tables
aws dynamodb create-backup \
  --table-name mcp-office-assistant-dev-users \
  --backup-name users-backup-$(date +%Y%m%d)
```

### Cleanup Old Resources

```bash
# Clean up old Lambda versions
aws lambda list-versions-by-function --function-name mcp-office-assistant-dev-tool-executor

# Delete old versions
aws lambda delete-function --function-name mcp-office-assistant-dev-tool-executor:1
```

## 📚 Additional Resources

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/)
- [SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
- [CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)

## 🆘 Support

For issues with the deployment:

1. Check CloudWatch logs first
2. Verify all parameters are correctly set
3. Ensure IAM permissions are sufficient
4. Test individual components in isolation
5. Use the client examples to verify functionality

## 🎯 Next Steps

After successful deployment:

1. **Set up monitoring dashboards**
2. **Configure automated backups**
3. **Implement proper logging and alerting**
4. **Set up CI/CD pipeline**
5. **Document your specific configuration**
6. **Train your team on the new API**

Your MCP Office Assistant is now running on AWS and ready to serve multiple projects! 🚀