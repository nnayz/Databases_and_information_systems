import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()

DB_PARAMS = {
    'host': os.getenv("PGHOST"),
    'database': os.getenv("PGDATABASE"),
    'user': os.getenv("PGUSER"),
    'password': os.getenv("PGPASSWORD"),
    'port': os.getenv("PGPORT"),
}

def get_connection(isolation_level=None):
    """
    Establishes a database connection.
    If isolation_level is provided, it will be set for the connection.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    if isolation_level:
        if isolation_level == "READ COMMITTED":
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        elif isolation_level == "SERIALIZABLE":
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        else:
            raise ValueError(f"Unsupported isolation level: {isolation_level}")
    return conn

def get_cursor(conn):
    """
    Returns a cursor for the connection.
    """
    return conn.cursor()

def get_engine():
    """
    Returns an SQLAlchemy engine for the database.
    """
    return create_engine(f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}")


