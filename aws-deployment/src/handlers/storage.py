"""
Storage and Messages Handler
===========================

This module contains MCP tool handlers for storage and message management functions.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from services.storage_service import StorageService
from utils.formatting import format_database_response, format_error_response

logger = logging.getLogger(__name__)


class StorageHandler:
    """Handler for storage and message management MCP tools."""
    
    def __init__(self):
        """Initialize the storage handler."""
        self.storage_service = StorageService()
    
    async def get_message_by_sort_id(self, role: str, chat_id: str, sort_id: int) -> str:
        """
        Retrieve a specific message by its sort ID and role.
        
        Args:
            role: The role of the message sender (user or assistant)
            chat_id: The chat/channel ID
            sort_id: The sort ID (timestamp) of the message
            
        Returns:
            Formatted message data as JSON string
        """
        try:
            logger.info(f"Getting message by sort ID: {sort_id} for role: {role} in chat: {chat_id}")
            
            # Validate input
            if role not in ["user", "assistant"]:
                return format_error_response("Role must be 'user' or 'assistant'")
            
            if not chat_id or not chat_id.strip():
                return format_error_response("Chat ID cannot be empty")
            
            if not isinstance(sort_id, int) or sort_id < 0:
                return format_error_response("Sort ID must be a positive integer")
            
            # Get message
            message = await self.storage_service.get_message_by_sort_id(
                role.strip(), 
                chat_id.strip(), 
                sort_id
            )
            
            if message is None:
                return format_database_response(None, "get_message")
            
            result = {
                "role": role,
                "chat_id": chat_id,
                "sort_id": sort_id,
                "message": message
            }
            
            return format_database_response(result, "get_message")
            
        except Exception as e:
            logger.error(f"Error getting message by sort ID: {e}")
            return format_error_response(f"Failed to get message: {str(e)}")
    
    async def get_messages_in_range(self, chat_id: str, start_sort_id: int, end_sort_id: int) -> str:
        """
        Retrieve messages within a specific time range.
        
        Args:
            chat_id: The chat/channel ID
            start_sort_id: Start timestamp for the range
            end_sort_id: End timestamp for the range
            
        Returns:
            Formatted messages data as JSON string
        """
        try:
            logger.info(f"Getting messages in range {start_sort_id}-{end_sort_id} for chat: {chat_id}")
            
            # Validate input
            if not chat_id or not chat_id.strip():
                return format_error_response("Chat ID cannot be empty")
            
            if not isinstance(start_sort_id, int) or start_sort_id < 0:
                return format_error_response("Start sort ID must be a positive integer")
            
            if not isinstance(end_sort_id, int) or end_sort_id < 0:
                return format_error_response("End sort ID must be a positive integer")
            
            if start_sort_id >= end_sort_id:
                return format_error_response("Start sort ID must be less than end sort ID")
            
            # Get messages
            messages = await self.storage_service.get_messages_in_range(
                chat_id.strip(),
                start_sort_id,
                end_sort_id
            )
            
            return format_database_response(messages, "get_messages_in_range")
            
        except Exception as e:
            logger.error(f"Error getting messages in range: {e}")
            return format_error_response(f"Failed to get messages: {str(e)}")
    
    async def get_users(self, user_id: Optional[str] = None) -> str:
        """
        Retrieve user information from the database.
        
        Args:
            user_id: Optional specific user ID to retrieve
            
        Returns:
            Formatted user data as JSON string
        """
        try:
            if user_id:
                logger.info(f"Getting user: {user_id}")
                user_id = user_id.strip()
            else:
                logger.info("Getting all users")
            
            # Get users
            users = await self.storage_service.get_users(user_id)
            
            return format_database_response(users, "get_users")
            
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return format_error_response(f"Failed to get users: {str(e)}")
    
    async def get_channels(self, id: Optional[str] = None) -> str:
        """
        Retrieve channel information from the database.
        
        Args:
            id: Optional specific channel ID to retrieve
            
        Returns:
            Formatted channel data as JSON string
        """
        try:
            if id:
                logger.info(f"Getting channel: {id}")
                id = id.strip()
            else:
                logger.info("Getting all channels")
            
            # Get channels
            channels = await self.storage_service.get_channels(id)
            
            return format_database_response(channels, "get_channels")
            
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return format_error_response(f"Failed to get channels: {str(e)}")
    
    async def manage_mute_status(self, chat_id: str, status: Optional[Union[bool, str]] = None) -> str:
        """
        Get or set the mute status for a chat/channel.
        
        Args:
            chat_id: The chat/channel ID
            status: New mute status (true/false) or None to just retrieve current status
            
        Returns:
            Formatted mute status data as JSON string
        """
        try:
            logger.info(f"Managing mute status for chat: {chat_id}, status: {status}")
            
            # Validate input
            if not chat_id or not chat_id.strip():
                return format_error_response("Chat ID cannot be empty")
            
            chat_id = chat_id.strip()
            
            # Validate status if provided
            if status is not None:
                if isinstance(status, str):
                    status = status.strip().lower()
                    if status not in ['true', 'false']:
                        return format_error_response("Status string must be 'true' or 'false'")
                    status = status == 'true'
                elif not isinstance(status, bool):
                    return format_error_response("Status must be boolean or string 'true'/'false'")
            
            # Manage mute status
            result = await self.storage_service.manage_mute_status(chat_id, status)
            
            # Format result
            if isinstance(result, list) and len(result) == 2:
                current_status, message = result
                response_data = {
                    "chat_id": chat_id,
                    "mute_status": current_status,
                    "message": message,
                    "action": "set" if status is not None else "get"
                }
            else:
                response_data = result
            
            return format_database_response(response_data, "manage_mute_status")
            
        except Exception as e:
            logger.error(f"Error managing mute status: {e}")
            return format_error_response(f"Failed to manage mute status: {str(e)}")