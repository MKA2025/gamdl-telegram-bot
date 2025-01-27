from telegram import Update
from telegram.ext import ContextTypes

from ...config.config import ADMIN_USERS, AUTH_CHANNELS

async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user authorization"""
    if not update.message:
        return
    
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS:
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return
    
    # Get user to authorize
    try:
        target_user = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Please provide a valid user ID to authorize."
        )
        return
    
    # Add user to authorized users
    if target_user not in AUTH_CHANNELS:
        AUTH_CHANNELS.append(target_user)
        await update.message.reply_text(
            f"✅ User {target_user} has been authorized."
        )
    else:
