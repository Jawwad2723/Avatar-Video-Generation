"""
Avatar Video Generator Module
Creates AI avatar videos with lip-sync using D-ID API
"""

import requests
import logging
import time
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class AvatarVideoGenerator:
    """
    Generates avatar videos using D-ID API
    """
    
    def __init__(self):
        """
        Initialize D-ID API client
        """
        self.api_key = settings.DID_API_KEY
        self.base_url = settings.DID_BASE_URL
        self.presenter_id = settings.DID_PRESENTER_ID
        self.voice_id = settings.DID_VOICE_ID
        
        self.headers = {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Initialized AvatarVideoGenerator with D-ID")
    
    def generate_video(self, script: str, wait_for_completion: bool = True) -> str:
        """
        Generate avatar video from script
        
        Args:
            script: News anchor script text
            wait_for_completion: Whether to wait for video generation
            
        Returns:
            URL of generated video
        """
        try:
            logger.info("Starting video generation with D-ID")
            
            # Create talk (video generation request)
            talk_id = self._create_talk(script)
            
            if not wait_for_completion:
                logger.info(f"Video generation started. Talk ID: {talk_id}")
                return f"Video generation in progress. Talk ID: {talk_id}"
            
            # Wait for video to be ready
            video_url = self._wait_for_video(talk_id)
            
            logger.info(f"Video generated successfully: {video_url}")
            return video_url
            
        except Exception as e:
            logger.error(f"Error generating video: {str(e)}")
            raise ValueError(f"Failed to generate video: {str(e)}")
    
    def _create_talk(self, script: str) -> str:
        """
        Create a new talk (video generation) via D-ID API
        
        Args:
            script: Script text for avatar to speak
            
        Returns:
            Talk ID
        """
        try:
            endpoint = f"{self.base_url}/talks"
            
            payload = {
                "script": {
                    "type": "text",
                    "input": script,
                    "provider": {
                        "type": "microsoft",
                        "voice_id": self.voice_id
                    }
                },
                "config": {
                    "fluent": True,
                    "pad_audio": 0.0,
                    "stitch": True
                },
                "source_url": f"https://create-images-results.d-id.com/DefaultPresenters/{self.presenter_id}/image.jpeg"
            }
            
            logger.info(f"Creating talk with D-ID API")
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 401:
                raise ValueError("D-ID authentication failed. Check API key.")
            
            response.raise_for_status()
            
            data = response.json()
            talk_id = data.get('id')
            
            if not talk_id:
                raise ValueError("No talk ID returned from D-ID API")
            
            logger.info(f"Talk created successfully. ID: {talk_id}")
            return talk_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"D-ID API request failed: {str(e)}")
            raise ValueError(f"D-ID API error: {str(e)}")
    
    def _wait_for_video(self, talk_id: str, max_wait_seconds: int = 300) -> str:
        """
        Poll D-ID API until video is ready
        
        Args:
            talk_id: Talk ID to check
            max_wait_seconds: Maximum time to wait
            
        Returns:
            Video URL when ready
        """
        endpoint = f"{self.base_url}/talks/{talk_id}"
        start_time = time.time()
        
        logger.info(f"Waiting for video generation (max {max_wait_seconds}s)")
        
        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > max_wait_seconds:
                raise TimeoutError(f"Video generation exceeded {max_wait_seconds}s timeout")
            
            try:
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                status = data.get('status')
                
                logger.info(f"Video status: {status} (elapsed: {elapsed:.0f}s)")
                
                if status == 'done':
                    video_url = data.get('result_url')
                    if not video_url:
                        raise ValueError("No video URL in completed response")
                    return video_url
                
                elif status == 'error':
                    error_msg = data.get('error', {}).get('description', 'Unknown error')
                    raise ValueError(f"Video generation failed: {error_msg}")
                
                elif status in ['created', 'started']:
                    # Still processing, wait and retry
                    time.sleep(5)
                    continue
                
                else:
                    logger.warning(f"Unknown status: {status}")
                    time.sleep(5)
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error checking video status: {str(e)}")
                time.sleep(5)
                continue
    
    def get_video_status(self, talk_id: str) -> dict:
        """
        Get current status of video generation
        
        Args:
            talk_id: Talk ID to check
            
        Returns:
            Status dictionary
        """
        try:
            endpoint = f"{self.base_url}/talks/{talk_id}"
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting video status: {str(e)}")
            raise
    
    def delete_video(self, talk_id: str) -> bool:
        """
        Delete a generated video
        
        Args:
            talk_id: Talk ID to delete
            
        Returns:
            True if successful
        """
        try:
            endpoint = f"{self.base_url}/talks/{talk_id}"
            
            response = requests.delete(
                endpoint,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Deleted video: {talk_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting video: {str(e)}")
            return False