import os
from pathlib import Path

# Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_USERS = [12345678]  # Add admin user IDs
AUTH_CHANNELS = [-1001234567890]  # Add authorized channel IDs
LOG_CHANNEL = -1001234567891  # Log channel ID

# Path Configuration
BASE_DIR = Path(__file__).parent.parent
DOWNLOAD_DIR = BASE_DIR / "data" / "downloads"
CACHE_DIR = BASE_DIR / "data" / "cache"
COOKIES_FILE = BASE_DIR / "config" / "cookies.txt"

# Cache Configuration
CACHE_CLEANUP_INTERVAL = 3600  # Cleanup interval in seconds (1 hour)
MAX_CACHE_AGE = 24 * 3600  # Maximum cache age in seconds (24 hours)

# Download Configuration
MAX_CONCURRENT_DOWNLOADS = 5
ALLOWED_TYPES = ["song", "album", "playlist", "music-video"]
DEFAULT_QUALITY = "HIGH"  # HIGH, MEDIUM, LOW

# Telegram Configuration
MAX_MESSAGE_LENGTH = 4096
MAX_CAPTION_LENGTH = 1024
PROGRESS_UPDATE_INTERVAL = 5  # seconds

# Apple Music Configuration
AM_QUALITY_OPTIONS = {
    "HIGH": "256",
    "MEDIUM": "128",
    "LOW": "64"
}
