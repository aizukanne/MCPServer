"""
Utilities Service Implementation
===============================

This module contains the business logic for utility operations like math and AI queries.
"""

import json
import logging
from typing import Any, Dict, Optional

try:
    import openai
    from decimal import Decimal
except ImportError as e:
    logging.warning(f"Some dependencies not available: {e}")

# Import from config (assuming it exists)
try:
    from config import client  # OpenAI client
except ImportError:
    client = None
    logging.warning("OpenAI client not configured")

from utils.text_processing import decimal_default, is_serializable

logger = logging.getLogger(__name__)


class UtilitiesService:
    """Service for utility operations."""
    
    def __init__(self):
        """Initialize the utilities service."""
        if not client:
            logger.warning("OpenAI client not configured")
    
    async def solve_maths(self, code: str, **params) -> Dict[str, Any]:
        """
        Execute Python code for mathematical calculations.
        
        Args:
            code: The Python code to execute
            **params: Any parameters that the code might need
            
        Returns:
            Dictionary containing the result or an error message
        """
        exec_env = {}
        exec_env.update(params)
        
        try:
            # Execute the code in a controlled environment
            exec(code, {}, exec_env)
            
            # Filter out non-serializable objects
            serializable_result = {
                key: value for key, value in exec_env.items() 
                if is_serializable(value)
            }
            
            logger.info(f"Math execution successful, returned {len(serializable_result)} variables")
            return {"status": "success", "result": serializable_result}
            
        except Exception as e:
            logger.error(f"Math execution error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def ask_openai_o1(self, prompt: str) -> Optional[str]:
        """
        Query OpenAI O1 model for advanced reasoning.
        
        Args:
            prompt: Prompt to send to OpenAI O1 model
            
        Returns:
            AI response or None if failed
        """
        if not client:
            raise ValueError("OpenAI client not configured")
        
        logger.info('Sending prompt to OpenAI O1 model')
        
        message = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            # Prepare the API call
            response = client.chat.completions.create(
                model="o3-mini-2025-01-31",  # Using the model from original code
                messages=message
            )
            
            logger.info('Received response from OpenAI O1')
            
            # Extract the actual message content
            response_message_content = response.choices[0].message.content

            # Return the serialized content
            return json.dumps(response_message_content, default=decimal_default)
            
        except Exception as e:
            logger.error(f"Error during OpenAI O1 API call: {e}")
            return None