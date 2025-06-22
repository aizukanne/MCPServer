# Troubleshooting Guide

## Common Issues and Solutions

### 🔧 Local Development Issues

#### Python Import Errors
```bash
ModuleNotFoundError: No module named 'handlers'
```

**Solution:**
1. Ensure all `__init__.py` files exist
2. Check Python path: `export PYTHONPATH="${PYTHONPATH}:."`
3. Install missing dependencies: `pip install -r requirements.txt`

#### Config Module Not Found
```bash
ModuleNotFoundError: No module named 'config'
```

**Solution:**
1. Ensure `config.py` exists in project root
2. Check config.py contains all required variables
3. Verify environment variables are set

### ☁️ AWS Deployment Issues

#### SAM Build Failures
```bash
BUILD FAILED - Missing dependencies
```

**Solution:**
1. Install SAM CLI: `pip install aws-sam-cli`
2. Install Docker for containerized builds
3. Check Python version compatibility (3.9+)

#### CloudFormation Stack Errors
```bash
CREATE_FAILED - Insufficient permissions
```

**Solution:**
1. Check IAM permissions for CloudFormation
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Ensure region supports all services

#### Lambda Function Timeouts
```bash
Task timed out after 300.00 seconds
```

**Solution:**
1. Increase timeout in CloudFormation template
2. Optimize function code for performance
3. Use specialized handlers for heavy operations

#### API Gateway 403 Errors
```bash
{"message": "Forbidden"}
```

**Solution:**
1. Check API key is correct
2. Verify API key is associated with usage plan
3. Check CORS configuration for browser requests

### 🔑 Authentication Issues

#### Invalid API Key
```bash
{"message": "Forbidden"}
```

**Solution:**
1. Get API key from CloudFormation outputs
2. Check API key hasn't been deleted or disabled
3. Verify correct stage (dev/staging/prod)

#### Parameter Store Access Denied
```bash
AccessDenied: User is not authorized to perform ssm:GetParameter
```

**Solution:**
1. Check Lambda execution role has SSM permissions
2. Verify parameter names match CloudFormation
3. Ensure parameters exist in correct region

### 📡 Network and Connectivity Issues

#### Connection Timeouts
```bash
Connection timeout when calling external APIs
```

**Solution:**
1. Check internet connectivity from Lambda
2. Verify VPC configuration if using custom VPC
3. Check security group rules
4. Increase timeout values

#### DNS Resolution Issues
```bash
Unable to resolve hostname
```

**Solution:**
1. Check VPC DNS settings
2. Verify NAT Gateway configuration
3. Test DNS resolution locally

### 💰 Cost Issues

#### Unexpected High Costs
```bash
AWS bill higher than expected
```

**Solution:**
1. Check CloudWatch metrics for usage
2. Review API Gateway request counts
3. Monitor Lambda execution duration
4. Set up billing alerts

#### Lambda Cold Starts
```bash
Functions taking too long to start
```

**Solution:**
1. Use provisioned concurrency for critical functions
2. Optimize function size and dependencies
3. Consider keeping functions warm with scheduled events

### 🐛 Tool-Specific Issues

#### Weather API Errors
```bash
Failed to get weather data: API key invalid
```

**Solution:**
1. Verify OpenWeather API key in parameters
2. Check API key quota and usage
3. Ensure correct API version

#### Slack Integration Failures
```bash
Slack API returned error: invalid_token
```

**Solution:**
1. Check Slack bot token validity
2. Verify bot permissions in Slack workspace
3. Ensure token format is correct (starts with xoxb-)

#### Odoo Connection Issues
```bash
Connection refused to Odoo instance
```

**Solution:**
1. Check Odoo URL and credentials
2. Verify network connectivity to Odoo
3. Check Odoo API module is installed

### 🔍 Debugging Tips

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Test Individual Functions
```python
import asyncio
from handlers.weather import WeatherHandler

handler = WeatherHandler()
result = asyncio.run(handler.get_weather_data("New York"))
print(result)
```

#### Check CloudWatch Logs
```bash
aws logs tail /aws/lambda/mcp-office-assistant-dev-tool-executor --follow
```

#### Validate JSON Responses
```python
import json
try:
    data = json.loads(response)
    print("Valid JSON:", data)
except json.JSONDecodeError as e:
    print("Invalid JSON:", e)
```

### 📞 Getting Help

1. **Check CloudWatch logs** for detailed error messages
2. **Verify configuration** in parameter files
3. **Test components individually** to isolate issues
4. **Check AWS service status** for regional outages
5. **Review recent changes** that might have caused issues

### 🔧 Useful Commands

```bash
# Check AWS credentials
aws sts get-caller-identity

# View CloudFormation stack status
aws cloudformation describe-stacks --stack-name mcp-office-assistant-dev

# Test API endpoint
curl -X GET "https://api-url/tools" -H "x-api-key: your-key"

# View Lambda logs
aws logs tail /aws/lambda/function-name --follow

# Check S3 bucket contents
aws s3 ls s3://bucket-name --recursive
```
