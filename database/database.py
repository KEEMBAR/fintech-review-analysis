"""
Database connection and management module.
"""
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import logging
from config import DB_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Manages database connections using a connection pool.
    """
    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        """
        Initialize the connection pool if it hasn't been created yet.
        """
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    **DB_CONFIG
                )
                logger.info("Database connection pool initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing database connection pool: {e}")
                raise

    @classmethod
    @contextmanager
    def get_connection(cls):
        """
        Get a connection from the pool.
        
        Yields:
            connection: A database connection from the pool
        """
        if cls._connection_pool is None:
            cls.initialize_pool()
        
        connection = None
        try:
            connection = cls._connection_pool.getconn()
            yield connection
        except Exception as e:
            logger.error(f"Error getting database connection: {e}")
            raise
        finally:
            if connection:
                cls._connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        """
        Close all connections in the pool.
        """
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            logger.info("All database connections closed") 