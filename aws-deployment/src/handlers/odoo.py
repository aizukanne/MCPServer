"""
Odoo ERP Integration Handler
===========================

This module contains MCP tool handlers for Odoo ERP integration functions.
"""

import logging
from typing import Any, Dict, List, Optional

from services.odoo_service import OdooService
from utils.formatting import format_odoo_response, format_error_response

logger = logging.getLogger(__name__)


class OdooHandler:
    """Handler for Odoo ERP integration MCP tools."""
    
    def __init__(self):
        """Initialize the Odoo handler."""
        self.odoo_service = OdooService()
    
    async def get_mapped_models(
        self, 
        include_fields: bool = True, 
        model_name: Optional[str] = None
    ) -> str:
        """
        Get available mapped models from Odoo.
        
        Args:
            include_fields: Whether to include field mappings
            model_name: Optional filter for specific model name
            
        Returns:
            Formatted mapped models data as JSON string
        """
        try:
            logger.info(f"Getting Odoo mapped models, include_fields={include_fields}, model_name={model_name}")
            
            # Get mapped models
            result = await self.odoo_service.get_mapped_models(include_fields, model_name)
            
            # Format and return result
            return format_odoo_response(result, "get_mapped_models")
            
        except Exception as e:
            logger.error(f"Error getting Odoo mapped models: {e}")
            return format_error_response(f"Failed to get mapped models: {str(e)}")
    
    async def fetch_records(
        self, 
        external_model: str, 
        filters: Optional[List[List[Any]]] = None
    ) -> str:
        """
        Retrieve records from an Odoo model.
        
        Args:
            external_model: External model name in Odoo
            filters: Optional Odoo domain filters
            
        Returns:
            Formatted records data as JSON string
        """
        try:
            logger.info(f"Fetching Odoo records from model: {external_model}")
            
            # Validate input
            if not external_model or not external_model.strip():
                return format_error_response("External model name cannot be empty")
            
            external_model = external_model.strip()
            
            # Fetch records
            result = await self.odoo_service.fetch_records(external_model, filters)
            
            # Format and return result
            return format_odoo_response(result, "fetch_records")
            
        except Exception as e:
            logger.error(f"Error fetching Odoo records: {e}")
            return format_error_response(f"Failed to fetch records: {str(e)}")
    
    async def create_record(self, external_model: str, record_data: Dict[str, Any]) -> str:
        """
        Create a new record in Odoo.
        
        Args:
            external_model: External model name in Odoo
            record_data: Data for the new record
            
        Returns:
            Formatted creation result as JSON string
        """
        try:
            logger.info(f"Creating Odoo record in model: {external_model}")
            
            # Validate input
            if not external_model or not external_model.strip():
                return format_error_response("External model name cannot be empty")
            
            if not record_data or not isinstance(record_data, dict):
                return format_error_response("Record data must be a non-empty dictionary")
            
            external_model = external_model.strip()
            
            # Create record
            result = await self.odoo_service.create_record(external_model, record_data)
            
            # Format and return result
            return format_odoo_response(result, "create_record")
            
        except Exception as e:
            logger.error(f"Error creating Odoo record: {e}")
            return format_error_response(f"Failed to create record: {str(e)}")
    
    async def update_record(
        self, 
        external_model: str, 
        record_id: int, 
        **kwargs
    ) -> str:
        """
        Update an existing record in Odoo.
        
        Args:
            external_model: External model name in Odoo
            record_id: ID of the record to update
            **kwargs: Fields to update
            
        Returns:
            Formatted update result as JSON string
        """
        try:
            logger.info(f"Updating Odoo record {record_id} in model: {external_model}")
            
            # Validate input
            if not external_model or not external_model.strip():
                return format_error_response("External model name cannot be empty")
            
            if not isinstance(record_id, int) or record_id <= 0:
                return format_error_response("Record ID must be a positive integer")
            
            if not kwargs:
                return format_error_response("No fields provided for update")
            
            external_model = external_model.strip()
            
            # Update record
            result = await self.odoo_service.update_record(external_model, record_id, **kwargs)
            
            # Format and return result
            return format_odoo_response(result, "update_record")
            
        except Exception as e:
            logger.error(f"Error updating Odoo record: {e}")
            return format_error_response(f"Failed to update record: {str(e)}")
    
    async def delete_record(self, external_model: str, record_id: int) -> str:
        """
        Delete a record from Odoo.
        
        Args:
            external_model: External model name in Odoo
            record_id: ID of the record to delete
            
        Returns:
            Formatted deletion result as JSON string
        """
        try:
            logger.info(f"Deleting Odoo record {record_id} from model: {external_model}")
            
            # Validate input
            if not external_model or not external_model.strip():
                return format_error_response("External model name cannot be empty")
            
            if not isinstance(record_id, int) or record_id <= 0:
                return format_error_response("Record ID must be a positive integer")
            
            external_model = external_model.strip()
            
            # Delete record
            result = await self.odoo_service.delete_record(external_model, record_id)
            
            # Format and return result
            return format_odoo_response(result, "delete_record")
            
        except Exception as e:
            logger.error(f"Error deleting Odoo record: {e}")
            return format_error_response(f"Failed to delete record: {str(e)}")
    
    async def print_record(self, model_name: str, record_id: int) -> str:
        """
        Generate a PDF report for an Odoo record.
        
        Args:
            model_name: Technical name of the Odoo model
            record_id: ID of the record to print
            
        Returns:
            Formatted print result with download URL as JSON string
        """
        try:
            logger.info(f"Printing Odoo record {record_id} from model: {model_name}")
            
            # Validate input
            if not model_name or not model_name.strip():
                return format_error_response("Model name cannot be empty")
            
            if not isinstance(record_id, int) or record_id <= 0:
                return format_error_response("Record ID must be a positive integer")
            
            model_name = model_name.strip()
            
            # Print record
            result = await self.odoo_service.print_record(model_name, record_id)
            
            # Format and return result
            return format_odoo_response(result, "print_record")
            
        except Exception as e:
            logger.error(f"Error printing Odoo record: {e}")
            return format_error_response(f"Failed to print record: {str(e)}")
    
    async def post_record(self, external_model: str, record_id: int) -> str:
        """
        Post a record in Odoo (change status to posted).
        
        Args:
            external_model: External model name in Odoo
            record_id: ID of the record to post
            
        Returns:
            Formatted post result as JSON string
        """
        try:
            logger.info(f"Posting Odoo record {record_id} in model: {external_model}")
            
            # Validate input
            if not external_model or not external_model.strip():
                return format_error_response("External model name cannot be empty")
            
            if not isinstance(record_id, int) or record_id <= 0:
                return format_error_response("Record ID must be a positive integer")
            
            external_model = external_model.strip()
            
            # Post record
            result = await self.odoo_service.post_record(external_model, record_id)
            
            # Format and return result
            return format_odoo_response(result, "post_record")
            
        except Exception as e:
            logger.error(f"Error posting Odoo record: {e}")
            return format_error_response(f"Failed to post record: {str(e)}")