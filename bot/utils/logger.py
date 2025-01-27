import logging
from datetime import datetime
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError

from ...config.config import LOG_CHANNEL

logger = logging.getLogger(__name__)

class LogChannelHandler:
    def __init__(self, bot: Bot, log_channel_id: int):
        self.bot = bot
        self.log_channel_id = log_channel_id

    async def log_download(
        self,
        user_id: int,
        content_url: str,
        status: str,
        error: Optional[str] = None
    ):
        """Log download activity to the log channel"""
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        log_message = (
            f"📥 Download Log\n\n"
            f"Time: {current_time}\n"
            f"User ID: {user_id}\n"
            f"Content: {content_url}\n"
            f"Status: {status}\n"
        )
        
        if error:
            log_message += f"Error: {error}\n"
        
        try:
            await self.bot.send_message(
                chat_id=self.log_channel_id,
                text=log_message
            )
        except TelegramError as e:
            logger.error(f"Failed to send log message: {e}")

    async def log_auth_event(
        self,
        admin_id: int,
        target_user_id: int,
        action: str
    ):
        """Log authorization events"""
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        log_message = (
            f"🔐 Authorization Event\n\n"
            f"Time: {current_time}\n"
            f"Admin: {admin_id}\n"
            f"Target User: {target_user_id}\n"
            f"Action: {action}\n"
        )
        
        try:
            await self.bot.send_message(
                chat_id=self.log_channel_id,
                text=log_message
            )
        except TelegramError as e:
            logger.error(f"Failed to send auth log message: {e}")
