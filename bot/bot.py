import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from .handlers import (
    auth_handler,
    command_handler,
    download_handler
)
from .utils.cache import CacheManager
from .utils.formatter import format_message
from gamdl.downloader import Downloader

logger = logging.getLogger(__name__)

class GamdlBot:
    def __init__(
        self,
        token: str,
        admin_users: List[int],
        auth_channels: List[int],
        log_channel: int,
        cache_cleanup_interval: int
    ):
        self.token = token
        self.admin_users = admin_users
        self.auth_channels = auth_channels
        self.log_channel = log_channel
        
        # Initialize the application
        self.app = Application.builder().token(self.token).build()
        
        # Initialize cache manager
        self.cache_manager = CacheManager(cleanup_interval=cache_cleanup_interval)
        
        # Initialize downloader
        self.downloader = Downloader()
        
        # Setup handlers
        self._setup_handlers()

    def _setup_handlers(self):
        # Command handlers
        self.app.add_handler(CommandHandler("start", command_handler.start))
        self.app.add_handler(CommandHandler("help", command_handler.help))
        self.app.add_handler(CommandHandler("settings", command_handler.settings))
        self.app.add_handler(CommandHandler("stats", command_handler.stats))
        
        # Auth handlers
        self.app.add_handler(CommandHandler("auth", auth_handler.authorize))
        self.app.add_handler(CommandHandler("revoke", auth_handler.revoke))
        
        # Download handlers
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_handler.handle_download
        ))
        self.app.add_handler(CallbackQueryHandler(
            download_handler.handle_callback
        ))
        
        # Error handler
        self.app.add_error_handler(self._error_handler)

    async def _error_handler(
        self,
        update: Optional[Update],
        context: ContextTypes.DEFAULT_TYPE
    ):
        """Log errors and send a message to admin users"""
        logger.error(
            f"Exception while handling an update: {context.error}",
            exc_info=context.error
        )
        
        error_msg = (
            f"❌ Error occurred at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"Error: {str(context.error)}\n"
        )
        
        # Notify admins
        for admin_id in self.admin_users:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=error_msg
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")

    def run(self):
        """Start the bot"""
        logger.info("Starting bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
