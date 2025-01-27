import asyncio
from typing import Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from ...config.config import (
    DOWNLOAD_DIR,
    MAX_CONCURRENT_DOWNLOADS,
    ALLOWED_TYPES
)
from ..utils.compress import create_zip
from ..utils.formatter import format_progress

class DownloadStatus:
    def __init__(self):
        self.active_downloads = {}
        self.download_semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

download_status = DownloadStatus()

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle download requests from users"""
    message = update.message
    url = message.text.strip()
    
    # Validate URL
    if not is_valid_apple_music_url(url):
        await message.reply_text(
            "❌ Invalid Apple Music URL. Please provide a valid Apple Music link."
        )
        return

    # Check if user is authorized
    if not await is_user_authorized(message.from_user.id, context):
        await message.reply_text(
            "❌ You are not authorized to use this bot. Please contact an admin."
        )
        return

    # Create download buttons
    keyboard = [
        [
            InlineKeyboardButton("Download File", callback_data=f"dl_file_{url}"),
            InlineKeyboardButton("Download ZIP", callback_data=f"dl_zip_{url}")
        ],
        [
            InlineKeyboardButton("Select Quality", callback_data=f"quality_{url}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        "Please choose download options:",
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline buttons"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("dl_file_"):
        url = data.replace("dl_file_", "")
        await start_download(update, context, url, zip_file=False)
    elif data.startswith("dl_zip_"):
        url = data.replace("dl_zip_", "")
        await start_download(update, context, url, zip_file=True)
    elif data.startswith("quality_"):
        url = data.replace("quality_", "")
        await show_quality_options(update, context, url)

async def start_download(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    url: str,
    zip_file: bool = False
):
    """Start the download process"""
    async with download_status.download_semaphore:
        message = await update.effective_message.edit_text(
            "⏳ Starting download..."
        )
        
        try:
            # Download using gamdl
            download_path = DOWNLOAD_DIR / str(update.effective_user.id)
            download_path.mkdir(parents=True, exist_ok=True)
            
            result = await download_content(url, download_path)
            
            if zip_file:
                zip_path = await create_zip(download_path, result['files'])
                await send_zip_file(update, context, zip_path)
            else:
                await send_individual_files(update, context, result['files'])
                
        except Exception as e:
            await message.edit_text(f"❌ Download failed: {str(e)}")
            return
        finally:
            # Cleanup
            if download_path.exists():
                shutil.rmtree(download_path)

def is_valid_apple_music_url(url: str) -> bool:
    """Validate Apple Music URL"""
    # Add URL validation logic
    return True

async def is_user_authorized(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user is authorized"""
    # Add authorization logic
    return True
