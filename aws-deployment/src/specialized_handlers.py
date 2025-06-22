"""
Specialized Lambda Handlers
===========================

Specialized Lambda functions for heavy operations that need more resources or time.
"""

import json
import logging
import traceback
from typing import Any, Dict

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from handlers.web_browsing import WebBrowsingHandler
from handlers.documents import DocumentHandler
from utils.validation import validate_tool_arguments
from schemas.tool_schemas import get_all_tool_schemas


def create_response(status_code: int, body: Any, headers: Dict[str, str] = None) -> Dict[str, Any]:
    """Create API Gateway response."""
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body) if not isinstance(body, str) else body
    }


def web_browsing_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Specialized Lambda handler for web browsing operations.
    
    Handles:
    - google_search
    - browse_internet 
    - shorten_url
    
    These operations can take longer and need more memory.
    """
    try:
        # Parse the event - could be direct invocation or SQS/EventBridge
        if 'Records' in event:
            # SQS/EventBridge invocation
            record = event['Records'][0]
            if 'body' in record:
                # SQS
                message_body = json.loads(record['body'])
            else:
                # EventBridge
                message_body = record
            
            tool_name = message_body['tool_name']
            arguments = message_body['arguments']
            callback_info = message_body.get('callback_info')
        else:
            # Direct invocation
            tool_name = event['tool_name']
            arguments = event['arguments']
            callback_info = event.get('callback_info')
        
        logger.info(f"Processing web browsing tool: {tool_name}")
        
        # Initialize handler
        handler = WebBrowsingHandler()
        
        # Execute the appropriate tool
        if tool_name == "google_search":
            result = handler.google_search(
                search_term=arguments["search_term"],
                before=arguments.get("before"),
                after=arguments.get("after"),
                intext=arguments.get("intext"),
                allintext=arguments.get("allintext"),
                and_condition=arguments.get("and_condition"),
                must_have=arguments.get("must_have")
            )
        elif tool_name == "browse_internet":
            result = handler.browse_internet(
                urls=arguments["urls"],
                full_text=arguments.get("full_text", False)
            )
        elif tool_name == "shorten_url":
            result = handler.shorten_url(
                url=arguments["url"],
                custom_code=arguments.get("custom_code")
            )
        else:
            raise ValueError(f"Unsupported web browsing tool: {tool_name}")
        
        # Handle callback if provided (for async operations)
        if callback_info:
            # Send result back via API Gateway or SQS
            import boto3
            
            callback_type = callback_info.get('type')
            if callback_type == 'api_gateway':
                # Store result in DynamoDB or S3 for retrieval
                pass
            elif callback_type == 'sqs':
                sqs = boto3.client('sqs')
                sqs.send_message(
                    QueueUrl=callback_info['queue_url'],
                    MessageBody=json.dumps({
                        'tool_name': tool_name,
                        'result': result,
                        'status': 'completed'
                    })
                )
        
        logger.info(f"Web browsing tool {tool_name} completed successfully")
        
        # Parse result if it's a JSON string
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = {'status': 'success', 'data': result}
        
        return create_response(200, result)
        
    except Exception as e:
        logger.error(f"Error in web browsing handler: {e}")
        logger.error(traceback.format_exc())
        
        error_response = {
            'status': 'error',
            'error': {
                'type': 'InternalError',
                'message': f'Web browsing operation failed: {str(e)}'
            }
        }
        return create_response(500, error_response)


def document_processing_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Specialized Lambda handler for document processing operations.
    
    Handles:
    - send_as_pdf
    - get_embedding
    - list_files
    
    These operations need more memory for document processing.
    """
    try:
        # Parse the event
        if 'Records' in event:
            # SQS/EventBridge invocation
            record = event['Records'][0]
            if 'body' in record:
                message_body = json.loads(record['body'])
            else:
                message_body = record
            
            tool_name = message_body['tool_name']
            arguments = message_body['arguments']
            callback_info = message_body.get('callback_info')
        else:
            # Direct invocation
            tool_name = event['tool_name']
            arguments = event['arguments']
            callback_info = event.get('callback_info')
        
        logger.info(f"Processing document tool: {tool_name}")
        
        # Initialize handler
        handler = DocumentHandler()
        
        # Execute the appropriate tool
        if tool_name == "send_as_pdf":
            result = handler.send_as_pdf(
                text=arguments["text"],
                chat_id=arguments["chat_id"],
                title=arguments["title"],
                ts=arguments.get("ts")
            )
        elif tool_name == "get_embedding":
            result = handler.get_embedding(
                text=arguments["text"],
                model=arguments.get("model", "text-embedding-ada-002")
            )
        elif tool_name == "list_files":
            result = handler.list_files(
                folder_prefix=arguments.get("folder_prefix", "uploads")
            )
        else:
            raise ValueError(f"Unsupported document tool: {tool_name}")
        
        # Handle callback if provided
        if callback_info:
            import boto3
            
            callback_type = callback_info.get('type')
            if callback_type == 'sqs':
                sqs = boto3.client('sqs')
                sqs.send_message(
                    QueueUrl=callback_info['queue_url'],
                    MessageBody=json.dumps({
                        'tool_name': tool_name,
                        'result': result,
                        'status': 'completed'
                    })
                )
        
        logger.info(f"Document tool {tool_name} completed successfully")
        
        # Parse result if it's a JSON string
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = {'status': 'success', 'data': result}
        
        return create_response(200, result)
        
    except Exception as e:
        logger.error(f"Error in document processing handler: {e}")
        logger.error(traceback.format_exc())
        
        error_response = {
            'status': 'error',
            'error': {
                'type': 'InternalError',
                'message': f'Document processing operation failed: {str(e)}'
            }
        }
        return create_response(500, error_response)


