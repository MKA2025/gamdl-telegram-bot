import logging
import sys
from datetime import datetime
from pathlib import Path

from bot.bot import GamdlBot
from config.config import (
    BOT_TOKEN,
    ADMIN_USERS,
    AUTH_CHANNELS,
    LOG_CHANNEL,
    CACHE_CLEANUP_INTERVAL
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    # Ensure required directories exist
    Path("data/downloads").mkdir(parents=True, exist_ok=True)
    Path("data/cache").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    logger.info(f"Starting bot at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    try:
        bot = GamdlBot(
            token=BOT_TOKEN,
            admin_users=ADMIN_USERS,
            auth_channels=AUTH_CHANNELS,
            log_channel=LOG_CHANNEL,
            cache_cleanup_interval=CACHE_CLEANUP_INTERVAL
        )
        bot.run()
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
