"""
Database connection module
"""

import os
import json
from pathlib import Path
from sqlalchemy import create_engine
import psycopg2


def get_db_connection():
    """
    Get database connection parameters from environment or config file.
    Priority: ENV vars > Local config > Fallback
    """

    # 1. Try environment variables (for AWS ECS)
    if os.environ.get('DB_PASSWORD'):
        return {
            'host': os.environ.get('DB_HOST', 'datauploader-instance-1.ci6sgcrhrg7k.us-west-1.rds.amazonaws.com'),
            'port': os.environ.get('DB_PORT', '5432'),
            'database': os.environ.get('DB_NAME', 'data_uploader'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD')
        }

    # 2. Try local config file
    config_path = Path.home() / '.vk' / 'db_config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {
                    'host': config.get('host', 'datauploader-instance-1.ci6sgcrhrg7k.us-west-1.rds.amazonaws.com'),
                    'port': config.get('port', '5432'),
                    'database': config.get('database', 'data_uploader'),
                    'user': config.get('user', 'postgres'),
                    'password': config['password']
                }
        except Exception as e:
            print(f"Warning: Could not read config file: {e}")

    # 3. Fallback (for backward compatibility - will be removed)
    print("WARNING: Using fallback credentials. Please set DB_PASSWORD environment variable or create ~/.vk/db_config.json")
    return {
        'host': 'datauploader-instance-1.ci6sgcrhrg7k.us-west-1.rds.amazonaws.com',
        'port': '5432',
        'database': 'data_uploader',
        'user': 'postgres',
        'password': 'Winterandfalcon1!'
    }


def get_connection():
    """Get database connection using credentials from environment or config"""
    config = get_db_connection()

    return psycopg2.connect(
        host=config['host'],
        port=config['port'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )


def PGconnection():
    """Legacy PGconnection function that returns SQLAlchemy engine for sessionmaker compatibility"""
    config = get_db_connection()

    # Create SQLAlchemy engine URL
    db_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    # Return SQLAlchemy engine for use with sessionmaker
    return create_engine(db_url)


# For backward compatibility
def get_db_connection_legacy():
    """Legacy method for backward compatibility"""
    return get_connection()