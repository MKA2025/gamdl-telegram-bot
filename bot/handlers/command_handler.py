telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from ...config.config import ADMIN_USERS, AUTH_CHANNELS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = (
        "👋 Welcome to Gamdl Music Bot!\n\n"
        "This bot helps you download music from Apple Music.\n"
        "Simply send an Apple Music link to start downloading.\n\n"
        "Available commands:\n"
        "/help - Show help message\n"
        "/settings - Show current settings\n"
        "/stats - Show bot statistics (admin only)\n"
    )
    await update.message.reply_text(welcome_message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = (
        "📖 Gamdl Music Bot Help\n\n"
        "How to use:\n"
        "1. Send an Apple Music link\n"
        "2. Choose download options (Single file or ZIP)\n"
        "3. Select quality if needed\n\n"
        "Supported content types:\n"
        "- Songs\n"
        "- Albums\n"
        "- Playlists\n"
        "- Music Videos\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/settings - Show current settings\n"
        "/stats - Show bot statistics (admin only)\n"
        "/auth <user_id> - Authorize user (admin only)\n"
        "/revoke <user_id> - Revoke authorization (admin only)\n"
    )
    await update.message.reply_text(help_message)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user_id = update.effective_user.id
    settings_message = (
        "⚙️ Current Settings\n\n"
        f"User ID: {user_id}\n"
        f"Authorization Status: {'Authorized' if await check_auth(user_id) else 'Unauthorized'}\n"
        f"Admin Status: {'Yes' if user_id in ADMIN_USERS else 'No'}\n"
        f"Max Download Quality: {context.user_data.get('quality', 'HIGH')}\n"
        f"Auto-ZIP large downloads: {context.user_data.get('auto_zip', 'Yes')}\n"
    )
    await update.message.reply_text(settings_message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command (admin only)"""
    if update.effective_user.id not in ADMIN_USERS:
        await update.message.reply_text("❌ This command is for admins only.")
        return

    # Get current stats
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    stats_message = (
        "📊 Bot Statistics\n\n"
        f"Current Time: {current_time}\n"
        f"Total Authorized Users: {len(AUTH_CHANNELS)}\n"
        f"Active Downloads: {len(context.dispatcher.running_jobs)}\n"
        f"Total Admins: {len(ADMIN_USERS)}\n"
    )
    await update.message.reply_text(stats_message)
