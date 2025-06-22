"""
Documents Handler
================

This module contains MCP tool handlers for document management functions.
"""

import logging
from typing import Optional

from services.document_service import DocumentService
from utils.formatting import format_file_operation_response, format_success_response, format_error_response

logger = logging.getLogger(__name__)


class DocumentHandler:
    """Handler for document management MCP tools."""
    
    def __init__(self):
        """Initialize the document handler."""
        self.document_service = DocumentService()
    
    async def send_as_pdf(
        self, 
        text: str, 
        chat_id: str, 
        title: str, 
        ts: Optional[str] = None
    ) -> str:
        """
        Convert text to PDF and upload to Slack.
        
        Args:
            text: Text content to convert to PDF
            chat_id: Slack channel ID to upload to
            title: Title for the PDF document
            ts: Optional thread timestamp for threaded upload
            
        Returns:
            Formatted operation result as JSON string
        """
        try:
            logger.info(f"Converting text to PDF and uploading to Slack: {title}")
            
            # Validate input
            if not text or not text.strip():
                return format_error_response("Text content cannot be empty")
            
            if not chat_id or not chat_id.strip():
                return format_error_response("Chat ID cannot be empty")
            
            if not title or not title.strip():
                return format_error_response("Title cannot be empty")
            
            text = text.strip()
            chat_id = chat_id.strip()
            title = title.strip()
            
            # Check text length (reasonable limit for PDF generation)
            if len(text) > 500000:  # 500KB text limit
                return format_error_response("Text content is too large for PDF conversion")
            
            # Convert to PDF and upload
            result = await self.document_service.send_as_pdf(text, chat_id, title, ts)
            
            # Format and return result
            return format_file_operation_response(result, "pdf_conversion_upload")
            
        except Exception as e:
            logger.error(f"Error converting text to PDF: {e}")
            return format_error_response(f"Failed to convert text to PDF: {str(e)}")
    
    async def list_files(self, folder_prefix: str = "uploads") -> str:
        """
        List files in S3 bucket folder.
        
        Args:
            folder_prefix: Folder prefix to list files from
            
        Returns:
            Formatted file list as JSON string
        """
        try:
            logger.info(f"Listing files in folder: {folder_prefix}")
            
            # Validate input
            if not folder_prefix:
                folder_prefix = "uploads"
            
            folder_prefix = folder_prefix.strip()
            
            # Basic validation for folder prefix
            if any(char in folder_prefix for char in ['..', '/', '\\']):
                return format_error_response("Invalid folder prefix. Cannot contain path traversal characters")
            
            # List files
            files = await self.document_service.list_files(folder_prefix)
            
            # Format and return result
            result = {
                "folder": folder_prefix,
                "files": files,
                "file_count": len(files)
            }
            
            return format_success_response(result)
            
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return format_error_response(f"Failed to list files: {str(e)}")
    
    async def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> str:
        """
        Generate text embedding using OpenAI.
        
        Args:
            text: Text to generate embedding for
            model: OpenAI embedding model to use
            
        Returns:
            Formatted embedding result as JSON string
        """
        try:
            logger.info(f"Generating embedding for text (length: {len(text)})")
            
            # Validate input
            if not text or not text.strip():
                return format_error_response("Text cannot be empty")
            
            text = text.strip()
            
            # Check text length (OpenAI has token limits)
            if len(text) > 8000:  # Conservative character limit
                return format_error_response("Text is too long for embedding generation")
            
            # Validate model
            valid_models = [
                "text-embedding-ada-002", 
                "text-embedding-3-small", 
                "text-embedding-3-large"
            ]
            if model not in valid_models:
                return format_error_response(f"Invalid model. Must be one of: {', '.join(valid_models)}")
            
            # Generate embedding
            result = await self.document_service.get_embedding(text, model)
            
            # Format and return result
            return format_success_response(result)
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return format_error_response(f"Failed to generate embedding: {str(e)}")