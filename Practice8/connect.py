import psycopg2
from config import load_config

def connect_db():
    config = load_config()
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as error:
        print(error)