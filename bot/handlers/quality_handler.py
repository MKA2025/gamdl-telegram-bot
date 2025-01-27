from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from ...config.config import AM_QUALITY_OPTIONS

async def show_quality_options(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    url: str
):
    """Show quality selection options"""
    query = update.callback_query
    
    keyboard = []
    for quality, value in AM_QUALITY_OPTIONS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{quality} ({value}kbps)",
                callback_data=f"setq_{quality}_{url}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Select download quality:",
        reply_markup=reply_markup
    )

async def handle_quality_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Handle quality selection callback"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    quality = data.split("_")[1]
    url = "_".join(data.split("_")[2:])
    
    # Store selected quality in user data
    context.user_data['quality'] = quality
    
    # Show download options
    keyboard = [
        [
            InlineKeyboardButton(
                "Download File",
                callback_data=f"dl_file_{url}"
            ),
            InlineKeyboardButton(
                "Download ZIP",
                callback_data=f"dl_zip_{url}"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Quality set to {quality}. Choose download option:",
        reply_markup=reply_markup
    )
