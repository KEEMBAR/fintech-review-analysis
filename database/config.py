"""
Database configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'fintech_db'),
    'user': os.getenv('POSTGRES_USER', 'fintech_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'fintech_password'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
} 