"""
Web Service Implementation
=========================

This module contains the business logic for web browsing and search operations.
"""

import os
import json
import asyncio
import logging
import warnings
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import aiohttp
import requests

# Import from original modules (assuming they exist)
try:
    from config import proxy_url, USER_AGENTS
    from url_shortener import URLShortener
except ImportError:
    proxy_url = None
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

# Import helper functions from original functions module
from utils.text_processing import (
    clean_website_data, has_proper_sentences, rank_sentences,
    load_stopwords, decimal_default
)

logger = logging.getLogger(__name__)


class WebService:
    """Service for web browsing and search operations."""
    
    def __init__(self):
        """Initialize the web service."""
        self.custom_search_api_key = os.getenv('CUSTOM_SEARCH_API_KEY')
        self.custom_search_id = os.getenv('CUSTOM_SEARCH_ID')
        self.stopwords = set()  # Will be loaded by load_stopwords function
        
        if not self.custom_search_api_key or not self.custom_search_id:
            logger.warning("Google Custom Search API credentials not configured")
    
    async def google_search(
        self,
        search_term: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        intext: Optional[str] = None,
        allintext: Optional[str] = None,
        and_condition: Optional[str] = None,
        must_have: Optional[str] = None
    ) -> Any:
        """
        Perform a Google search with advanced operators.
        
        Args:
            search_term: The main search query
            before: Search for content before this date (YYYY-MM-DD format)
            after: Search for content after this date (YYYY-MM-DD format)
            intext: Search for this text within the page content
            allintext: Search for all these terms within the page content
            and_condition: Additional term that must be present (AND operator)
            must_have: Exact phrase that must be present in results
            
        Returns:
            Search results with web content
        """
        if not self.custom_search_api_key or not self.custom_search_id:
            raise ValueError("Google Custom Search API credentials not configured")
        
        try:
            # Constructing the search term with advanced operators
            search_components = [search_term]

            # Implementing 'and' search operator
            if and_condition:
                search_components.append(search_term + " AND " + and_condition)

            # Implementing 'before' search operator (YYYY-MM-DD format)
            if before:
                search_components.append(f"before:{before}")

            # Implementing 'after' search operator (YYYY-MM-DD format)
            if after:
                search_components.append(f"after:{after}")

            # Implementing 'intext' search operator
            if intext:
                search_components.append(f"intext:{intext}")
            
            # Implementing 'allintext' search operator
            if allintext:
                search_components.append(f"allintext:{allintext}")
            
            # Implementing 'must_have' operator to require exact phrase match
            if must_have:
                search_components.append(f'"{must_have}"')

            # Join all components to form the final search query
            combined_search_term = ' '.join(search_components)
            url_encoded_search_term = quote_plus(combined_search_term)
            logger.info(f'Search Term: {url_encoded_search_term}')

            # Build the search URL   
            search_url = f"https://www.googleapis.com/customsearch/v1?q={url_encoded_search_term}&cx={self.custom_search_id}&key={self.custom_search_api_key}"
            
            # Make synchronous request for Google search
            response = requests.get(search_url)
            results = response.json().get('items', [])
            logger.info(f"Found {len(results)} search results")

            web_links = []
            for result in results:
                web_links.append(result['link'])
            
            # Get web content for top 5 results
            web_content = await self.get_web_pages(web_links[:5])
            logger.info(f"Processed {len(web_content)} web pages")
            
            return web_content
            
        except Exception as e:
            logger.error(f"Error in Google search: {e}")
            raise
    
    async def browse_internet(self, urls: List[str], full_text: bool = False) -> List[Dict[str, Any]]:
        """
        Browse and extract content from URLs.
        
        Args:
            urls: List of URLs to browse
            full_text: Whether to return full text or summarized content
            
        Returns:
            List of web page content
        """
        try:
            # Suppress resource warnings in async environment
            warnings.filterwarnings("ignore", category=ResourceWarning)
            
            web_pages = await self.get_web_pages(urls, full_text)
            return web_pages
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout error in browse_internet for URLs: {urls}")
            return [{
                "type": "text",
                "text": {
                    'error': 'Request timed out while fetching web pages',
                    'urls': urls
                }
            }]
        except Exception as e:
            logger.error(f"Error in browse_internet: {e}")
            return [{
                "type": "text",
                "text": {
                    'error': f'Failed to fetch web pages: {str(e)}',
                    'urls': urls
                }
            }]
    
    async def get_web_pages(self, urls: List[str], full_text: bool = False, max_concurrent_requests: int = 5) -> List[Dict[str, Any]]:
        """
        Asynchronously fetch and process multiple web pages.
        
        Args:
            urls: List of URLs to fetch
            full_text: Whether to return full text or summarized content
            max_concurrent_requests: Maximum concurrent requests
            
        Returns:
            List of processed web page content
        """
        try:
            # Configure connector with explicit settings to prevent resource warnings
            connector = aiohttp.TCPConnector(
                limit=max_concurrent_requests,
                limit_per_host=2,
                force_close=True,
                enable_cleanup_closed=True
            )
            
            async with aiohttp.ClientSession(connector=connector) as session:
                semaphore = asyncio.Semaphore(max_concurrent_requests)
                tasks = [self._process_page(session, url, semaphore, full_text) for url in urls]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results and handle any exceptions
                flattened_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(f"Error processing URL {urls[i]}: {result}")
                        flattened_results.append({
                            "type": "text",
                            "text": {
                                'url': urls[i],
                                'error': f'Failed to process page: {str(result)}'
                            }
                        })
                    else:
                        flattened_results.extend(result)
                
                return flattened_results
                
        except Exception as e:
            logger.error(f"Error in get_web_pages: {e}")
            return [{
                "type": "text",
                "text": {
                    'url': url,
                    'error': f'Failed to fetch pages: {str(e)}'
                }
            } for url in urls]
    
    async def _process_page(self, session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore, full_text: bool = False) -> List[Dict[str, Any]]:
        """Process a single web page."""
        async with semaphore:
            try:
                result = await self._fetch_page(session, url)
            except Exception as e:
                logger.error(f"Error fetching page {url}: {e}")
                return [{
                    "type": "text",
                    "text": {
                        'url': url,
                        'error': 'Failed to fetch page'
                    }
                }]
            
            response_list = []
            
            try:
                if isinstance(result, tuple):
                    # Handle document content (PDF, Word, etc.)
                    document_content, content_type = result
                    if document_content is not None and content_type is not None:
                        # For now, just return a placeholder
                        response_list.append({
                            "type": "text",
                            "text": {
                                'url': url,
                                'summary': 'Document content detected but processing not implemented in MCP version',
                                'content_type': content_type
                            }
                        })
                    else:
                        response_list.append({
                            "type": "text",
                            "text": {
                                'url': url,
                                'error': 'Unsupported content type'
                            }
                        })
                        
                elif isinstance(result, str) and 'Timeout error' not in result and 'error' not in result.lower():
                    # Process HTML content
                    from bs4 import BeautifulSoup
                    
                    soup = BeautifulSoup(result, 'lxml')
                    elements_to_extract = ['p', 'li', 'summary', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'td', 'th', 'a']
                    text = ' '.join(element.get_text().strip() for element in soup.find_all(elements_to_extract))
                    cleaned_text = clean_website_data(text)

                    # Load stopwords if not already loaded
                    if not self.stopwords:
                        self.stopwords = load_stopwords('english')

                    if full_text:
                        if has_proper_sentences(cleaned_text):
                            summary_or_full_text = rank_sentences(cleaned_text, self.stopwords, max_sentences=150)
                        else:
                            summary_or_full_text = cleaned_text
                    else:
                        try:
                            if has_proper_sentences(cleaned_text):
                                summary_or_full_text = rank_sentences(cleaned_text, self.stopwords, max_sentences=50)
                            else:
                                summary_or_full_text = cleaned_text
                        except Exception as e:
                            logger.error(f"Failed to rank sentences for {url}: {e}")
                            summary_or_full_text = cleaned_text

                    author = soup.find('meta', {'name': 'author'})
                    author = author['content'] if author else 'Unknown'
                    
                    date_published = soup.find('meta', {'property': 'article:published_time'})
                    date_published = date_published['content'] if date_published else 'Unknown'

                    response_list.append({
                        "type": "text",
                        "text": {
                            'url': url,
                            'summary_or_full_text': summary_or_full_text,
                            'author': author,
                            'date_published': date_published,
                            'internal_links': []
                        }
                    })

                else:
                    response_list.append({
                        "type": "text",
                        "text": {
                            'url': url,
                            'error': result if isinstance(result, str) else 'Unknown error'
                        }
                    })
                    
            except Exception as e:
                logger.error(f"Error processing page {url}: {e}")
                response_list.append({
                    "type": "text",
                    "text": {
                        'url': url,
                        'error': 'An error occurred while processing the page'
                    }
                })

            return response_list
    
    async def _fetch_page(self, session: aiohttp.ClientSession, url: str, timeout: int = 30) -> Any:
        """Fetch a single web page."""
        import random
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        
        timeout_obj = aiohttp.ClientTimeout(total=timeout, connect=10, sock_read=timeout)
        
        try:
            kwargs = {'headers': headers, 'timeout': timeout_obj}
            if proxy_url:
                kwargs['proxy'] = proxy_url
                
            async with session.get(url, **kwargs) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'text' in content_type:
                    encoding = response.charset or 'utf-8'
                    content = await response.text(encoding=encoding)
                    response.release()
                    return content
                elif any(ct in content_type for ct in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats']):
                    content = await response.read()
                    response.release()
                    return content, content_type
                else:
                    response.release()
                    return None, content_type
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout error: {url} took too long to respond.")
            return f"Timeout error: {url} took too long to respond."
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return f"Error: {str(e)}"
    
    async def shorten_url(self, url: str, custom_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Shorten a URL using the URL shortener service.
        
        Args:
            url: The URL to shorten
            custom_code: Optional custom short code
            
        Returns:
            Shortened URL result
        """
        try:
            # Use the URLShortener from the original module
            shortener = URLShortener()
            result = shortener.shorten_url(url, custom_code=custom_code)
            
            # Remove sensitive information
            if 'originalUrl' in result:
                result.pop('originalUrl', None)
            
            return result
            
        except Exception as e:
            logger.error(f"Error shortening URL: {e}")
            raise