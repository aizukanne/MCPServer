#!/bin/bash

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
