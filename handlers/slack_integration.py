"""
Slack Integration Handler
========================

This module contains MCP tool handlers for Slack integration functions.
"""

import logging
from typing import Optional

from services.slack_service import SlackService
from utils.formatting import format_file_operation_response, format_database_response, format_error_response
from utils.validation import validate_file_path

logger = logging.getLogger(__name__)


class SlackHandler:
    """Handler for Slack integration MCP tools."""
    
    def __init__(self):
        """Initialize the Slack handler."""
        self.slack_service = SlackService()
    
    async def send_file_to_slack(
        self, 
        file_path: str, 
        chat_id: str, 
        title: str, 
        ts: Optional[str] = None
    ) -> str:
        """
        Upload a file to a Slack channel.
        
        Args:
            file_path: Path to the file or URL to upload
            chat_id: Slack channel ID
            title: Title for the file
            ts: Optional thread timestamp for threaded upload
            
        Returns:
            Formatted upload result as JSON string
        """
        try:
            logger.info(f"Uploading file to Slack: {file_path} -> {chat_id}")
            
            # Validate input
            if not file_path or not file_path.strip():
                return format_error_response("File path cannot be empty")
            
            if not chat_id or not chat_id.strip():
                return format_error_response("Chat ID cannot be empty")
            
            if not title or not title.strip():
                return format_error_response("Title cannot be empty")
            
            file_path = file_path.strip()
            chat_id = chat_id.strip()
            title = title.strip()
            
            # Basic validation for file path/URL
            if not (file_path.startswith(('http://', 'https://')) or file_path.startswith('/')):
                return format_error_response("File path must be a valid URL or absolute file path")
            
            # If it's a file path (not URL), validate it
            if not file_path.startswith(('http://', 'https://')):
                validation_result = validate_file_path(file_path)
                if not validation_result["valid"]:
                    return format_error_response(f"Invalid file path: {', '.join(validation_result['errors'])}")
            
            # Upload file
            result = await self.slack_service.send_file_to_slack(file_path, chat_id, title, ts)
            
            # Format and return result
            return format_file_operation_response(result, "slack_file_upload")
            
        except Exception as e:
            logger.error(f"Error uploading file to Slack: {e}")
            return format_error_response(f"Failed to upload file to Slack: {str(e)}")
    
    async def update_slack_users(self) -> str:
        """
        Sync user data from Slack workspace.
        
        Returns:
            Formatted sync result as JSON string
        """
        try:
            logger.info("Updating Slack users")
            
            # Update users from Slack
            result = await self.slack_service.update_slack_users()
            
            # Format and return result
            return format_database_response(result, "update_slack_users")
            
        except Exception as e:
            logger.error(f"Error updating Slack users: {e}")
            return format_error_response(f"Failed to update Slack users: {str(e)}")
    
    async def update_slack_conversations(self) -> str:
        """
        Sync channel/conversation data from Slack workspace.
        
        Returns:
            Formatted sync result as JSON string
        """
        try:
            logger.info("Updating Slack conversations")
            
            # Update conversations from Slack
            result = await self.slack_service.update_slack_conversations()
            
            # Format and return result
            return format_database_response(result, "update_slack_conversations")
            
        except Exception as e:
            logger.error(f"Error updating Slack conversations: {e}")
            return format_error_response(f"Failed to update Slack conversations: {str(e)}")