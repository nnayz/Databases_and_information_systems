import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )
    return conn

def get_session():
    session = sessionmaker(bind=get_engine())
    return session()

def get_engine():
    # print(os.getenv("DATABASE_URL"))
    return create_engine(os.getenv("DATABASE_URL"))

    