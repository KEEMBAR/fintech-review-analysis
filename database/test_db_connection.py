"""
Test script to verify database connectivity.
"""
from database import DatabaseConnection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """
    Test the database connection and print PostgreSQL version.
    """
    try:
        with DatabaseConnection.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT version();')
                version = cur.fetchone()
                logger.info(f"Successfully connected to PostgreSQL. Version: {version[0]}")
                return True
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return False

if __name__ == "__main__":
    test_connection() 