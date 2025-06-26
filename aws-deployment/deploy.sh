#!/bin/bash

# MCP Office Assistant - AWS Lambda Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="mcp-office-assistant"
DEFAULT_ENVIRONMENT="dev"
DEFAULT_REGION="us-west-2"

# Parse command line arguments
ENVIRONMENT=${1:-$DEFAULT_ENVIRONMENT}
REGION=${2:-$DEFAULT_REGION}
ACTION=${3:-deploy}

echo -e "${BLUE}MCP Office Assistant - AWS Deployment${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "Region: ${YELLOW}$REGION${NC}"
echo -e "Action: ${YELLOW}$ACTION${NC}"
echo

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI not found. Please install AWS CLI first.${NC}"
        exit 1
    fi
    
    # Check SAM CLI
    if ! command -v sam &> /dev/null; then
        echo -e "${RED}SAM CLI not found. Please install SAM CLI first.${NC}"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 not found. Please install Python 3.8+ first.${NC}"
        exit 1
    fi
    
    # Check if authenticated with AWS
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}AWS credentials not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Prerequisites check passed!${NC}"
}

# Create directory structure
setup_directories() {
    echo -e "${BLUE}Setting up directory structure...${NC}"
    
    mkdir -p src
    mkdir -p layers/dependencies/python
    mkdir -p cloudformation
    mkdir -p scripts
    
    # Copy handler files to src
    if [ -d "handlers" ]; then
        cp -r handlers src/
    fi
    
    if [ -d "services" ]; then
        cp -r services src/
    fi
    
    if [ -d "schemas" ]; then
        cp -r schemas src/
    fi
    
    if [ -d "utils" ]; then
        cp -r utils src/
    fi
    
    # Copy existing config and url_shortener
    if [ -f "config.py" ]; then
        cp config.py src/
    fi
    
    if [ -f "url_shortener.py" ]; then
        cp url_shortener.py src/
    fi
    
    echo -e "${GREEN}Directory structure created!${NC}"
}

# Build dependencies layer
build_dependencies() {
    echo -e "${BLUE}Building dependencies layer...${NC}"
    
    # Create requirements.txt for Lambda layer
    cat > layers/dependencies/requirements.txt << EOF
boto3>=1.26.0
requests>=2.28.0
aiohttp>=3.8.0
beautifulsoup4>=4.11.0
weaviate-client>=3.15.0
openai>=1.0.0
fpdf>=2.5.0
markdown2>=2.4.0
pydantic>=2.0.0
nltk>=3.8.0
lxml>=4.9.0
python-dotenv>=1.0.0
EOF

    # Install dependencies to layer
    cd layers/dependencies
    # Check if uv is installed, if not use pip
    if command -v uv &> /dev/null; then
        uv pip install -r requirements.txt --target python/
    else
        pip install -r requirements.txt -t python/
    fi
    
    # Remove unnecessary files to reduce size
    find python/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find python/ -name "*.pyc" -delete 2>/dev/null || true
    find python/ -name "*.so" -exec strip {} + 2>/dev/null || true
    
    cd ../../
    
    echo -e "${GREEN}Dependencies layer built!${NC}"
}

# Package application
package_application() {
    echo -e "${BLUE}Packaging application...${NC}"
    
    # Create SAM template
    sam build --template cloudformation/mcp-infrastructure.yaml
    
    echo -e "${GREEN}Application packaged!${NC}"
}

# Deploy infrastructure
deploy_infrastructure() {
    echo -e "${BLUE}Deploying infrastructure...${NC}"
    
    # Check if parameter file exists
    PARAM_FILE="cloudformation/parameters-${ENVIRONMENT}.json"
    
    if [ ! -f "$PARAM_FILE" ]; then
        echo -e "${YELLOW}Parameter file not found. Creating template...${NC}"
        create_parameter_file
    fi
    
    # Deploy using SAM
    sam deploy \
        --template-file .aws-sam/build/template.yaml \
        --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
        --parameter-overrides file://${PARAM_FILE} \
        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
        --region $REGION \
        --confirm-changeset \
        --resolve-s3
    
    echo -e "${GREEN}Infrastructure deployed!${NC}"
}

# Create parameter file template
create_parameter_file() {
    PARAM_FILE="cloudformation/parameters-${ENVIRONMENT}.json"
    
    cat > $PARAM_FILE << EOF
[
  {
    "ParameterKey": "Environment",
    "ParameterValue": "$ENVIRONMENT"
  },
  {
    "ParameterKey": "ProjectName", 
    "ParameterValue": "$PROJECT_NAME"
  },
  {
    "ParameterKey": "AllowedOrigins",
    "ParameterValue": "*"
  },
  {
    "ParameterKey": "OpenAIApiKey",
    "ParameterValue": "CHANGE_ME"
  },
  {
    "ParameterKey": "SlackBotToken",
    "ParameterValue": "CHANGE_ME"
  },
  {
    "ParameterKey": "OpenWeatherApiKey",
    "ParameterValue": "CHANGE_ME"
  },
  {
    "ParameterKey": "GoogleSearchApiKey",
    "ParameterValue": "CHANGE_ME"
  },
  {
    "ParameterKey": "GoogleSearchEngineId",
    "ParameterValue": "CHANGE_ME"
  }
]
EOF

    echo -e "${YELLOW}Parameter file created at: $PARAM_FILE${NC}"
    echo -e "${YELLOW}Please update the CHANGE_ME values with your actual API keys${NC}"
    read -p "Press Enter to continue after updating the parameter file..."
}

