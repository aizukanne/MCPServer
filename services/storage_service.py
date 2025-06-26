"""
Storage Service Implementation
=============================

This module contains the business logic for storage and message management operations.
"""

import logging
import datetime
from typing import Any, Dict, List, Optional, Union

try:
    import weaviate
    from weaviate.classes.query import Filter
    import boto3
    from boto3.dynamodb.conditions import Key, Attr
    from botocore.exceptions import ClientError
except ImportError as e:
    logging.warning(f"Some dependencies not available: {e}")

# Import from config (assuming it exists)
try:
    from config import weaviate_client, names_table, channels_table
except ImportError:
    weaviate_client = None
    names_table = None
    channels_table = None
    logging.warning("Config module not available, storage operations will not work")

logger = logging.getLogger(__name__)


def transform_objects(objects: List[Any], collection_name: str) -> List[Dict[str, Any]]:
    """Transform Weaviate objects to the expected format."""
    transformed = []
    for obj in objects:
        properties = obj.properties
        # Convert timestamp to Unix timestamp for sorting
        timestamp = properties.get('timestamp')
        if timestamp:
            # Parse ISO format timestamp and convert to Unix timestamp
            dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            sort_key = int(dt.timestamp())
        else:
            sort_key = 0
            
        transformed.append({
            "role": "user" if collection_name == "UserMessages" else "assistant",
            "message": properties.get('message', ''),
            "sort_key": sort_key,
            "chat_id": properties.get('chat_id', '')
        })
    return transformed


