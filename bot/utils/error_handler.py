import logging
from typing import Optional, Callable
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class BotError(Exception):
    """Base class for bot errors"""
    def __init__(self, message: str, user_friendly_message: Optional[str] = None):
        super().__init__(message)
        self.user_friendly_message = user_friendly_message or message

class DownloadError(BotError):
    """Raised when download fails"""
    pass

class AuthorizationError(BotError):
    """Raised when user is not authorized"""
    pass

class QualityError(BotError):
    """Raised when quality selection fails"""
    pass

def handle_errors(func: Callable):
    """Decorator to handle errors in bot commands"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except AuthorizationError as e:
            await update.effective_message.reply_text(
                f"❌ Authorization Error: {e.user_friendly_message}"
            )
        except DownloadError as e:
            await update.effective_message.reply_text(
                f"❌ Download Failed: {e.user_friendly_message}"
            )
        except QualityError as e:
            await update.effective_message.reply_text(
                f"❌ Quality Selection Error: {e.user_friendly_message}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            await update.effective_message.reply_text(
                "❌ An unexpected error occurred. Please try again later."
            )
    
    return wrapper
