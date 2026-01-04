import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def is_db_online(db: AsyncSession) -> bool:
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logging.error(f"Health check DB connection failed: {e}")
        return False
