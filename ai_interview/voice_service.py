import os
import io
import base64
import hashlib
from typing import Optional, Dict
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from django.conf import settings


class VoiceService:
    """Service for natural voice synthesis using ElevenLabs API with caching"""
    
    def __init__(self):
        # Initialize ElevenLabs client with API key
        api_key = os.getenv('ELEVEN_LABS_API_KEY')
        if api_key:
            self.client = ElevenLabs(api_key=api_key)
        else:
            print("Warning: ELEVEN_LABS_API_KEY not found in environment variables")
            self.client = None
        
        # Audio cache to store generated speech
        self.audio_cache: Dict[str, str] = {}  # text_hash -> base64_audio
    
    def generate_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[str]:
        """
        Generate natural speech from text using ElevenLabs API with caching
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID (default is a natural-sounding voice)
            
        Returns:
            Base64 encoded audio data or None if failed
        """
        if not self.client:
            print("ElevenLabs client not initialized - API key missing")
            return None
            
        try:
            # Clean text for better speech synthesis
            clean_text = self._clean_text_for_speech(text)
            
            # Create cache key from cleaned text and voice_id
            cache_key = self._create_cache_key(clean_text, voice_id)
            
            # Check if we have cached audio for this text
            if cache_key in self.audio_cache:
                print(f"Using cached audio for text: '{clean_text[:30]}...'")
                return self.audio_cache[cache_key]
            
            print(f"Generating new audio for text: '{clean_text[:30]}...'")
            
            # Generate speech using ElevenLabs
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=clean_text,
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.8,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Convert generator to bytes
            audio_bytes = b''.join(audio_generator)
            
            # Convert audio to base64 for web transmission
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Cache the audio for future use
            self.audio_cache[cache_key] = audio_base64
            print(f"Cached audio for future use. Cache size: {len(self.audio_cache)}")
            
            return audio_base64
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text to make it more suitable for speech synthesis and save characters
        
        Args:
            text: Raw text with markdown formatting
            
        Returns:
            Cleaned text optimized for speech
        """
        import re
        
        # Remove markdown formatting
        text = re.sub(r'```[^`]*```', '', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'#{1,6}\s*', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'^\s*[-*+]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
        
        # Replace multiple newlines with single space
        text = re.sub(r'\n+', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Additional character-saving optimizations
        # Remove common interview phrases that add no value to speech
        text = re.sub(r'\b(Here\'s|Here is)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(Let me|Let\'s)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(Please|Kindly)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(That\'s|That is)\b', 'That', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(You\'re|You are)\b', 'You', text, flags=re.IGNORECASE)
        
        # Remove redundant words
        text = re.sub(r'\b(great|good|nice|perfect|excellent)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(very|really|quite|pretty)\b', '', text, flags=re.IGNORECASE)
        
        # Clean up any double spaces created by removals
        text = re.sub(r'\s+', ' ', text)
        
        # Trim and return
        return text.strip()
    
    def _create_cache_key(self, text: str, voice_id: str) -> str:
        """
        Create a cache key from text and voice_id
        
        Args:
            text: Cleaned text
            voice_id: Voice ID used for synthesis
            
        Returns:
            MD5 hash string for cache key
        """
        # Combine text and voice_id for unique cache key
        combined = f"{text}|{voice_id}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def clear_cache(self) -> None:
        """Clear the audio cache to free memory"""
        self.audio_cache.clear()
        print("Audio cache cleared")
    
    def get_cache_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            'cache_size': len(self.audio_cache),
            'cache_keys': list(self.audio_cache.keys())[:5]  # First 5 keys for debugging
        }
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices from ElevenLabs
        
        Returns:
            List of voice information
        """
        if not self.client:
            return []
            
        try:
            voice_list = self.client.voices.get_all()
            return [
                {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': getattr(voice, 'category', 'Unknown')
                }
                for voice in voice_list
            ]
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []
    
    def is_available(self) -> bool:
        """
        Check if ElevenLabs service is available
        
        Returns:
            True if API key is set and service is available
        """
        return bool(os.getenv('ELEVEN_LABS_API_KEY'))


# Global instance
voice_service = VoiceService()
