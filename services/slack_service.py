"""
Slack Service Implementation
===========================

This module contains the business logic for Slack integration operations.
"""

import os
import logging
import tempfile
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests

# Import from config (assuming it exists)
try:
    from config import slack_bot_token, names_table, channels_table
except ImportError:
    slack_bot_token = None
    names_table = None
    channels_table = None
    logging.warning("Slack configuration not available")

logger = logging.getLogger(__name__)


class SlackService:
    """Service for Slack integration operations."""
    
    def __init__(self):
        """Initialize the Slack service."""
        if not slack_bot_token:
            logger.warning("Slack bot token not configured")
        if not names_table or not channels_table:
            logger.warning("DynamoDB tables not configured for Slack operations")
    
    async def send_file_to_slack(
        self, 
        file_path: str, 
        chat_id: str, 
        title: str, 
        ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to a Slack channel using the external upload API.
        If the file_path is a URL, downloads the file first.
        
        Args:
            file_path: The path to the file or a URL
            chat_id: The ID of the Slack channel where the file will be uploaded
            title: The title of the file
            ts: The thread timestamp (optional)
            
        Returns:
            The JSON response from the files.completeUploadExternal API
        """
        if not slack_bot_token:
            raise ValueError("Slack bot token not configured")
        
        # Check if file_path is a URL
        parsed_url = urlparse(file_path)
        is_url = parsed_url.scheme in ('http', 'https')
        
        if is_url:
            # Download the file into a temporary file
            response = requests.get(file_path)
            response.raise_for_status()  # Ensure the download succeeded
            suffix = os.path.splitext(parsed_url.path)[1]  # Extract the file extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(response.content)
                file_to_upload = tmp_file.name
        else:
            file_to_upload = file_path

        try:
            # Get file details
            file_size = os.path.getsize(file_to_upload)
            file_name = os.path.basename(file_to_upload)
            
            # Step 1: Get upload URL
            headers = {
                "Authorization": f"Bearer {slack_bot_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            url_params = {
                "filename": file_name,
                "length": file_size
            }
            
            response = requests.get(
                "https://slack.com/api/files.getUploadURLExternal",
                headers=headers,
                params=url_params
            )
            
            if not response.ok or not response.json().get("ok"):
                error = response.json().get("error", "Unknown error")
                logger.error(f"Error getting upload URL: {error}")
                return response.json()
            
            upload_url = response.json()["upload_url"]
            file_id = response.json()["file_id"]
            
            # Step 2: Upload file to the provided URL
            with open(file_to_upload, "rb") as file:
                # Determine content type based on file extension
                import mimetypes
                file_extension = os.path.splitext(file_to_upload)[1].lower()
                content_type = mimetypes.guess_type(file_to_upload)[0] or "application/octet-stream"
                
                files = {
                    "file": (file_name, file, content_type)
                }
                upload_response = requests.post(upload_url, files=files)
            
            if not upload_response.ok:
                logger.error(f"Error uploading file: {upload_response.status_code}")
                return {"ok": False, "error": "upload_failed"}
            
            # Step 3: Complete the upload
            complete_data = {
                "files": [{
                    "id": file_id,
                    "title": title
                }],
                "channel_id": chat_id
            }
            
            if ts:
                complete_data["thread_ts"] = ts
            
            complete_response = requests.post(
                "https://slack.com/api/files.completeUploadExternal",
                headers={
                    "Authorization": f"Bearer {slack_bot_token}",
                    "Content-Type": "application/json"
                },
                json=complete_data
            )
            
            if complete_response.ok and complete_response.json().get("ok"):
                logger.info(f"File uploaded successfully: {file_id}")
            else:
                error = complete_response.json().get("error", "Unknown error")
                logger.error(f"Error completing upload: {error}")
            
            return complete_response.json()
            
        finally:
            if is_url:
                # Remove the temporary file
                os.unlink(file_to_upload)
    
    async def update_slack_users(self) -> Dict[str, Any]:
        """
        Sync user data from Slack workspace.
        
        Returns:
            Dictionary with update results
        """
        if not slack_bot_token or not names_table:
            raise ValueError("Slack bot token or names table not configured")
        
        url = 'https://slack.com/api/users.list'
        headers = {
            'Authorization': f'Bearer {slack_bot_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            error_msg = f"Failed to retrieve users list: HTTP {response.status_code}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "users_processed": 0
            }

        users_list = response.json().get('members', [])
        processed_count = 0
        updated_count = 0
        added_count = 0
        error_count = 0
        
        for user in users_list:
            if not user.get('deleted', True) and not user.get('is_bot', True) and not user.get('is_app_user', True):
                user_id = user.get('id')
                processed_count += 1
                
                try:
                    response = names_table.get_item(Key={'user_id': user_id})
                    item = response.get('Item', None)
                    
                    if item:
                        logger.debug(f"User {user_id} already exists in the database.")
                        # Check if all keys are available
                        missing_keys = [key for key in ['real_name', 'display_name', 'email'] if key not in item]
                        if missing_keys:
                            logger.info(f"Updating user {user_id} with missing keys: {missing_keys}")
                            for key in missing_keys:
                                item[key] = user.get('profile', {}).get(key, '')
                            names_table.put_item(Item=item)
                            logger.info(f"User {user_id} updated successfully.")
                            updated_count += 1
                    else:
                        logger.info(f"Adding user {user_id} to the database.")
                        user_data = {
                            'user_id': user_id,
                            'real_name': user.get('profile', {}).get('real_name', ''),
                            'display_name': user.get('profile', {}).get('display_name', ''),
                            'email': user.get('profile', {}).get('email', '')
                        }
                        names_table.put_item(Item=user_data)
                        logger.info(f"User {user_id} added successfully.")
                        added_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing user {user_id}: {e}")
                    error_count += 1

        return {
            "success": True,
            "users_processed": processed_count,
            "users_added": added_count,
            "users_updated": updated_count,
            "errors": error_count,
            "message": f"Processed {processed_count} users: {added_count} added, {updated_count} updated, {error_count} errors"
        }
    
    async def update_slack_conversations(self) -> Dict[str, Any]:
        """
        Sync channel/conversation data from Slack workspace.
        
        Returns:
            Dictionary with update results
        """
        if not slack_bot_token or not channels_table:
            raise ValueError("Slack bot token or channels table not configured")
        
        url = 'https://slack.com/api/conversations.list'
        headers = {
            'Authorization': f'Bearer {slack_bot_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'types': 'public_channel,private_channel'
        }

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            error_msg = f"Failed to retrieve conversations list: HTTP {response.status_code}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "channels_processed": 0
            }

        conversations_list = response.json().get('channels', [])
        processed_count = 0
        updated_count = 0
        added_count = 0
        error_count = 0
        
        for channel in conversations_list:
            channel_id = channel.get('id')
            processed_count += 1
            
            try:
                # Retrieve the existing channel details from DynamoDB
                existing_channel = channels_table.get_item(Key={'id': channel_id})
                
                if 'Item' in existing_channel:
                    logger.debug(f"Channel {channel_id} already exists in the database.")
                    # Existing channel: update if necessary
                    channels_table.update_item(
                        Key={'id': channel_id},
                        UpdateExpression="set #info.#name=:n, #info.#is_private=:p, #info.#num_members=:m",
                        ExpressionAttributeValues={
                            ':n': channel.get('name'),
                            ':p': channel.get('is_private'),
                            ':m': channel.get('num_members')
                        },
                        ExpressionAttributeNames={
                            "#info": "info",
                            "#name": "name",
                            "#is_private": "is_private",
                            "#num_members": "num_members"
                        }
                    )
                    updated_count += 1
                else:
                    # New channel: add to the database
                    channels_table.put_item(Item=channel)
                    logger.info(f"Channel {channel_id} added to the database.")
                    added_count += 1

            except Exception as e:
                logger.error(f"Error updating channel {channel_id}: {e}")
                error_count += 1

        return {
            "success": True,
            "channels_processed": processed_count,
            "channels_added": added_count,
            "channels_updated": updated_count,
            "errors": error_count,
            "message": f"Processed {processed_count} channels: {added_count} added, {updated_count} updated, {error_count} errors"
        }