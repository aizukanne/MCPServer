"""
Shell Script Templates
======================

Templates for various shell scripts used in the project.
"""


class ScriptTemplates:
    """Shell script templates."""
    
    def get_setup_script(self) -> str:
        """Get environment setup script."""
        return '''#!/bin/bash

echo "🚀 Setting up AWS deployment environment..."

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v aws >/dev/null 2>&1; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
    echo "   Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

if ! command -v sam >/dev/null 2>&1; then
    echo -e "${RED}❌ SAM CLI not found. Please install SAM CLI first.${NC}"
    echo "   Install: pip install aws-sam-cli"
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo -e "${RED}❌ AWS credentials not configured.${NC}"
    echo "   Run: aws configure"
    echo "   You need: Access Key ID, Secret Access Key, Region"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites check passed!${NC}"

# Install Python dependencies
echo "Installing additional Python dependencies..."
pip install boto3 requests aiohttp beautifulsoup4

echo -e "${GREEN}✅ Environment setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update parameter files with your API keys:"
echo "   - cloudformation/parameters-dev.json"
echo "   - cloudformation/parameters-staging.json"  
echo "   - cloudformation/parameters-prod.json"
echo ""
echo "2. Deploy to AWS:"
echo "   ./deploy.sh dev us-west-2 deploy"
echo ""
echo "3. Test deployment:"
echo "   python examples/client.py"
'''
    
    def get_test_script(self) -> str:
        """Get API testing script."""
        return '''#!/bin/bash

# Test script for the deployed MCP API
API_URL="$1"
API_KEY="$2"

if [ -z "$API_URL" ] || [ -z "$API_KEY" ]; then
    echo "Usage: $0 <API_URL> <API_KEY>"
    echo "Example: $0 https://abc123.execute-api.us-west-2.amazonaws.com/dev your-api-key"
    exit 1
fi

echo "🧪 Testing MCP Office Assistant API"
echo "=================================="

# Test 1: List tools
echo "1. 📋 Listing available tools..."
RESPONSE=$(curl -s -X GET "$API_URL/tools" \\
  -H "x-api-key: $API_KEY" \\
  -H "Content-Type: application/json")

if echo "$RESPONSE" | grep -q '"status": "success"'; then
    echo "✅ Tools list endpoint working"
    TOOL_COUNT=$(echo "$RESPONSE" | jq -r '.tools | length' 2>/dev/null || echo "unknown")
    echo "   Found $TOOL_COUNT tools"
else
    echo "❌ Tools list endpoint failed"
    echo "Response: $RESPONSE"
fi

echo ""
echo "2. 🌤️ Testing weather tool..."
RESPONSE=$(curl -s -X POST "$API_URL/tools/get_weather_data" \\
  -H "x-api-key: $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"location_name": "London"}')

if echo "$RESPONSE" | grep -q '"status": "success"'; then
    echo "✅ Weather tool working"
else
    echo "❌ Weather tool failed"
    echo "Response: $RESPONSE"
fi

echo ""
echo "3. 🧮 Testing math tool..."
RESPONSE=$(curl -s -X POST "$API_URL/tools/solve_maths" \\
  -H "x-api-key: $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"code": "result = 2 + 2\\nprint(f\\"Answer: {result}\\")"}')

if echo "$RESPONSE" | grep -q '"status": "success"'; then
    echo "✅ Math tool working"
else
    echo "❌ Math tool failed"
    echo "Response: $RESPONSE"
fi

echo ""
echo "🎉 API tests completed!"
echo ""
echo "📊 Full test with Python client:"
echo "python examples/client.py"
'''
    
    def get_cleanup_script(self) -> str:
        """Get cleanup script."""
        return '''#!/bin/bash

ENVIRONMENT=${1:-dev}
REGION=${2:-us-west-2}

echo "🧹 Cleaning up MCP Office Assistant deployment..."
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

STACK_NAME="mcp-office-assistant-$ENVIRONMENT"

# Get S3 bucket name and empty it
echo "🗑️ Emptying S3 bucket..."
BUCKET_NAME=$(aws cloudformation describe-stacks \\
  --stack-name $STACK_NAME \\
  --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucket`].OutputValue' \\
  --output text \\
  --region $REGION 2>/dev/null)

if [ ! -z "$BUCKET_NAME" ] && [ "$BUCKET_NAME" != "None" ]; then
  echo "Emptying S3 bucket: $BUCKET_NAME"
  aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION 2>/dev/null || true
else
  echo "No S3 bucket found or already empty"
fi

# Delete CloudFormation stack
echo "🗂️ Deleting CloudFormation stack: $STACK_NAME"
aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION

echo "✅ Cleanup initiated. Stack deletion may take several minutes."
echo "💡 Monitor progress in AWS Console or run:"
echo "   aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION"
'''
    
    def get_copy_script(self) -> str:
        """Get artifact copying script."""
        return '''#!/bin/bash

# MCP Office Assistant - File Copy Script
# This script helps you copy files from downloaded artifacts

echo "🚀 MCP Office Assistant - File Copy Helper"
echo "=========================================="

# Check if artifacts directory exists
if [ ! -d "artifacts" ]; then
    echo "❌ Please create an 'artifacts' directory and place your downloaded artifact files there"
    echo "   Expected structure:"
    echo "   artifacts/"
    echo "   ├── cloudformation-template.yaml"
    echo "   ├── lambda-handlers.py" 
    echo "   ├── specialized-handlers.py"
    echo "   ├── deploy-script.sh"
    echo "   ├── sam-config.toml"
    echo "   ├── client-example.py"
    echo "   ├── aws-deployment-guide.md"
    echo "   ├── handlers/ (directory with 8 .py files)"
    echo "   ├── services/ (directory with 8 .py files)"
    echo "   ├── schemas/ (directory with 1 .py file)"
    echo "   └── utils/ (directory with 3 .py files)"
    exit 1
fi

echo "📁 Copying artifact files to correct locations..."

# Copy main AWS deployment files
[ -f "artifacts/cloudformation-template.yaml" ] && cp "artifacts/cloudformation-template.yaml" "aws-deployment/cloudformation/mcp-infrastructure.yaml"
[ -f "artifacts/lambda-handlers.py" ] && cp "artifacts/lambda-handlers.py" "aws-deployment/src/lambda_handlers.py"
[ -f "artifacts/specialized-handlers.py" ] && cp "artifacts/specialized-handlers.py" "aws-deployment/src/specialized_handlers.py"
[ -f "artifacts/deploy-script.sh" ] && cp "artifacts/deploy-script.sh" "aws-deployment/deploy.sh" && chmod +x "aws-deployment/deploy.sh"
[ -f "artifacts/sam-config.toml" ] && cp "artifacts/sam-config.toml" "aws-deployment/samconfig.toml"
[ -f "artifacts/client-example.py" ] && cp "artifacts/client-example.py" "aws-deployment/examples/client.py"
[ -f "artifacts/aws-deployment-guide.md" ] && cp "artifacts/aws-deployment-guide.md" "aws-deployment/AWS_DEPLOYMENT_GUIDE.md"

# Copy handlers, services, schemas, utils
[ -d "artifacts/handlers" ] && cp -r "artifacts/handlers/"* "handlers/" && cp -r "artifacts/handlers/"* "aws-deployment/src/handlers/"
[ -d "artifacts/services" ] && cp -r "artifacts/services/"* "services/" && cp -r "artifacts/services/"* "aws-deployment/src/services/"
[ -d "artifacts/schemas" ] && cp -r "artifacts/schemas/"* "schemas/" && cp -r "artifacts/schemas/"* "aws-deployment/src/schemas/"
[ -d "artifacts/utils" ] && cp -r "artifacts/utils/"* "utils/" && cp -r "artifacts/utils/"* "aws-deployment/src/utils/"

# Copy existing config files to AWS deployment
[ -f "config.py" ] && cp "config.py" "aws-deployment/src/"
[ -f "url_shortener.py" ] && cp "url_shortener.py" "aws-deployment/src/"

echo "✅ Files copied successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update API keys in aws-deployment/cloudformation/parameters-*.json"
echo "2. Test locally: python main.py"
echo "3. Deploy to AWS: cd aws-deployment && ./deploy.sh dev us-west-2 deploy"
echo "4. Test deployment: python aws-deployment/examples/client.py"
'''