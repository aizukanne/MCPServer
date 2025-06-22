"""
Documentation Templates
=======================

Templates for documentation files like API reference, troubleshooting guide, etc.
"""


class DocumentationTemplates:
    """Documentation file templates."""
    
    def get_api_reference(self) -> str:
        """Get API reference documentation."""
        return '''# MCP Office Assistant - API Reference

## Overview

The MCP Office Assistant provides 26 tools across 8 categories for comprehensive office automation.

## Tool Categories

### 🌤️ Weather Tools

#### get_weather_data
Get current weather information for any location.

**Parameters:**
- `location_name` (string, optional): Location name (default: "Whitehorse")

**Example:**
```python
client.get_weather("New York")
```

#### get_coordinates  
Get latitude and longitude coordinates for a location.

**Parameters:**
- `location_name` (string, required): Location name

**Example:**
```python
client.execute_tool("get_coordinates", location_name="London")
```

### 🌐 Web Browsing Tools

#### google_search
Perform advanced Google search with operators.

**Parameters:**
- `search_term` (string, required): Main search query
- `before` (string, optional): Date before (YYYY-MM-DD)
- `after` (string, optional): Date after (YYYY-MM-DD)  
- `intext` (string, optional): Text that must appear in content
- `allintext` (string, optional): All terms that must appear
- `and_condition` (string, optional): Additional AND term
- `must_have` (string, optional): Exact phrase required

**Example:**
```python
client.google_search("AI research", after="2024-01-01", intext="GPT")
```

#### browse_internet
Extract content from web pages.

**Parameters:**
- `urls` (array, required): List of URLs to browse
- `full_text` (boolean, optional): Return full text vs summary

**Example:**
```python
client.browse_urls(["https://example.com", "https://news.com"])
```

#### shorten_url
Create shortened URLs.

**Parameters:**
- `url` (string, required): URL to shorten
- `custom_code` (string, optional): Custom short code

**Example:**
```python
client.shorten_url("https://very-long-url.com/path")
```

### 💾 Storage & Messages

#### get_message_by_sort_id
Retrieve specific message by ID.

#### get_messages_in_range
Get messages within time range.

#### get_users
Get user information.

#### get_channels
Get channel information.

#### manage_mute_status
Manage channel mute status.

### 💬 Slack Integration

#### send_file_to_slack
Upload files to Slack.

#### update_slack_users
Sync user data from Slack.

#### update_slack_conversations  
Sync channel data from Slack.

### 🏢 Odoo ERP Integration

#### odoo_get_mapped_models
Get available Odoo models.

#### odoo_fetch_records
Retrieve Odoo records.

#### odoo_create_record
Create new Odoo record.

#### odoo_update_record
Update existing Odoo record.

#### odoo_delete_record
Delete Odoo record.

#### odoo_print_record
Generate PDF report for Odoo record.

#### odoo_post_record
Post Odoo record (change status).

### 🛒 Amazon Integration

#### search_amazon_products
Search Amazon marketplace.

#### search_and_format_products
Search Amazon with formatted results.

### 📄 Document Management

#### send_as_pdf
Convert text to PDF and upload to Slack.

#### list_files
List files in S3 bucket.

#### get_embedding
Generate text embeddings.

### 🔧 Utilities

#### solve_maths
Execute mathematical calculations.

#### ask_openai_o1
Query OpenAI O1 model.

## Response Format

All tools return responses in this format:

```json
{
  "status": "success|error",
  "data": { ... },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Authentication

### API Key Authentication
Include in headers:
```
x-api-key: your-api-key-here
```

### Project Identification (Optional)
Include for multi-tenant usage:
```
X-Project-ID: project-name
```

## Rate Limits

- **Default**: 50 requests/second, 10,000/month
- **Burst**: Up to 100 requests in short periods
- **Per-project**: Limits apply per API key

## Error Codes

- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid API key)
- `404` - Tool not found
- `429` - Rate limit exceeded
- `500` - Internal server error
'''
    
    def get_troubleshooting_guide(self) -> str:
        """Get troubleshooting guide."""
        return '''# Troubleshooting Guide

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
'''
    
    def get_changelog(self) -> str:
        """Get changelog template."""
        return '''# Changelog

All notable changes to the MCP Office Assistant project will be documented in this file.

## [1.0.0] - 2024-01-XX - Initial Release

### Added
- ✨ Complete MCP server implementation with 26 tools
- 🌤️ Weather tools (OpenWeather API integration)
- 🌐 Web browsing tools (Google search, URL browsing, shortening)
- 💾 Storage and message management tools
- 💬 Slack integration (file uploads, user sync)
- 🏢 Odoo ERP integration (full CRUD operations)
- 🛒 Amazon product search integration
- 📄 Document management (PDF generation, S3 storage)
- 🔧 Utility tools (math calculations, OpenAI queries)
- ☁️ AWS Lambda deployment infrastructure
- 📚 Comprehensive documentation and examples

### Infrastructure
- 🏗️ CloudFormation template for AWS deployment
- 🚀 Automated deployment scripts
- 🔑 Multi-project API key management
- 📊 CloudWatch monitoring and logging
- 🔒 Security best practices and IAM roles
- 💰 Cost-optimized Lambda functions

### Documentation
- 📖 Complete setup and deployment guides
- 🔧 Troubleshooting documentation
- 💻 Client examples in Python and JavaScript
- 📋 API reference documentation
- 🎯 Integration guide for existing projects

## [Unreleased]

### Planned Features
- 🔄 Enhanced error handling and retry logic
- 📈 Advanced monitoring and alerting
- 🎨 Additional client SDKs (Go, Java)
- 🔌 Plugin system for custom tools
- 📱 Mobile-friendly API clients
- 🌍 Additional language support

### Known Issues
- Lambda cold start times on first request
- Large file processing timeouts in some regions
- Rate limiting could be more granular

## Version History

### Version Naming Convention
- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes or significant new features
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes and minor improvements

### Release Types
- 🎉 **Major Release**: New major features or breaking changes
- ✨ **Feature Release**: New tools or significant enhancements
- 🐛 **Bugfix Release**: Bug fixes and stability improvements
- 🔒 **Security Release**: Security updates and patches

### Support Policy
- **Current Version**: Full support and active development
- **Previous Major**: Security updates for 6 months
- **Legacy Versions**: Community support only

### Migration Guide
When upgrading between major versions:
1. Review breaking changes in changelog
2. Update configuration files as needed
3. Test in development environment first
4. Update client applications if needed
5. Deploy to staging before production

### Contributing
To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Feedback
We welcome feedback and suggestions:
- 🐛 Bug reports: Use GitHub issues
- 💡 Feature requests: Use GitHub discussions
- 📧 Direct contact: [your-email]
- 📖 Documentation improvements: Submit PRs
'''
    
    def get_deployment_comparison(self) -> str:
        """Get deployment comparison documentation."""
        return '''# Deployment Options Comparison

## Overview

The MCP Office Assistant supports two deployment architectures, each with distinct advantages.

## 🏠 Local MCP Server vs ☁️ AWS Lambda

| Aspect | Local MCP Server | AWS Lambda |
|--------|------------------|------------|
| **Protocol** | Native MCP over WebSocket | REST API over HTTPS |
| **Scaling** | Single instance | Auto-scaling |
| **Cost** | Server hosting costs | Pay-per-request |
| **Latency** | Very low (local) | Low (network dependent) |
| **Availability** | Depends on server uptime | 99.9% AWS SLA |
| **Setup Complexity** | Simple | Moderate |
| **Multi-Project** | Requires custom routing | Built-in API keys |
| **Maintenance** | Manual updates | Managed infrastructure |

## 🎯 When to Choose Each Option

### Choose Local MCP Server When:
- **Direct MCP Protocol**: Your AI application requires native MCP
- **Low Latency**: Sub-millisecond response times needed
- **Development**: Local testing and development
- **Simple Setup**: Quick start without cloud complexity
- **Private Network**: Tools must stay within private network
- **Custom Protocol**: Need WebSocket or specific MCP features

### Choose AWS Lambda When:
- **Multiple Projects**: Serving multiple teams/applications
- **High Availability**: Need 99.9%+ uptime
- **Auto-Scaling**: Variable or unpredictable load
- **Cost Optimization**: Pay only for actual usage
- **Global Access**: Worldwide API access needed
- **Zero Maintenance**: Prefer managed infrastructure
- **REST API**: Client applications prefer HTTP/REST

## 📊 Performance Comparison

### Local MCP Server
```
Cold Start: None (always running)
Response Time: 10-50ms (local network)
Throughput: Limited by server resources
Concurrent Users: Depends on server capacity
Memory Usage: Full application in memory
```

### AWS Lambda
```
Cold Start: 1-3 seconds (first request)
Response Time: 100-500ms (including network)
Throughput: Virtually unlimited
Concurrent Users: 1000+ concurrent executions
Memory Usage: Per-function optimization
```

## 💰 Cost Analysis

### Local MCP Server Costs
- **Server**: $20-100/month (VPS/dedicated)
- **Bandwidth**: Usually included
- **Maintenance**: Developer time
- **Scaling**: Additional servers needed

### AWS Lambda Costs
- **Requests**: $0.20 per 1M requests
- **Compute**: $0.0000166667 per GB-second
- **API Gateway**: $3.50 per 1M API calls
- **Storage**: S3 and DynamoDB usage

### Cost Examples (Monthly)
| Usage Level | Local Server | AWS Lambda |
|-------------|--------------|------------|
| **Light** (1K requests) | $25-50 | $0.50-2 |
| **Medium** (10K requests) | $25-50 | $2-5 |
| **Heavy** (100K requests) | $50-100+ | $10-20 |
| **Enterprise** (1M requests) | $100-500+ | $50-100 |

## 🔧 Feature Comparison

### Both Options Support:
- ✅ All 26 MCP tools
- ✅ Same business logic
- ✅ Identical functionality
- ✅ Security and validation
- ✅ Error handling
- ✅ Logging and monitoring

### Local MCP Server Exclusive:
- 🔌 Native MCP protocol
- ⚡ WebSocket connections
- 🏠 Local file system access
- 🔐 Network isolation
- 🛠️ Direct debugging

### AWS Lambda Exclusive:
- 🔑 Built-in API key management
- 🌍 Global edge locations
- 📊 CloudWatch integration
- 🔄 Auto-scaling
- 💾 Managed database integration
- 🏗️ Infrastructure as Code

## 🚀 Migration Path

### From Local to AWS
1. **Test AWS deployment** alongside local
2. **Update client applications** to use REST API
3. **Migrate data** to AWS services (S3, DynamoDB)
4. **Switch DNS/endpoints** to AWS
5. **Decommission** local server

### From AWS to Local
1. **Deploy local MCP server**
2. **Export data** from AWS services
3. **Update client applications** to use MCP protocol
4. **Test thoroughly** in local environment
5. **Clean up** AWS resources

## 🎛️ Hybrid Approach

You can run both simultaneously:

```
Development → Local MCP Server (fast iteration)
Staging → AWS Lambda (production-like testing)
Production → AWS Lambda (high availability)
```

Or use different options for different use cases:

```
Internal Tools → Local MCP Server
Customer-Facing → AWS Lambda
```

## 📋 Decision Matrix

Rate each factor from 1-5 based on your needs:

| Factor | Weight | Local Score | AWS Score |
|--------|--------|-------------|-----------|
| **Cost Sensitivity** | ___ | 3 | 5 |
| **Setup Simplicity** | ___ | 5 | 3 |
| **Scalability Needs** | ___ | 2 | 5 |
| **Latency Requirements** | ___ | 5 | 4 |
| **Availability Needs** | ___ | 3 | 5 |
| **Multi-Project Support** | ___ | 2 | 5 |
| **Maintenance Preference** | ___ | 2 | 5 |

**Calculate**: (Weight × Score) for each option and compare totals.

## 🎯 Recommendation

### For Most Users: **AWS Lambda**
- Better long-term value
- Easier multi-project support
- Higher reliability
- Lower maintenance overhead

### For Specific Cases: **Local MCP Server**
- Need native MCP protocol
- Extremely latency-sensitive
- Private network requirements
- Simple single-user setup

### For Enterprises: **Both**
- Local for development
- AWS for production
- Best of both worlds

## 🔄 Next Steps

1. **Assess your requirements** using the decision matrix
2. **Start with local development** to test functionality
3. **Deploy AWS version** for production scaling
4. **Monitor costs and performance** to optimize
5. **Consider hybrid approach** for complex needs
'''