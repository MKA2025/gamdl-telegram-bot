import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DownloadQueue:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.current_downloads: Dict[int, Dict] = {}  # user_id: download_info
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def add_to_queue(
        self,
        user_id: int,
        url: str,
        quality: str,
        message_id: int
    ):
        """Add download request to queue"""
        download_info = {
            'user_id': user_id,
            'url': url,
            'quality': quality,
            'message_id': message_id,
            'status': 'queued',
            'progress': 0,
            'start_time': None,
            'finish_time': None
        }
        
        await self.queue.put(download_info)
        return len(self.current_downloads) + self.queue.qsize()

    async def start_download(self, download_info: Dict):
        """Start a download"""
        async with self.semaphore:
            user_id = download_info['user_id']
            download_info['status'] = 'downloading'
            download_info['start_time'] = datetime.utcnow()
            self.current_downloads[user_id] = download_info
            
            try:
                # Actual download logic here
                await self._process_download(download_info)
                
                download_info['status'] = 'completed'
            except Exception as e:
                download_info['status'] = 'failed'
                download_info['error'] = str(e)
                logger.error(f"Download failed for user {user_id}: {e}")
            finally:
                download_info['finish_time'] = datetime.utcnow()
                del self.current_downloads[user_id]

    async def _process_download(self, download_info: Dict):
        """Process the actual download"""
        # Implement the actual download logic here
        pass

    def get_download_status(self, user_id: int) -> Optional[Dict]:
        """Get current download status for user"""
        return self.current_downloads.get(user_id)

    def cancel_download(self, user_id: int) -> bool:
        """Cancel download for user"""
        if user_id in self.current_downloads:
            self.current_downloads[user_id]['status'] = 'cancelled'
            return True
        return False
