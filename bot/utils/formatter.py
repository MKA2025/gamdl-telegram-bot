from typing import Dict, Any
from pathlib import Path

def format_progress(current: int, total: int, status: str = "") -> str:
    """Format download progress message"""
    progress = min(current / total, 1.0)
    blocks = int(round(20 * progress))
    progress_bar = "█" * blocks + "░" * (20 - blocks)
    percentage = progress * 100
    
    return (
        f"📥 Downloading...\n"
        f"[{progress_bar}] {percentage:.1f}%\n"
        f"{format_size(current)}/{format_size(total)}\n"
        f"{status}"
    )

def format_size(size_in_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f}{unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f}GB"

def format_track_info(track_data: Dict[str, Any]) -> str:
    """Format track information message"""
    return (
        f"🎵 {track_data.get('title', 'Unknown Title')}\n"
        f"👤 {track_data.get('artist', 'Unknown Artist')}\n"
        f"💿 {track_data.get('album', 'Unknown Album')}\n"
        f"🎼 Quality: {track_data.get('quality', 'Unknown')}\n"
    )

def format_download_complete(file_path: Path, duration: float) -> str:
    """Format download completion message"""
    return (
        f"✅ Download Complete!\n\n"
        f"📁 File: {file_path.name}\n"
        f"📦 Size: {format_size(file_path.stat().st_size)}\n"
        f"⏱ Time taken: {duration:.1f}s"
    )
