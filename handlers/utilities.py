"""
Utilities Handler
================

This module contains MCP tool handlers for utility functions like math and AI queries.
"""

import logging
from typing import Any, Dict

from services.utilities_service import UtilitiesService
from utils.formatting import format_math_response, format_openai_response, format_error_response

logger = logging.getLogger(__name__)


class UtilitiesHandler:
    """Handler for utility MCP tools."""
    
    def __init__(self):
        """Initialize the utilities handler."""
        self.utilities_service = UtilitiesService()
    
    async def solve_maths(self, code: str, **params) -> str:
        """
        Execute Python code for mathematical calculations.
        
        Args:
            code: Python code to execute for calculations
            **params: Additional parameters that the code might need
            
        Returns:
            Formatted calculation result as JSON string
        """
        try:
            logger.info("Executing mathematical calculation")
            
            # Validate input
            if not code or not code.strip():
                return format_error_response("Code cannot be empty")
            
            code = code.strip()
            
            # Basic security check for dangerous operations
            dangerous_keywords = [
                'import os', 'import sys', 'import subprocess', 'import shutil',
                'open(', 'file(', 'input(', 'raw_input(', 'eval(', 'exec(',
                '__import__', 'getattr(', 'setattr(', 'delattr(',
                'globals(', 'locals(', 'vars(', 'dir(',
                'exit(', 'quit(', 'reload('
            ]
            
            code_lower = code.lower()
            for keyword in dangerous_keywords:
                if keyword in code_lower:
                    return format_error_response(f"Potentially dangerous operation detected: {keyword}")
            
            # Execute code
            result = await self.utilities_service.solve_maths(code, **params)
            
            # Format and return result
            return format_math_response(result)
            
        except Exception as e:
            logger.error(f"Error executing math code: {e}")
            return format_error_response(f"Failed to execute code: {str(e)}")
    
    async def ask_openai_o1(self, prompt: str) -> str:
        """
        Query OpenAI O1 model for advanced reasoning.
        
        Args:
            prompt: Prompt to send to OpenAI O1 model
            
        Returns:
            Formatted AI response as JSON string
        """
        try:
            logger.info("Querying OpenAI O1 model")
            
            # Validate input
            if not prompt or not prompt.strip():
                return format_error_response("Prompt cannot be empty")
            
            prompt = prompt.strip()
            
            # Check prompt length (OpenAI has token limits)
            if len(prompt) > 50000:  # Rough character limit
                return format_error_response("Prompt is too long. Please reduce the length.")
            
            # Query OpenAI
            result = await self.utilities_service.ask_openai_o1(prompt)
            
            # Format and return result
            return format_openai_response(result)
            
        except Exception as e:
            logger.error(f"Error querying OpenAI: {e}")
            return format_error_response(f"Failed to query OpenAI: {str(e)}")