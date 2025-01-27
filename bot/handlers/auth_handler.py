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

        await update.message.reply_text(
            f"ℹ️ User {target_user} is already authorized."
        )

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user authorization revocation"""
    if not update.message:
        return
    
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS:
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return
    
    # Get user to revoke
    try:
        target_user = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Please provide a valid user ID to revoke."
        )
        return
    
    # Remove user from authorized users
    if target_user in AUTH_CHANNELS:
        AUTH_CHANNELS.remove(target_user)
        await update.message.reply_text(
            f"✅ Authorization revoked for user {target_user}."
        )
    else:
        await update.message.reply_text(
            f"ℹ️ User {target_user} is not authorized."
        )

async def check_auth(user_id: int) -> bool:
    """Check if a user is authorized"""
    return user_id in ADMIN_USERS or user_id in AUTH_CHANNELS
