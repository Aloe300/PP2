import psycopg2
from config import database, user

def get_connection():
    conn = psycopg2.connect(
        dbname=database,
        user=user
    )
    return conn