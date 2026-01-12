import sqlite3
import pandas as pd
import os

DB_PATH = "data/salon.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            client TEXT NOT NULL,
            service TEXT NOT NULL,
            employee TEXT NOT NULL,
            price REAL NOT NULL,
            duration INTEGER NOT NULL
        )
        """)

def insert_appointment(data):
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO appointments
        (date, client, service, employee, price, duration)
        VALUES (?, ?, ?, ?, ?, ?)
        """, data)

def load_appointments():
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM appointments ORDER BY date DESC", conn)

def delete_appointment(appointment_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM appointments WHERE id = ?",
        (appointment_id,)
    )

    conn.commit()
    conn.close()