"""
Web Browsing Tools Handler
==========================

This module contains MCP tool handlers for web browsing and search functions.
"""

import logging
from typing import Any, Dict, List, Optional

from services.web_service import WebService
from utils.formatting import format_search_response, format_web_content_response, format_success_response, format_error_response
from utils.validation import validate_file_path

logger = logging.getLogger(__name__)


class WebBrowsingHandler:
    """Handler for web browsing and search MCP tools."""
    
    def __init__(self):
        """Initialize the web browsing handler."""
        self.web_service = WebService()
    
    async def google_search(
        self,
        search_term: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        intext: Optional[str] = None,
        allintext: Optional[str] = None,
        and_condition: Optional[str] = None,
        must_have: Optional[str] = None
    ) -> str:
        """
        Perform a Google search with advanced operators and return web content.
        
        Args:
            search_term: The main search query
            before: Search for content before this date (YYYY-MM-DD format)
            after: Search for content after this date (YYYY-MM-DD format)
            intext: Search for this text within the page content
            allintext: Search for all these terms within the page content
            and_condition: Additional term that must be present (AND operator)
            must_have: Exact phrase that must be present in results
            
        Returns:
            Formatted search results as JSON string
        """
        try:
            logger.info(f"Performing Google search for: {search_term}")
            
            # Validate input
            if not search_term or not search_term.strip():
                return format_error_response("Search term cannot be empty")
            
            # Perform search
            search_results = await self.web_service.google_search(
                search_term=search_term.strip(),
                before=before,
                after=after,
                intext=intext,
                allintext=allintext,
                and_condition=and_condition,
                must_have=must_have
            )
            
            # Format and return results
            return format_search_response(search_results)
            
        except Exception as e:
            logger.error(f"Error performing Google search: {e}")
            return format_error_response(f"Failed to perform search: {str(e)}")
    
    async def browse_internet(self, urls: List[str], full_text: bool = False) -> str:
        """
        Browse and extract content from a list of URLs.
        
        Args:
            urls: List of URLs to browse and extract content from
            full_text: Whether to return full text or summarized content
            
        Returns:
            Formatted web content as JSON string
        """
        try:
            logger.info(f"Browsing {len(urls)} URLs, full_text={full_text}")
            
            # Validate input
            if not urls:
                return format_error_response("URLs list cannot be empty")
            
            if len(urls) > 20:
                return format_error_response("Too many URLs. Maximum 20 URLs allowed per request")
            
            # Validate URLs
            for url in urls:
                if not url or not url.strip():
                    return format_error_response("URL cannot be empty")
                
                url = url.strip()
                if not (url.startswith('http://') or url.startswith('https://')):
                    return format_error_response(f"Invalid URL format: {url}")
            
            # Browse URLs
            web_content = await self.web_service.browse_internet(urls, full_text)
            
            # Format and return results
            return format_web_content_response(web_content)
            
        except Exception as e:
            logger.error(f"Error browsing internet: {e}")
            return format_error_response(f"Failed to browse URLs: {str(e)}")
    
    async def shorten_url(self, url: str, custom_code: Optional[str] = None) -> str:
        """
        Create a shortened URL using the URL shortener service.
        
        Args:
            url: The URL to shorten
            custom_code: Optional custom short code
            
        Returns:
            Formatted shortened URL result as JSON string
        """
        try:
            logger.info(f"Shortening URL: {url}")
            
            # Validate input
            if not url or not url.strip():
                return format_error_response("URL cannot be empty")
            
            url = url.strip()
            if not (url.startswith('http://') or url.startswith('https://')):
                return format_error_response("URL must start with http:// or https://")
            
            # Validate custom code if provided
            if custom_code:
                custom_code = custom_code.strip()
                if not custom_code.replace('_', '').replace('-', '').isalnum():
                    return format_error_response("Custom code can only contain letters, numbers, hyphens, and underscores")
            
            # Shorten URL
            result = await self.web_service.shorten_url(url, custom_code)
            
            # Format and return result
            return format_success_response(result)
            
        except Exception as e:
            logger.error(f"Error shortening URL: {e}")
            return format_error_response(f"Failed to shorten URL: {str(e)}")