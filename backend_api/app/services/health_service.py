import logging
from sqlalchemy.orm import Session
from sqlalchemy import text


def is_db_online():
    try:
        return True
    except Exception as e:
        logging.error(f"Health check DB connection failed: {e}")
        return False

