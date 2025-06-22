#!/bin/bash

ENVIRONMENT=${1:-dev}
REGION=${2:-us-west-2}

echo "🧹 Cleaning up MCP Office Assistant deployment..."
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

STACK_NAME="mcp-office-assistant-$ENVIRONMENT"

# Get S3 bucket name and empty it
echo "🗑️ Emptying S3 bucket..."
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucket`].OutputValue' \
  --output text \
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