class StorageService:
    """Service for storage and message management operations."""
    
    def __init__(self):
        """Initialize the storage service."""
        if not get_or_create_weaviate_client:
            logger.warning("Weaviate client not configured")
        if not names_table or not channels_table:
            logger.warning("DynamoDB tables not configured")
    
    async def get_message_by_sort_id(self, role: str, chat_id: str, sort_id: int) -> Optional[str]:
        """
        Retrieve a specific message by its sort ID and role.
        
        Args:
            role: The role of the message sender (user or assistant)
            chat_id: The chat/channel ID
            sort_id: The sort ID (timestamp) of the message
            
        Returns:
            Message content or None if not found
        """
        if not weaviate_client:
            raise ValueError("Weaviate client not configured")
        
        try:
            # Determine the appropriate collection based on the role
            if role == "user":
                collection = weaviate_client.collections.get('UserMessages')
            elif role == "assistant":
                collection = weaviate_client.collections.get('AssistantMessages')
            else:
                return None

            timestamp = int(sort_id)
            timestamp_iso = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).isoformat()
            
            # Create filters to match chat_id and sort_id
            filters = (
                Filter.by_property("chat_id").equal(chat_id)
                & Filter.by_property("timestamp").equal(timestamp_iso)
            )

            # Fetch the single matching object
            response = collection.query.fetch_objects(
                filters=filters,
                limit=1
            )

            message = response.objects[0].properties.get('message') if response.objects else None
            logger.info(f"Retrieved message for sort_id {sort_id}: {bool(message)}")
            return message
            
        except Exception as e:
            logger.error(f"Error retrieving message by sort ID: {e}")
            return None
    
    async def get_messages_in_range(self, chat_id: str, start_sort_id: int, end_sort_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve messages within a specific time range.
        
        Args:
            chat_id: The chat/channel ID
            start_sort_id: Start timestamp for the range
            end_sort_id: End timestamp for the range
            
        Returns:
            List of messages in the range
        """
        weaviate_client = get_or_create_weaviate_client()
        if not weaviate_client:
            raise ValueError("Weaviate client not configured")
        
        try:
            # Retrieve user and assistant messages
            user_collection = weaviate_client.collections.get("UserMessages")
            assistant_collection = weaviate_client.collections.get("AssistantMessages")

            # Define filters for both collections using the correct timestamp conversion
            start_date = datetime.datetime.fromtimestamp(start_sort_id, datetime.timezone.utc).isoformat()
            end_date = datetime.datetime.fromtimestamp(end_sort_id, datetime.timezone.utc).isoformat()
            logger.info(f"Searching messages between {start_date} and {end_date}")

            # Define filters for both collections
            filters = (
                Filter.by_property("chat_id").equal(chat_id) 
                & Filter.by_property("timestamp").greater_or_equal(start_date) 
                & Filter.by_property("timestamp").less_or_equal(end_date)
            )

            # Fetch user messages
            user_messages_response = user_collection.query.fetch_objects(filters=filters)
            user_messages = transform_objects(
                user_messages_response.objects if user_messages_response.objects else [], 
                "UserMessages"
            )
            
            # Fetch assistant messages
            assistant_messages_response = assistant_collection.query.fetch_objects(filters=filters)
            assistant_messages = transform_objects(
                assistant_messages_response.objects if assistant_messages_response.objects else [], 
                "AssistantMessages"
            )

            # Combine and sort messages
            all_messages = user_messages + assistant_messages
            all_messages.sort(key=lambda x: x["sort_key"])

            logger.info(f"Retrieved {len(all_messages)} messages in range")
            return all_messages
            
        except Exception as e:
            logger.error(f"Error retrieving messages in range: {e}")
            return []
    
    async def get_users(self, user_id: Optional[str] = None) -> Any:
        """
        Retrieve user information from the database.
        
        Args:
            user_id: Optional specific user ID to retrieve
            
        Returns:
            User data or list of users
        """
        if not names_table:
            raise ValueError("Names table not configured")
        
        try:
            if user_id:
                # Retrieve a single user
                response = names_table.get_item(Key={'user_id': user_id})
                item = response.get('Item', None)
                if item:
                    return item
                else:
                    # Try to update from Slack and fetch again
                    from services.slack_service import SlackService
                    slack_service = SlackService()
                    await slack_service.update_slack_users()
                    
                    response = names_table.get_item(Key={'user_id': user_id})
                    item = response.get('Item', None)
                    if item:
                        return item
                    else:
                        logger.warning(f"User {user_id} not found after Slack update")
                        return None
            else:
                # Retrieve all users
                response = names_table.scan()
                items = response.get('Items', [])
                return items
                
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return None
    
    async def get_channels(self, id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve channel information from the database.
        
        Args:
            id: Optional specific channel ID to retrieve
            
        Returns:
            Channel data or list of channels
        """
        if not channels_table:
            raise ValueError("Channels table not configured")
        
        try:
            # Update from Slack first
            from services.slack_service import SlackService
            slack_service = SlackService()
            await slack_service.update_slack_conversations()
            
            if id:
                # Get specific channel
                response = channels_table.get_item(Key={'id': id})
                item = response.get('Item')
                return [item] if item else []
            else:
                # Perform a scan operation on the table to retrieve all channels  
                response = channels_table.scan()
                channels = response.get('Items', [])

                # Check if there are more channels to fetch
                while 'LastEvaluatedKey' in response:
                    response = channels_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    channels.extend(response.get('Items', []))

                return channels
                
        except Exception as e:
            logger.error(f"Error fetching channels: {e}")
            return []
    
    async def manage_mute_status(self, chat_id: str, status: Optional[Union[bool, str]] = None) -> List[Any]:
        """
        Get or set the mute status for a chat/channel.
        
        Args:
            chat_id: The chat/channel ID
            status: New mute status (true/false) or None to just retrieve current status
            
        Returns:
            List containing [status_bool, message]
        """
        if not channels_table:
            raise ValueError("Channels table not configured")
        
        table = channels_table
        
        if status is not None:
            # Initialize status_bool based on the type and value of status
            if isinstance(status, bool):
                status_bool = status
            elif isinstance(status, str):
                status = status.strip()
                if status.lower() in ['true', 'false']:
                    status_bool = status.lower() == 'true'
                else:
                    raise ValueError("String status must be 'true' or 'false' (case insensitive).")
            else:
                raise TypeError("Status must be provided as either a boolean or a string.")

            try:
                response = table.update_item(
                    Key={'id': chat_id},
                    UpdateExpression='SET maria_status = :val',
                    ExpressionAttributeValues={':val': status_bool},
                    ReturnValues='UPDATED_NEW'
                )
                current_status = "true" if status_bool else "false"
                return [status_bool, f"Current mute status: {current_status}"]
                
            except ClientError as e:
                logger.error(f"Error updating mute status: {e}")
                raise
        else:
            try:
                response = table.get_item(Key={'id': chat_id})
                item = response.get('Item', {})
                maria_status = item.get('maria_status', None)

                if maria_status is None:
                    status_bool = False  # Default if status doesn't exist
                    current_status = "false"
                    logger.info("The 'maria_status' attribute does not exist for this record.")
                else:
                    status_bool = maria_status
                    current_status = "true" if maria_status else "false"
                
                return [status_bool, f"Current mute status: {current_status}"]
                
            except ClientError as e:
                logger.error(f"Error getting mute status: {e}")
                raise