#!/usr/bin/env python3
"""
Test script to verify the Google search fix
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from handlers.web_browsing import WebBrowsingHandler


async def test_google_search():
    """Test the Google search functionality"""
    print("Testing Google Search Fix...")
    print("-" * 50)
    
    # Check if API credentials are set
    if not os.getenv('CUSTOM_SEARCH_API_KEY') or not os.getenv('CUSTOM_SEARCH_ID'):
        print("ERROR: Google Custom Search API credentials not configured")
        print("Please set CUSTOM_SEARCH_API_KEY and CUSTOM_SEARCH_ID environment variables")
        return
    
    # Initialize handler
    handler = WebBrowsingHandler()
    
    # Test search
    search_term = "Alexander Pope"
    print(f"Searching for: {search_term}")
    print("-" * 50)
    
    try:
        result = await handler.google_search(search_term)
        
        # Parse the result
        import json
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            content_items = result_data.get('data', {}).get('content', [])
            
            print(f"Found {len(content_items)} results\n")
            
            for i, item in enumerate(content_items, 1):
                print(f"Result {i}:")
                print(f"  URL: {item.get('url', 'N/A')}")
                print(f"  Type: {item.get('type', 'N/A')}")
                
                if item.get('type') == 'error':
                    # Check if it's still returning HTML in error field
                    error_content = item.get('error', '')
                    if error_content.startswith('<!DOCTYPE'):
                        print(f"  ❌ STILL BROKEN: HTML content in error field")
                        print(f"  Error preview: {error_content[:100]}...")
                    else:
                        print(f"  Error: {error_content}")
                elif item.get('type') == 'content':
                    summary = item.get('summary', '')
                    if summary:
                        print(f"  ✅ SUCCESS: Content properly extracted")
                        print(f"  Summary preview: {summary[:200]}...")
                        print(f"  Author: {item.get('author', 'Unknown')}")
                        print(f"  Date: {item.get('date_published', 'Unknown')}")
                    else:
                        print(f"  ⚠️  WARNING: No summary extracted")
                
                print()
        else:
            print(f"Search failed: {result_data.get('error', {}).get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the test
    asyncio.run(test_google_search())