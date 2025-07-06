import os
import shutil
import asyncio
from dbagent.manage_log import get_logger

logger = get_logger(module_name=__name__)

async def create_directories_async(path="db-agent"):
    history_path = os.path.join(path, "history")
    try:
        await asyncio.to_thread(os.makedirs, path, exist_ok=True)
        await asyncio.to_thread(os.makedirs, history_path, exist_ok=True)
        logger.info(f"Created directories: {path}, {history_path}")
    except OSError as e:
        logger.error(f"Directory creation failed: {e}")

async def clear_local_db_folder(path="db-agent"):
    if os.path.exists(path):
        shutil.rmtree(path)
        logger.info(f"Cleared folder: {path}")
    else:
        logger.info(f"Folder not found: {path}")
