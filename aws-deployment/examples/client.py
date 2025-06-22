#!/usr/bin/env python3
"""
MCP Office Assistant API Client Example
=======================================

Example client for interacting with the deployed MCP Office Assistant API.
"""

import json
import requests
from typing import Any, Dict, List, Optional


class MCPClient:
    """Client for MCP Office Assistant API."""
    
    def __init__(self, api_url: str, api_key: str, project_id: Optional[str] = None):
        """
        Initialize the MCP client.
        
        Args:
            api_url: Base URL of the API Gateway
            api_key: API key for authentication
            project_id: Optional project ID for multi-tenant usage
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.project_id = project_id
        
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        if self.project_id:
            self.headers['X-Project-ID'] = self.project_id
    
    def list_tools(self) -> Dict[str, Any]:
        """
        List all available tools.
        
        Returns:
            Dictionary containing available tools
        """
        url = f"{self.api_url}/tools"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to list tools: {str(e)}"}
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific tool.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
            
        Returns:
            Tool execution result
        """
        url = f"{self.api_url}/tools/{tool_name}"
        
        try:
            response = requests.post(url, headers=self.headers, json=kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to execute tool {tool_name}: {str(e)}"}
    
    # Convenience methods for specific tools
    
    def get_weather(self, location: str = "Whitehorse") -> Dict[str, Any]:
        """Get weather data for a location."""
        return self.execute_tool("get_weather_data", location_name=location)
    
    def google_search(self, query: str, **options) -> Dict[str, Any]:
        """Perform a Google search."""
        return self.execute_tool("google_search", search_term=query, **options)
    
    def browse_urls(self, urls: List[str], full_text: bool = False) -> Dict[str, Any]:
        """Browse and extract content from URLs."""
        return self.execute_tool("browse_internet", urls=urls, full_text=full_text)
    
    def shorten_url(self, url: str, custom_code: Optional[str] = None) -> Dict[str, Any]:
        """Shorten a URL."""
        return self.execute_tool("shorten_url", url=url, custom_code=custom_code)
    
    def search_amazon(self, query: str, country: str = "CA", **options) -> Dict[str, Any]:
        """Search Amazon products."""
        return self.execute_tool("search_amazon_products", query=query, country=country, **options)
    
    def create_pdf(self, text: str, chat_id: str, title: str, ts: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to PDF and upload to Slack."""
        return self.execute_tool("send_as_pdf", text=text, chat_id=chat_id, title=title, ts=ts)
    
    def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> Dict[str, Any]:
        """Generate text embedding."""
        return self.execute_tool("get_embedding", text=text, model=model)
    
    def solve_math(self, code: str, **params) -> Dict[str, Any]:
        """Execute mathematical calculations."""
        return self.execute_tool("solve_maths", code=code, **params)
    
    def ask_openai(self, prompt: str) -> Dict[str, Any]:
        """Query OpenAI O1 model."""
        return self.execute_tool("ask_openai_o1", prompt=prompt)
    
    def get_users(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get user information."""
        return self.execute_tool("get_users", user_id=user_id)
    
    def get_channels(self, channel_id: Optional[str] = None) -> Dict[str, Any]:
        """Get channel information."""
        return self.execute_tool("get_channels", id=channel_id)


def main():
    """Example usage of the MCP client."""
    
    # Configuration - replace with your actual values
    API_URL = "https://your-api-id.execute-api.us-west-2.amazonaws.com/dev"
    API_KEY = "your-api-key-here"
    PROJECT_ID = "project-a"  # Optional
    
    # Initialize client
    client = MCPClient(API_URL, API_KEY, PROJECT_ID)
    
    print("🚀 MCP Office Assistant API Client Example")
    print("=" * 50)
    
    # Example 1: List available tools
    print("\n📋 Listing available tools...")
    tools_response = client.list_tools()
    
    if "error" in tools_response:
        print(f"❌ Error: {tools_response['error']}")
        return
    
    tools = tools_response.get("tools", [])
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools[:5]:  # Show first 5 tools
        print(f"   • {tool['name']}: {tool['description']}")
    
    if len(tools) > 5:
        print(f"   ... and {len(tools) - 5} more tools")
    
    # Example 2: Get weather data
    print("\n🌤️  Getting weather data...")
    weather_response = client.get_weather("London")
    
    if weather_response.get("status") == "success":
        print("✅ Weather data retrieved successfully")
        # Extract some weather info from the response
        try:
            data = weather_response.get("data", {})
            if isinstance(data, dict) and "temperature" in data:
                print(f"   Temperature: {data.get('temperature', 'N/A')}")
                print(f"   Humidity: {data.get('humidity', 'N/A')}")
        except:
            print("   Weather data format differs from expected")
    else:
        print(f"❌ Weather request failed: {weather_response}")
    
    # Example 3: Perform a Google search
    print("\n🔍 Performing Google search...")
    search_response = client.google_search("OpenAI GPT-4", after="2024-01-01")
    
    if search_response.get("status") == "success":
        print("✅ Search completed successfully")
        data = search_response.get("data", {})
        if isinstance(data, dict) and "content" in data:
            content_items = data["content"]
            print(f"   Found {len(content_items)} content items")
        else:
            print("   Search results in different format")
    else:
        print(f"❌ Search failed: {search_response}")
    
    # Example 4: Browse a webpage
    print("\n🌐 Browsing webpage...")
    browse_response = client.browse_urls(["https://httpbin.org/json"])
    
    if browse_response.get("status") == "success":
        print("✅ Webpage browsed successfully")
    else:
        print(f"❌ Browse failed: {browse_response}")
    
    # Example 5: Search Amazon products
    print("\n🛒 Searching Amazon products...")
    amazon_response = client.search_amazon("wireless headphones", country="US", max_products=3)
    
    if amazon_response.get("status") == "success":
        print("✅ Amazon search completed")
        data = amazon_response.get("data", {})
        if isinstance(data, str):
            # Formatted string response
            lines = data.split('\n')
            print(f"   {lines[0] if lines else 'Products found'}")
        elif isinstance(data, dict) and "products" in data:
            # Structured response
            products = data["products"]
            print(f"   Found {len(products)} products")
    else:
        print(f"❌ Amazon search failed: {amazon_response}")
    
    # Example 6: Mathematical calculation
    print("\n🧮 Performing mathematical calculation...")
    math_code = """
import math
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius
result = f"Circle with radius {radius}: area={area:.2f}, circumference={circumference:.2f}"
"""
    
    math_response = client.solve_math(math_code)
    
    if math_response.get("status") == "success":
        print("✅ Mathematical calculation completed")
        data = math_response.get("data", {})
        if "result" in data:
            variables = data["result"]
            if "result" in variables:
                print(f"   Result: {variables['result']}")
    else:
        print(f"❌ Math calculation failed: {math_response}")
    
    # Example 7: Generate text embedding
    print("\n🤖 Generating text embedding...")
    embedding_response = client.get_embedding("Hello, this is a test sentence for embedding.")
    
    if embedding_response.get("status") == "success":
        print("✅ Embedding generated successfully")
        data = embedding_response.get("data", {})
        if "embedding_length" in data:
            print(f"   Embedding dimension: {data['embedding_length']}")
    else:
        print(f"❌ Embedding generation failed: {embedding_response}")
    
    print("\n🎉 Example completed!")
    print("\n💡 Tips:")
    print("   • Replace API_URL and API_KEY with your actual values")
    print("   • Check CloudFormation outputs for your API details")
    print("   • Use different PROJECT_IDs for multi-tenant access")
    print("   • Add error handling for production usage")


def interactive_mode():
    """Interactive mode for testing tools."""
    print("🔧 Interactive MCP Client")
    print("=" * 30)
    
    # Get configuration from user
    api_url = input("Enter API Gateway URL: ").strip()
    api_key = input("Enter API Key: ").strip()
    project_id = input("Enter Project ID (optional): ").strip() or None
    
    if not api_url or not api_key:
        print("❌ API URL and API Key are required")
        return
    
    client = MCPClient(api_url, api_key, project_id)
    
    while True:
        print("\n" + "="*50)
        print("Available commands:")
        print("1. list - List all tools")
        print("2. weather <location> - Get weather")
        print("3. search <query> - Google search")
        print("4. amazon <query> - Amazon search")
        print("5. math <code> - Execute math code")
        print("6. custom <tool_name> <json_args> - Execute custom tool")
        print("7. quit - Exit")
        
        command = input("\nEnter command: ").strip().split(maxsplit=1)
        
        if not command:
            continue
            
        cmd = command[0].lower()
        args = command[1] if len(command) > 1 else ""
        
        if cmd == "quit":
            break
        elif cmd == "list":
            response = client.list_tools()
            if "tools" in response:
                for tool in response["tools"]:
                    print(f"• {tool['name']}: {tool['description']}")
            else:
                print(f"Error: {response}")
        
        elif cmd == "weather":
            location = args or "Whitehorse"
            response = client.get_weather(location)
            print(json.dumps(response, indent=2))
        
        elif cmd == "search":
            if not args:
                print("❌ Search query required")
                continue
            response = client.google_search(args)
            print(json.dumps(response, indent=2))
        
        elif cmd == "amazon":
            if not args:
                print("❌ Search query required")
                continue
            response = client.search_amazon(args)
            print(json.dumps(response, indent=2))
        
        elif cmd == "math":
            if not args:
                print("❌ Math code required")
                continue
            response = client.solve_math(args)
            print(json.dumps(response, indent=2))
        
        elif cmd == "custom":
            parts = args.split(maxsplit=1)
            if len(parts) != 2:
                print("❌ Usage: custom <tool_name> <json_args>")
                continue
            
            tool_name, json_args = parts
            try:
                tool_args = json.loads(json_args)
                response = client.execute_tool(tool_name, **tool_args)
                print(json.dumps(response, indent=2))
            except json.JSONDecodeError:
                print("❌ Invalid JSON arguments")
        
        else:
            print(f"❌ Unknown command: {cmd}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()