# Get deployment outputs
get_outputs() {
    echo -e "${BLUE}Getting deployment outputs...${NC}"
    
    STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"
    
    # Get API Gateway URL
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
        --output text \
        --region $REGION)
    
    # Get API Keys
    PROJECT_A_KEY=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ProjectAApiKey`].OutputValue' \
        --output text \
        --region $REGION)
    
    PROJECT_B_KEY=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ProjectBApiKey`].OutputValue' \
        --output text \
        --region $REGION)
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo
    echo -e "${BLUE}=== DEPLOYMENT OUTPUTS ===${NC}"
    echo -e "API Gateway URL: ${GREEN}$API_URL${NC}"
    echo -e "Project A API Key: ${GREEN}$PROJECT_A_KEY${NC}"
    echo -e "Project B API Key: ${GREEN}$PROJECT_B_KEY${NC}"
    echo
    echo -e "${BLUE}=== USAGE EXAMPLES ===${NC}"
    echo -e "List tools:"
    echo -e "${YELLOW}curl -X GET \"$API_URL/tools\" -H \"x-api-key: $PROJECT_A_KEY\"${NC}"
    echo
    echo -e "Execute tool:"
    echo -e "${YELLOW}curl -X POST \"$API_URL/tools/get_weather_data\" \\"
    echo -e "  -H \"x-api-key: $PROJECT_A_KEY\" \\"
    echo -e "  -H \"Content-Type: application/json\" \\"
    echo -e "  -d '{\"location_name\": \"New York\"}'${NC}"
    echo
}

# Test deployment
test_deployment() {
    echo -e "${BLUE}Testing deployment...${NC}"
    
    STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"
    
    # Get API URL and key
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
        --output text \
        --region $REGION)
    
    PROJECT_A_KEY=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ProjectAApiKey`].OutputValue' \
        --output text \
        --region $REGION)
    
    echo -e "${BLUE}Testing tools list endpoint...${NC}"
    RESPONSE=$(curl -s -X GET "$API_URL/tools" -H "x-api-key: $PROJECT_A_KEY")
    
    if echo "$RESPONSE" | grep -q "\"status\": \"success\""; then
        echo -e "${GREEN}✓ Tools list endpoint working${NC}"
    else
        echo -e "${RED}✗ Tools list endpoint failed${NC}"
        echo "Response: $RESPONSE"
    fi
    
    echo -e "${BLUE}Testing weather tool...${NC}"
    RESPONSE=$(curl -s -X POST "$API_URL/tools/get_weather_data" \
        -H "x-api-key: $PROJECT_A_KEY" \
        -H "Content-Type: application/json" \
        -d '{"location_name": "London"}')
    
    if echo "$RESPONSE" | grep -q "\"status\": \"success\""; then
        echo -e "${GREEN}✓ Weather tool working${NC}"
    else
        echo -e "${RED}✗ Weather tool failed${NC}"
        echo "Response: $RESPONSE"
    fi
}

# Cleanup deployment
cleanup() {
    echo -e "${BLUE}Cleaning up deployment...${NC}"
    
    STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"
    
    # Empty S3 bucket first
    BUCKET_NAME=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucket`].OutputValue' \
        --output text \
        --region $REGION 2>/dev/null || true)
    
    if [ ! -z "$BUCKET_NAME" ]; then
        echo -e "${BLUE}Emptying S3 bucket: $BUCKET_NAME${NC}"
        aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION 2>/dev/null || true
    fi
    
    # Delete CloudFormation stack
    echo -e "${BLUE}Deleting CloudFormation stack: $STACK_NAME${NC}"
    aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION
    
    echo -e "${GREEN}Cleanup initiated. Stack deletion in progress...${NC}"
}

# Main execution
main() {
    case $ACTION in
        "deploy")
            check_prerequisites
            setup_directories
            build_dependencies
            package_application
            deploy_infrastructure
            get_outputs
            ;;
        "test")
            test_deployment
            ;;
        "cleanup"|"destroy")
            cleanup
            ;;
        "package")
            setup_directories
            build_dependencies
            package_application
            ;;
        *)
            echo -e "${RED}Unknown action: $ACTION${NC}"
            echo "Usage: $0 [environment] [region] [action]"
            echo "Actions: deploy, test, cleanup, package"
            exit 1
            ;;
    esac
}

# Run main function
main

echo -e "${GREEN}Operation completed!${NC}"