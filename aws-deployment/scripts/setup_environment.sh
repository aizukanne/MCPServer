#!/bin/bash

echo "🚀 Setting up AWS deployment environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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
