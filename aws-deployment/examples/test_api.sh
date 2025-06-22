#!/bin/bash

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
RESPONSE=$(curl -s -X GET "$API_URL/tools" \
  -H "x-api-key: $API_KEY" \
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
RESPONSE=$(curl -s -X POST "$API_URL/tools/get_weather_data" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location_name": "London"}')

if echo "$RESPONSE" | grep -q '"status": "success"'; then
    echo "✅ Weather tool working"
else
    echo "❌ Weather tool failed"
    echo "Response: $RESPONSE"
fi

echo ""
echo "3. 🧮 Testing math tool..."
RESPONSE=$(curl -s -X POST "$API_URL/tools/solve_maths" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "result = 2 + 2\nprint(f\"Answer: {result}\")"}')

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
