import psycopg2
from psycopg2 import OperationalError

def connect():
    try:
        conn = psycopg2.connect(
            dbname="master",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print("Koneksi sukses!")
        return conn
    except OperationalError as e:
        print(f"Koneksi gagal: {e}")
        return None

def disconnect(conn):
    if conn:
        conn.close()
        print("Koneksi ditutup.")
