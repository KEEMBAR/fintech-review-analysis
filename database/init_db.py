"""
Database initialization script.
"""
import logging
from database import DatabaseConnection
from schema import CREATE_TABLES, CREATE_INDEXES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """
    Initialize the database by creating all necessary tables and indexes.
    """
    try:
        with DatabaseConnection.get_connection() as conn:
            with conn.cursor() as cur:
                # Create tables
                for table_name, create_table_sql in CREATE_TABLES.items():
                    logger.info(f"Creating table: {table_name}")
                    cur.execute(create_table_sql)
                
                # Create indexes
                for index_name, create_index_sql in CREATE_INDEXES.items():
                    logger.info(f"Creating index: {index_name}")
                    cur.execute(create_index_sql)
                
                conn.commit()
                logger.info("Database initialization completed successfully")
                return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    init_database() 