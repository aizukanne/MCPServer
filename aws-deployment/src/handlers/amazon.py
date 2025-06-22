"""
Amazon Integration Handler
=========================

This module contains MCP tool handlers for Amazon product search functions.
"""

import logging
from typing import Any, Dict

from services.amazon_service import AmazonService
from utils.formatting import format_amazon_products_response, format_error_response

logger = logging.getLogger(__name__)


class AmazonHandler:
    """Handler for Amazon integration MCP tools."""
    
    def __init__(self):
        """Initialize the Amazon handler."""
        self.amazon_service = AmazonService()
    
    async def search_products(
        self,
        query: str,
        country: str = "CA",
        page: int = 1,
        sort_by: str = "RELEVANCE",
        product_condition: str = "NEW",
        is_prime: bool = False,
        deals_and_discounts: str = "NONE"
    ) -> str:
        """
        Search for products on Amazon marketplace.
        
        Args:
            query: Search term for Amazon products
            country: Amazon marketplace country code
            page: Page number of results
            sort_by: How to sort the results
            product_condition: Product condition filter
            is_prime: Filter for Amazon Prime eligible products
            deals_and_discounts: Filter for deals and discounts
            
        Returns:
            Formatted search results as JSON string
        """
        try:
            logger.info(f"Searching Amazon products: {query} in {country}")
            
            # Validate input
            if not query or not query.strip():
                return format_error_response("Search query cannot be empty")
            
            query = query.strip()
            
            # Validate country code
            valid_countries = ["US", "CA", "UK", "DE", "FR", "IT", "ES", "JP", "AU"]
            if country not in valid_countries:
                return format_error_response(f"Invalid country code. Must be one of: {', '.join(valid_countries)}")
            
            # Validate page number
            if not isinstance(page, int) or page < 1:
                return format_error_response("Page number must be a positive integer")
            
            # Validate sort_by
            valid_sort_options = ["RELEVANCE", "PRICE_LOW_TO_HIGH", "PRICE_HIGH_TO_LOW", "RATING", "NEWEST"]
            if sort_by not in valid_sort_options:
                return format_error_response(f"Invalid sort option. Must be one of: {', '.join(valid_sort_options)}")
            
            # Validate product_condition
            valid_conditions = ["NEW", "USED", "REFURBISHED"]
            if product_condition not in valid_conditions:
                return format_error_response(f"Invalid product condition. Must be one of: {', '.join(valid_conditions)}")
            
            # Validate deals_and_discounts
            valid_deals = ["NONE", "TODAY_DEALS", "ON_SALE"]
            if deals_and_discounts not in valid_deals:
                return format_error_response(f"Invalid deals filter. Must be one of: {', '.join(valid_deals)}")
            
            # Search products
            result = await self.amazon_service.search_amazon_products(
                query=query,
                country=country,
                page=page,
                sort_by=sort_by,
                product_condition=product_condition,
                is_prime=is_prime,
                deals_and_discounts=deals_and_discounts
            )
            
            # Format and return result
            return format_amazon_products_response(result)
            
        except Exception as e:
            logger.error(f"Error searching Amazon products: {e}")
            return format_error_response(f"Failed to search Amazon products: {str(e)}")
    
    async def search_and_format_products(
        self,
        query: str,
        country: str = "CA",
        max_products: int = 5,
        **kwargs
    ) -> str:
        """
        Search Amazon products and return formatted results.
        
        Args:
            query: Search term for Amazon products
            country: Amazon marketplace country code
            max_products: Maximum number of products to show
            **kwargs: Additional parameters to pass to the search function
            
        Returns:
            Formatted search results as JSON string
        """
        try:
            logger.info(f"Searching and formatting Amazon products: {query}")
            
            # Validate input
            if not query or not query.strip():
                return format_error_response("Search query cannot be empty")
            
            query = query.strip()
            
            # Validate max_products
            if not isinstance(max_products, int) or max_products < 1 or max_products > 20:
                return format_error_response("Max products must be between 1 and 20")
            
            # Search and format products
            result = await self.amazon_service.search_and_format_products(
                query=query,
                country=country,
                max_products=max_products,
                **kwargs
            )
            
            # Format and return result
            return format_amazon_products_response(result)
            
        except Exception as e:
            logger.error(f"Error searching and formatting Amazon products: {e}")
            return format_error_response(f"Failed to search and format products: {str(e)}")