def async_operation_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler for long-running async operations.
    
    This can be triggered by EventBridge for scheduled tasks or
    by SQS for queued operations.
    """
    try:
        logger.info("Processing async operation")
        
        # Determine the source of the event
        if 'source' in event and event['source'] == 'aws.events':
            # EventBridge scheduled event
            detail = event.get('detail', {})
            operation_type = detail.get('operation_type')
            
            if operation_type == 'cleanup_old_files':
                # Clean up old files from S3
                import boto3
                from datetime import datetime, timedelta
                
                s3 = boto3.client('s3')
                bucket_name = os.environ.get('DOCS_BUCKET')
                
                # Delete files older than 30 days
                cutoff_date = datetime.now() - timedelta(days=30)
                
                response = s3.list_objects_v2(Bucket=bucket_name)
                deleted_count = 0
                
                if 'Contents' in response:
                    for obj in response['Contents']:
                        if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                            deleted_count += 1
                
                logger.info(f"Cleaned up {deleted_count} old files")
                return create_response(200, {'deleted_files': deleted_count})
                
            elif operation_type == 'update_slack_data':
                # Scheduled Slack data update
                from handlers.slack_integration import SlackHandler
                
                handler = SlackHandler()
                users_result = handler.update_slack_users()
                channels_result = handler.update_slack_conversations()
                
                return create_response(200, {
                    'users_update': users_result,
                    'channels_update': channels_result
                })
        
        elif 'Records' in event:
            # SQS message
            for record in event['Records']:
                body = json.loads(record['body'])
                operation_type = body.get('operation_type')
                
                if operation_type == 'batch_web_scraping':
                    # Process multiple URLs in batch
                    urls = body.get('urls', [])
                    full_text = body.get('full_text', False)
                    
                    from handlers.web_browsing import WebBrowsingHandler
                    handler = WebBrowsingHandler()
                    
                    results = []
                    for batch_start in range(0, len(urls), 5):  # Process 5 URLs at a time
                        batch_urls = urls[batch_start:batch_start + 5]
                        batch_result = handler.browse_internet(batch_urls, full_text)
                        results.extend(batch_result)
                    
                    return create_response(200, {'results': results})
        
        return create_response(200, {'status': 'completed'})
        
    except Exception as e:
        logger.error(f"Error in async operation handler: {e}")
        logger.error(traceback.format_exc())
        
        error_response = {
            'status': 'error',
            'error': {
                'type': 'InternalError',
                'message': f'Async operation failed: {str(e)}'
            }
        }
        return create_response(500, error_response)