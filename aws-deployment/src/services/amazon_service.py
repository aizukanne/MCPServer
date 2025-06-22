"""
Amazon Service Implementation
============================

This module contains the business logic for Amazon product search operations.
"""

import logging
from typing import Any, Dict, Union

import requests

logger = logging.getLogger(__name__)


class AmazonService:
    """Service for Amazon product search operations."""
    
    def __init__(self):
        """Initialize the Amazon service."""
        # Using the API key from the original code
        self.api_key = "4c37223acemsh65b1a8b456b72c1p15a99ajsnd4a09ab346a4"
        self.api_host = "real-time-amazon-data.p.rapidapi.com"
    
    async def search_amazon_products(
        self,
        query: str,
        country: str = "CA",
        page: int = 1,
        sort_by: str = "RELEVANCE",
        product_condition: str = "NEW",
        is_prime: bool = False,
        deals_and_discounts: str = "NONE"
    ) -> Dict[str, Any]:
        """
        Search for products on Amazon using the Real-Time Amazon Data API from RapidAPI.
        
        Args:
            query: The search term to query Amazon with
            country: The Amazon marketplace country code
            page: The page number of results
            sort_by: How to sort the results
            product_condition: Product condition filter
            is_prime: Filter for Amazon Prime eligible products
            deals_and_discounts: Filter for deals and discounts
            
        Returns:
            The full API response as a dictionary
        """
        url = "https://real-time-amazon-data.p.rapidapi.com/search"
        
        # Convert boolean to string for the API
        is_prime_str = str(is_prime).lower()
        
        querystring = {
            "query": query,
            "country": country,
            "page": str(page),
            "sort_by": sort_by,
            "product_condition": product_condition,
            "is_prime": is_prime_str,
            "deals_and_discounts": deals_and_discounts
        }
        
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Amazon API request failed: {e}")
            return {"status": "ERROR", "message": str(e)}
    
    async def search_and_format_products(
        self,
        query: str,
        country: str = "CA",
        max_products: int = 5,
        **kwargs
    ) -> str:
        """
        Search for products on Amazon and return formatted results.
        
        Args:
            query: The search term to query Amazon with
            country: The Amazon marketplace country code
            max_products: Maximum number of products to show in results
            **kwargs: Additional parameters to pass to the search_amazon_products function
            
        Returns:
            A formatted string containing the product information
        """
        response = await self.search_amazon_products(query=query, country=country, **kwargs)
        return self.format_product_results(response, max_products)
    
    def format_product_results(self, response_data: Dict[str, Any], max_products: int = 5) -> str:
        """
        Format the API response data into a readable string format.
        
        Args:
            response_data: The API response data
            max_products: Maximum number of products to include in the formatted output
            
        Returns:
            A formatted string containing the product information
        """
        if response_data.get("status") != "OK":
            return f"Error: {response_data.get('message', 'Unknown error')}"
        
        data = response_data.get("data", {})
        total_products = data.get("total_products", 0)
        products = data.get("products", [])
        
        if not products:
            return "No products found."
        
        result = f"Found {total_products} products. Showing top {min(max_products, len(products))}:\n\n"
        
        for i, product in enumerate(products[:max_products], 1):
            title = product.get("product_title", "No title")
            price = product.get("product_price", "Price not available")
            rating = product.get("product_star_rating", "No rating")
            num_ratings = product.get("product_num_ratings", 0)
            url = product.get("product_url", "URL not available")
            
            result += f"{i}. {title}\n"
            result += f"   Price: {price}\n"
            result += f"   URL: {url}\n"
            
            if rating and num_ratings:
                result += f"   Rating: {rating}/5 ({num_ratings} reviews)\n"
            
            # Add best seller or Amazon's choice badge if applicable
            if product.get("is_best_seller"):
                result += f"   🏆 Best Seller\n"
            if product.get("is_amazon_choice"):
                result += f"   ✅ Amazon's Choice\n"
            
            # Add delivery information if available
            delivery = product.get("delivery")
            if delivery:
                result += f"   Delivery: {delivery}\n"
            
            result += "\n"
        
        return result