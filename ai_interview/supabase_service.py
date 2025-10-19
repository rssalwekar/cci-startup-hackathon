"""
Supabase service for handling file uploads and storage
"""
import os
import logging
from typing import Optional, Tuple
from supabase import create_client, Client
from datetime import datetime
import mimetypes

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for interacting with Supabase storage"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.bucket_name = os.getenv('SUPABASE_BUCKET', 'interview-recordings')
        self.client: Optional[Client] = None
        
        if self.supabase_url and self.supabase_key:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not found in environment variables")
    
    def is_available(self) -> bool:
        """Check if Supabase service is available"""
        return self.client is not None
    
    def upload_file(self, file_data: bytes, file_path: str, content_type: str = None) -> Tuple[bool, Optional[str]]:
        """
        Upload a file to Supabase storage
        
        Args:
            file_data: The file content as bytes
            file_path: The path where to store the file in the bucket
            content_type: MIME type of the file
            
        Returns:
            Tuple of (success: bool, public_url: Optional[str])
        """
        if not self.is_available():
            logger.error("Supabase client not available")
            return False, None
        
        try:
            # Upload file to storage
            response = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_data,
                file_options={"content-type": content_type} if content_type else {}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            
            logger.info(f"File uploaded successfully: {file_path}")
            return True, public_url
            
        except Exception as e:
            logger.error(f"Failed to upload file to Supabase: {e}")
            return False, None
    
    def upload_recording(self, file_data: bytes, user_id: int, session_id: int, 
                        recording_type: str = 'audio') -> Tuple[bool, Optional[str]]:
        """
        Upload an interview recording
        
        Args:
            file_data: The recording file content
            user_id: User ID
            session_id: Interview session ID
            recording_type: Type of recording ('audio', 'video', 'screen')
            
        Returns:
            Tuple of (success: bool, public_url: Optional[str])
        """
        # Generate file path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extension = self._get_extension(recording_type)
        file_path = f"users/{user_id}/sessions/{session_id}/{recording_type}_{timestamp}.{extension}"
        
        # Determine content type
        content_type = self._get_content_type(recording_type)
        
        return self.upload_file(file_data, file_path, content_type)
    
    def upload_avatar(self, file_data: bytes, user_id: int, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Upload user avatar image
        
        Args:
            file_data: The image file content
            user_id: User ID
            filename: Original filename
            
        Returns:
            Tuple of (success: bool, public_url: Optional[str])
        """
        # Generate file path
        extension = filename.split('.')[-1] if '.' in filename else 'jpg'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = f"users/{user_id}/avatar/{timestamp}.{extension}"
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(filename)
        
        return self.upload_file(file_data, file_path, content_type)
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from Supabase storage
        
        Args:
            file_path: Path to the file in the bucket
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            self.client.storage.from_(self.bucket_name).remove([file_path])
            logger.info(f"File deleted successfully: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file from Supabase: {e}")
            return False
    
    def get_file_url(self, file_path: str) -> Optional[str]:
        """
        Get public URL for a file
        
        Args:
            file_path: Path to the file in the bucket
            
        Returns:
            Public URL or None
        """
        if not self.is_available():
            return None
        
        try:
            return self.client.storage.from_(self.bucket_name).get_public_url(file_path)
        except Exception as e:
            logger.error(f"Failed to get file URL: {e}")
            return None
    
    def _get_extension(self, recording_type: str) -> str:
        """Get file extension based on recording type"""
        extensions = {
            'audio': 'webm',  # Browser MediaRecorder typically uses WebM
            'video': 'webm',
            'screen': 'webm'
        }
        return extensions.get(recording_type, 'webm')
    
    def _get_content_type(self, recording_type: str) -> str:
        """Get MIME type based on recording type"""
        content_types = {
            'audio': 'audio/webm',
            'video': 'video/webm',
            'screen': 'video/webm'
        }
        return content_types.get(recording_type, 'application/octet-stream')
    
    def create_bucket_if_not_exists(self) -> bool:
        """Create the storage bucket if it doesn't exist"""
        if not self.is_available():
            return False
        
        try:
            # Try to get bucket info
            self.client.storage.get_bucket(self.bucket_name)
            logger.info(f"Bucket {self.bucket_name} already exists")
            return True
        except:
            try:
                # Create bucket if it doesn't exist
                self.client.storage.create_bucket(
                    self.bucket_name,
                    options={"public": True}
                )
                logger.info(f"Bucket {self.bucket_name} created successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to create bucket: {e}")
                return False


# Global instance
supabase_service = SupabaseService()
