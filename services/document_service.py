"""
Document Service Implementation
==============================

This module contains the business logic for document management operations.
"""

import os
import logging
import datetime
from typing import Any, Dict, Optional

import boto3
import markdown2

# Import from config and other modules
try:
    from config import docs_bucket_name, client  # OpenAI client
    from fpdf import FPDF
except ImportError:
    docs_bucket_name = None
    client = None
    FPDF = None
    logging.warning("Document service dependencies not available")

from utils.text_processing import replace_problematic_chars

logger = logging.getLogger(__name__)


class MyFPDF(FPDF):
    """Custom PDF class with header and footer."""
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, self.title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


class DocumentService:
    """Service for document management operations."""
    
    def __init__(self):
        """Initialize the document service."""
        if not docs_bucket_name:
            logger.warning("S3 bucket for documents not configured")
        if not client:
            logger.warning("OpenAI client not configured")
    
    async def send_as_pdf(
        self, 
        text: str, 
        chat_id: str, 
        title: str, 
        ts: Optional[str] = None
    ) -> str:
        """
        Convert formatted text to PDF and upload it to a Slack channel.
        
        Args:
            text: Text content to convert
            chat_id: Slack channel ID
            title: PDF title
            ts: Optional thread timestamp
            
        Returns:
            Clear status string after execution
        """
        if not FPDF or not docs_bucket_name:
            raise ValueError("PDF generation or S3 bucket not configured")
        
        pdf_path = f"/tmp/{title}.pdf"
        
        try:
            # Use a Unicode-supporting font
            pdf = MyFPDF(title)
            pdf.add_page()
            
            # Try to register and use a Unicode font
            try:
                pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
                pdf.set_font('DejaVu', '', 11)
            except:
                # Fallback to Arial if DejaVu is not available
                pdf.set_font('Arial', '', 11)

            # Convert Markdown to HTML
            text = text.replace("\n\n", "\n")
            html_content = markdown2.markdown(text)
            html_content = replace_problematic_chars(html_content)
            pdf.write_html(html_content)

            pdf.output(pdf_path, 'F')

            # Upload to S3
            bucket_name = docs_bucket_name
            folder_name = 'uploads'
            file_key = f"{folder_name}/{title}.pdf"
            s3_client = boto3.client('s3')
            s3_client.upload_file(pdf_path, bucket_name, file_key)

            # Upload to Slack
            from services.slack_service import SlackService
            slack_service = SlackService()
            slack_result = await slack_service.send_file_to_slack(pdf_path, chat_id, title, ts)
            
            if slack_result.get("ok"):
                status = "Success: PDF sent to Slack and uploaded to S3."
            else:
                status = f"Partial success: PDF uploaded to S3, but Slack upload failed: {slack_result.get('error', 'Unknown error')}"

        except Exception as e:
            status = f"Failure: {e}"

        finally:
            # Clean up
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        return status
    
    async def list_files(self, folder_prefix: str = 'uploads') -> Dict[str, str]:
        """
        List the files in a specified folder in the S3 bucket.

        Args:
            folder_prefix: The prefix of the folder whose files you want to list

        Returns:
            A dictionary where each key is the file name and the value is the object URL
        """
        if not docs_bucket_name:
            raise ValueError("S3 bucket for documents not configured")
        
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=docs_bucket_name, Prefix=folder_prefix)

        files = {}
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):  # Exclude any subfolders
                    file_url = f"https://{docs_bucket_name}.s3.amazonaws.com/{obj['Key']}"
                    file_name = obj['Key'].split('/')[-1]  # Extract the file name from the key
                    files[file_name] = file_url

        return files
    
    async def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> Dict[str, Any]:
        """
        Generate text embedding using OpenAI.
        
        Args:
            text: Text to generate embedding for
            model: OpenAI embedding model to use
            
        Returns:
            Dictionary containing the embedding result
        """
        if not client:
            raise ValueError("OpenAI client not configured")
        
        try:
            # Clean the text
            text_cleaned = text.replace("\n", " ")
            
            # Generate embedding
            response = client.embeddings.create(
                input=[text_cleaned], 
                model=model
            )
            
            embedding = response.data[0].embedding
            
            return {
                "text": text_cleaned,
                "embedding": embedding,
                "model": model,
                "embedding_length": len(embedding)
            }
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise