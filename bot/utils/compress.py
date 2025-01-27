import logging
import zipfile
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

async def create_zip(
    base_path: Path,
    files: List[Path],
    chunk_size: int = 2048
) -> Path:
    """Create a ZIP file from the given files"""
    zip_path = base_path / "download.zip"
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                if file.exists():
                    arcname = file.relative_to(base_path)
                    zip_file.write(file, arcname)
        
        logger.info(f"Created ZIP file: {zip_path}")
        return zip_path
    
    except Exception as e:
        logger.error(f"Failed to create ZIP file: {e}")
        raise
