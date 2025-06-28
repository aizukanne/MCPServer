# Deployment

This guide provides instructions for deploying the MCP Office Assistant Server to different environments.

## Local Deployment

For local development and testing, you can run the server directly from the command line:

```bash
python main.py
```

## Docker Deployment

To deploy the server using Docker, you can use the provided `Dockerfile`:

```bash
# Build the Docker image
docker build -t mcp-office-assistant .

# Run the Docker container
docker run -p 8000:8000 --env-file .env mcp-office-assistant
```

## AWS Deployment

For production deployments, we recommend using AWS. The `aws-deployment` directory contains all the necessary files and scripts for deploying the server to AWS Lambda and API Gateway.

Refer to the [AWS Deployment Guide](../aws-deployment/AWS_DEPLOYMENT_GUIDE.md) for detailed instructions.