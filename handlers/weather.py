"""
Weather Tools Handler
====================

This module contains MCP tool handlers for weather-related functions.
"""

import logging
from typing import Any, Dict, Optional, Tuple

from services.weather_service import WeatherService
from utils.formatting import format_weather_response, format_error_response, format_success_response

logger = logging.getLogger(__name__)


class WeatherHandler:
    """Handler for weather-related MCP tools."""
    
    def __init__(self):
        """Initialize the weather handler."""
        self.weather_service = WeatherService()
    
    async def get_weather_data(self, location_name: str = "Whitehorse") -> str:
        """
        Get current weather data for a specified location.
        
        Args:
            location_name: Name of the location to get weather for
            
        Returns:
            Formatted weather data as JSON string
        """
        try:
            logger.info(f"Getting weather data for location: {location_name}")
            
            # Validate input
            if not location_name or not location_name.strip():
                return format_error_response("Location name cannot be empty")
            
            location_name = location_name.strip()
            
            # Get weather data from service
            weather_data = await self.weather_service.get_weather_data(location_name)
            
            # Format response
            return format_weather_response(weather_data)
            
        except Exception as e:
            logger.error(f"Error getting weather data: {e}")
            return format_error_response(f"Failed to get weather data: {str(e)}")
    
    async def get_coordinates(self, location_name: str) -> str:
        """
        Get latitude and longitude coordinates for a location name.
        
        Args:
            location_name: Name of the location to get coordinates for
            
        Returns:
            Formatted coordinates as JSON string
        """
        try:
            logger.info(f"Getting coordinates for location: {location_name}")
            
            # Validate input
            if not location_name or not location_name.strip():
                return format_error_response("Location name cannot be empty")
            
            location_name = location_name.strip()
            
            # Get coordinates from service
            coordinates = await self.weather_service.get_coordinates(location_name)
            
            if coordinates is None:
                return format_error_response(f"Could not find coordinates for location: {location_name}")
            
            lat, lon = coordinates
            
            response = {
                "status": "success",
                "data": {
                    "location": location_name,
                    "latitude": lat,
                    "longitude": lon,
                    "coordinates": f"{lat}, {lon}"
                }
            }
            
            return format_success_response(response)
            
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
            return format_error_response(f"Failed to get coordinates: {str(e)}")