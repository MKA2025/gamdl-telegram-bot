import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_seen DATETIME,
                last_active DATETIME,
                total_downloads INTEGER DEFAULT 0,
                is_authorized BOOLEAN DEFAULT 0
            )
        ''')

        # Create downloads table
        c.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                url TEXT,
                file_type TEXT,
                quality TEXT,
                status TEXT,
                started_at DATETIME,
                completed_at DATETIME,
                file_size INTEGER,
                error_message TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        conn.commit()
        conn.close()

    async def add_user(self, user_id: int, username: str):
        """Add or update user in database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.utcnow()
        c.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_seen, last_active)
            VALUES (?, ?, COALESCE(
                (SELECT first_seen FROM users WHERE user_id = ?),
                ?
            ), ?)
        ''', (user_id, username, user_id, now, now))
        
        conn.commit()
        conn.close()

    async def log_download(
        self,
        user_id: int,
        url: str,
        file_type: str,
        quality: str,
        status: str,
        file_size: Optional[int] = None,
        error_message: Optional[str] = None
    ):
        """Log download attempt"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.utcnow()
        
        c.execute('''
            INSERT INTO downloads (
                user_id, url, file_type, quality, status,
                started_at, completed_at, file_size, error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, url, file_type, quality, status,
            now, now if status == 'completed' else None,
            file_size, error_message
        ))
        
        if status == 'completed':
            c.execute('''
                UPDATE users 
                SET total_downloads = total_downloads + 1,
                    last_active = ?
                WHERE user_id = ?
            ''', (now, user_id))
        
        conn.commit()
        conn.close()

    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT 
                u.total_downloads,
                u.first_seen,
                u.last_active,
                COUNT(CASE WHEN d.status = 'completed' THEN 1 END) as successful_downloads,
                COUNT(CASE WHEN d.status = 'failed' THEN 1 END) as failed_downloads
            FROM users u
            LEFT JOIN downloads d ON u.user_id = d.user_id
            WHERE u.user_id = ?
            GROUP BY u.user_id
        ''', (user_id,))
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {}
            
        return {
            'total_downloads': row[0],
            'first_seen': row[1],
            'last_active': row[2],
            'successful_downloads': row[3],
            'failed_downloads': row[4]
        }
