#!/usr/bin/env python3
"""Test script to verify config fixes"""

print("Testing config fixes...")

# Test 1: Check if dotenv can be imported and used
try:
    from dotenv import load_dotenv
    import os
    
    # Load .env file
    load_dotenv()
    
    print("✓ dotenv loaded successfully")
    print(f"  AWS_DEFAULT_REGION from env: {os.getenv('AWS_DEFAULT_REGION', 'not set')}")
except ImportError as e:
    print(f"✗ Failed to import dotenv: {e}")
    print("  Note: You may need to install python-dotenv or activate your virtual environment")

# Test 2: Check if boto3 can create DynamoDB resource with region
try:
    import boto3
    
    # Test creating DynamoDB resource with region
    region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    
    print(f"✓ boto3 DynamoDB resource created successfully with region: {region}")
except Exception as e:
    print(f"✗ Failed to create DynamoDB resource: {e}")

# Test 3: Show the actual changes made
print("\nChanges implemented:")
print("1. Local config.py:")
print("   - Added: from dotenv import load_dotenv")
print("   - Added: load_dotenv() to load .env file")
print("   - Changed: dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'))")
print("\n2. AWS config.py (aws-deployment/src/config.py):")
print("   - Changed: dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'))")
print("   - No dotenv loading (uses Lambda environment variables)")

print("\nTo use this fix:")
print("1. Make sure AWS_DEFAULT_REGION is set in your .env file")
print("2. Activate your virtual environment: source .venv/bin/activate")
print("3. Run your application")