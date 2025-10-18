from supabase import create_client, Client
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """
    Singleton Supabase client for handling authentication and storage
    """
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        if cls._instance is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                raise ValueError("Supabase URL and Key must be configured in settings")
            cls._instance = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return cls._instance
    
    @classmethod
    def get_service_client(cls) -> Client:
        """Get Supabase client with service role key for admin operations"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError("Supabase URL and Service Key must be configured")
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


def sign_up_user(email: str, password: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Sign up a new user with Supabase Auth
    
    Args:
        email: User's email address
        password: User's password
        metadata: Additional user metadata
        
    Returns:
        Dict containing user data and session info
    """
    try:
        client = SupabaseClient.get_client()
        
        sign_up_data = {
            "email": email,
            "password": password,
        }
        
        if metadata:
            sign_up_data["options"] = {"data": metadata}
        
        response = client.auth.sign_up(sign_up_data)
        
        if response.user:
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
            }
        else:
            return {
                "success": False,
                "error": "Failed to create user"
            }
            
    except Exception as e:
        logger.error(f"Supabase sign up error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def sign_in_user(email: str, password: str) -> Dict[str, Any]:
    """
    Sign in user with Supabase Auth
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        Dict containing user data and session info
    """
    try:
        client = SupabaseClient.get_client()
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
            }
        else:
            return {
                "success": False,
                "error": "Invalid credentials"
            }
            
    except Exception as e:
        logger.error(f"Supabase sign in error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def sign_out_user(access_token: str) -> bool:
    """
    Sign out user from Supabase
    
    Args:
        access_token: User's access token
        
    Returns:
        Boolean indicating success
    """
    try:
        client = SupabaseClient.get_client()
        client.auth.sign_out()
        return True
    except Exception as e:
        logger.error(f"Supabase sign out error: {str(e)}")
        return False


def get_user_from_token(access_token: str) -> Optional[Dict[str, Any]]:
    """
    Get user data from access token
    
    Args:
        access_token: User's access token
        
    Returns:
        User data dict or None
    """
    try:
        client = SupabaseClient.get_client()
        response = client.auth.get_user(access_token)
        return response.user if response else None
    except Exception as e:
        logger.error(f"Error getting user from token: {str(e)}")
        return None


def upload_file_to_storage(bucket_name: str, file_path: str, file_data: bytes, 
                          content_type: str = None) -> Dict[str, Any]:
    """
    Upload file to Supabase Storage
    
    Args:
        bucket_name: Name of the storage bucket
        file_path: Path where file should be stored
        file_data: File data as bytes
        content_type: MIME type of the file
        
    Returns:
        Dict with success status and file URL or error
    """
    try:
        client = SupabaseClient.get_service_client()
        
        options = {}
        if content_type:
            options['content-type'] = content_type
        
        response = client.storage.from_(bucket_name).upload(
            file_path,
            file_data,
            options
        )
        
        # Get public URL
        public_url = client.storage.from_(bucket_name).get_public_url(file_path)
        
        return {
            "success": True,
            "url": public_url,
            "path": file_path
        }
        
    except Exception as e:
        logger.error(f"Error uploading file to storage: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_file_from_storage(bucket_name: str, file_path: str) -> Optional[bytes]:
    """
    Download file from Supabase Storage
    
    Args:
        bucket_name: Name of the storage bucket
        file_path: Path to the file
        
    Returns:
        File data as bytes or None
    """
    try:
        client = SupabaseClient.get_client()
        response = client.storage.from_(bucket_name).download(file_path)
        return response
    except Exception as e:
        logger.error(f"Error downloading file from storage: {str(e)}")
        return None


def delete_file_from_storage(bucket_name: str, file_path: str) -> bool:
    """
    Delete file from Supabase Storage
    
    Args:
        bucket_name: Name of the storage bucket
        file_path: Path to the file
        
    Returns:
        Boolean indicating success
    """
    try:
        client = SupabaseClient.get_service_client()
        client.storage.from_(bucket_name).remove([file_path])
        return True
    except Exception as e:
        logger.error(f"Error deleting file from storage: {str(e)}")
        return False
