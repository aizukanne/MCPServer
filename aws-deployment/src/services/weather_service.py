"""
Weather Service Implementation
=============================

This module contains the business logic for weather-related operations.
"""

import os
import logging
from typing import Any, Dict, Optional, Tuple
import aiohttp
import asyncio

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather operations."""
    
    def __init__(self):
        """Initialize the weather service."""
        self.openweather_api_key = os.getenv('OPENWEATHER_KEY')
        if not self.openweather_api_key:
            logger.warning("OPENWEATHER_KEY environment variable not set")
    
    async def get_coordinates(self, location_name: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude coordinates for a location name.
        
        Args:
            location_name: Name of the location
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        if not self.openweather_api_key:
            raise ValueError("OpenWeather API key not configured")
        
        base_url = 'http://api.openweathermap.org/geo/1.0/direct'
        params = {
            'q': location_name,
            'limit': 1,
            'appid': self.openweather_api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            lat = data[0]['lat']
                            lon = data[0]['lon']
                            return lat, lon
                    else:
                        logger.error(f"Geocoding API error: {response.status}")
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
        
        return None
    
    async def get_weather_data(self, location_name: str = 'Whitehorse') -> Any:
        """
        Get current weather data for a location.
        
        Args:
            location_name: Name of the location
            
        Returns:
            Weather data or error message
        """
        try:
            # Validate location_name
            if not location_name.strip():
                return 'Location name is empty or contains only spaces. Please provide a valid location name.'
            
            # Get coordinates
            coordinates = await self.get_coordinates(location_name)
            if not coordinates:
                return 'Geolocation Failed! I could not find this location on a MAP.'
            
            lat, lon = coordinates
            
            # Get weather data
            url = 'https://api.openweathermap.org/data/3.0/onecall'
            params = {
                'appid': self.openweather_api_key,
                'lat': lat,
                'lon': lon,
                'exclude': 'hourly,minutely,daily',
                'units': 'metric'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        return f'Failed to get weather data: {response.reason}'
                    
                    weather_data = await response.json()
                    
                    # Add location information to the response
                    weather_data['location'] = {
                        'name': location_name,
                        'latitude': lat,
                        'longitude': lon
                    }
                    
                    return weather_data
        
        except Exception as e:
            logger.error(f"Error getting weather data: {e}")
            return f'Error getting weather data: {str(e)}'