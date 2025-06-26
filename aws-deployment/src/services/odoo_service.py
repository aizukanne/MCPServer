"""
Odoo Service Implementation
==========================

This module contains the business logic for Odoo ERP integration operations.
"""

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

import requests

# Import from config and other modules
try:
    from config import odoo_url, odoo_db, odoo_login, odoo_password, base_url
    from url_shortener import URLShortener
except ImportError:
    odoo_url = None
    odoo_db = None
    odoo_login = None
    odoo_password = None
    base_url = None
    URLShortener = None
    logging.warning("Odoo configuration or URL shortener not available")

logger = logging.getLogger(__name__)


class OdooService:
    """Service for Odoo ERP integration operations."""
    
    def __init__(self):
        """Initialize the Odoo service."""
        if not all([odoo_url, odoo_db, odoo_login, odoo_password, base_url]):
            logger.warning("Odoo configuration incomplete")
    
    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with Odoo and return session info.
        
        Returns:
            Dictionary with session information or error
        """
        if not all([odoo_url, odoo_db, odoo_login, odoo_password]):
            return {'error': 'Odoo configuration incomplete'}
        
        auth_url = f"{odoo_url}/web/session/authenticate"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': odoo_db,
                'login': odoo_login,
                'password': odoo_password
            },
            'id': 1
        }
        
        try:
            response = requests.post(auth_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if 'error' in result:
                return {'error': result['error']}
            
            session_id = response.cookies.get('session_id')
            if not session_id:
                return {'error': 'No session ID received'}
                
            return {
                'session_id': session_id,
                'uid': result.get('result', {}).get('uid'),
                'username': result.get('result', {}).get('username')
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def get_mapped_models(
        self, 
        include_fields: bool = True, 
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch available mapped models.
        
        Args:
            include_fields: Whether to include field mappings
            model_name: Optional filter for model names
            
        Returns:
            Response containing mapped models
        """
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        endpoint = f"{base_url}/api/mapped_models"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        params = {}
        payload = {}
        
        if include_fields:
            params['include_fields'] = include_fields
        if model_name:
            params['model_name'] = model_name
        payload['params'] = params
        
        try:
            logger.debug(f"Request payload: {json.dumps(payload)}")
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def fetch_records(
        self, 
        external_model: str, 
        filters: Optional[List[List[Any]]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve records from an external model.
        
        Args:
            external_model: External model name
            filters: Optional Odoo domain filters
            
        Returns:
            Response containing records
        """
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        endpoint = f"{base_url}/api/{external_model}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        payload = {}
        
        if filters:
            payload['filters'] = filters
            
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def create_record(self, external_model: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record.
        
        Args:
            external_model: External model name
            record_data: Data for the record to be created
            
        Returns:
            Response containing the created record or error
        """
        # Check for missing parameters
        if not external_model:
            return {'error': "Missing required parameter: 'external_model'."}
        if not record_data:
            return {'error': "Missing required parameter: 'record_data'."}
        if not isinstance(record_data, dict):
            return {'error': "'record_data' must be a dictionary."}
        
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        endpoint = f"{base_url}/api/{external_model}/create"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        payload = {'params': record_data}
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def update_record(
        self, 
        external_model: str, 
        record_id: int, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing record.
        
        Args:
            external_model: External model name
            record_id: ID of the record to update
            **kwargs: Variable keyword arguments that will be combined into record_data
            
        Returns:
            Response containing the updated record
        """
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        endpoint = f"{base_url}/api/{external_model}/update/{record_id}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        
        # Using kwargs directly as the record_data
        record_data = kwargs
        
        try:
            response = requests.put(endpoint, headers=headers, json=record_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def delete_record(self, external_model: str, record_id: int) -> Dict[str, Any]:
        """
        Delete a record.
        
        Args:
            external_model: External model name
            record_id: ID of the record to delete
            
        Returns:
            Response indicating success or failure
        """
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        endpoint = f"{base_url}/api/{external_model}/delete/{record_id}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        
        try:
            response = requests.delete(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def print_record(self, model_name: str, record_id: int) -> Dict[str, Any]:
        """
        Print the specified record (subject to the record being printable).
        
        Args:
            model_name: The technical name of the model
            record_id: The ID of the document to print
            
        Returns:
            Dictionary containing the result of the print request or an error message
        """
        auth_response = self.authenticate()
        if 'session_id' not in auth_response:
            return auth_response
        
        session_id = auth_response['session_id']
        endpoint = f"{odoo_url}/api/generate_pdf"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        payload = {
            "params": {
                "external_model": model_name,
                "record_id": record_id
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as resp:
                response_data = resp.read().decode()
                logger.debug(f"Response content: {response_data}")
                response_data = json.loads(response_data)
                full_url = response_data["result"]["download_url"]
                logger.info(f'Full URL: {full_url}')
                
                # Shorten the URL if URLShortener is available
                if URLShortener:
                    result = URLShortener().shorten_url(full_url)
                    logger.info(f'Shortened URL: {result}')
                    result.pop('originalUrl', None)
                    return result
                else:
                    return {
                        "success": True,
                        "download_url": full_url,
                        "message": "PDF generated successfully"
                    }
                    
        except urllib.error.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except json.JSONDecodeError as json_err:
            return {'error': f'JSON decode error occurred: {json_err} - Response content: {response_data}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}
    
    async def post_record(self, external_model: str, record_id: int) -> Dict[str, Any]:
        """
        Post a record using the specified external model and record ID.
        
        Args:
            external_model: External model name
            record_id: ID of the record to post
            
        Returns:
            Response containing the result of the post operation or error
        """
        # Authenticate first
        auth_result = self.authenticate()
        if 'error' in auth_result:
            return auth_result
        
        session_id = auth_result['session_id']
        # Properly encode the external_model for URL
        encoded_model = urllib.parse.quote(external_model, safe='')
        endpoint = f"{base_url}/api/{encoded_model}/post/{record_id}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'session_id={session_id}'
        }
        
        try:
            # Include an empty JSON payload for the PUT request
            response = requests.put(endpoint, headers=headers, json={})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'error': f'Other error occurred: {err}'}