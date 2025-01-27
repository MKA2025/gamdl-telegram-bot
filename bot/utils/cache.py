import asyncio
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from ...config.config import CACHE_DIR, MAX_CACHE_AGE

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cleanup_interval: int):
        self.cleanup_interval = cleanup_interval
        self.cache_dir = CACHE_DIR
        self._cleanup_task: Optional[asyncio.Task] = None

    async def start_cleanup_task(self):
        """Start the periodic cache cleanup task"""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self):
        """Periodically clean up old cache files"""
        while True:
            try:
                await self.cleanup_old_files()
                await asyncio.sleep(self.cleanup_interval)
            except Exception as e:
                logger.error(f"Error during cache cleanup: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    async def cleanup_old_files(self):
        """Clean up files older than MAX_CACHE_AGE"""
        current_time = datetime.now()
        cleanup_before = current_time - timedelta(seconds=MAX_CACHE_AGE)
        
        try:
            for path in self.cache_dir.rglob("*"):
                if path.is_file():
                    mtime = datetime.fromtimestamp(path.stat().st_mtime)
                    if mtime < cleanup_before:
                        try:
                            path.unlink()
                            logger.info(f"Deleted old cache file: {path}")
                        except Exception as e:
                            logger.error(f"Failed to delete cache file {path}: {e}")
                elif path.is_dir():
                    try:
                        # Remove empty directories
                        if not any(path.iterdir()):
                            path.rmdir()
                            logger.info(f"Removed empty cache directory: {path}")
                    except Exception as e:
                        logger.error(f"Failed to remove directory {path}: {e}")
        
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")

    async def clear_user_cache(self, user_id: int):
        """Clear cache for a specific user"""
        user_cache_dir = self.cache_dir / str(user_id)
        if user_cache_dir.exists():
            try:
                shutil.rmtree(user_cache_dir)
                logger.info(f"Cleared cache for user {user_id}")
            except Exception as e:
                logger.error(f"Failed to clear cache for user {user_id}: {e}")
