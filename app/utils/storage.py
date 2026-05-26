import sqlite3
import json
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            brand TEXT,
            model TEXT,
            engine_type TEXT,
            engine_code TEXT,
            vin TEXT,
            symptoms TEXT,
            obd_data TEXT,
            prediction_results TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(username: str, email: str, password_hash: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, datetime.now().isoformat()))

        conn.commit()
        return True, "Cont creat cu succes."
    except sqlite3.IntegrityError:
        return False, "Username sau email deja folosit."
    finally:
        conn.close()


def get_user_by_username_or_email(identifier: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, email, password_hash
        FROM users
        WHERE username = ? OR email = ?
    """, (identifier, identifier))

    user = cursor.fetchone()
    conn.close()

    return user


def save_diagnosis(user_id: int, vehicle_data: dict, symptoms: list, obd_data: dict, prediction_results: list):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO diagnosis_history (
            user_id,
            brand,
            model,
            engine_type,
            engine_code,
            vin,
            symptoms,
            obd_data,
            prediction_results,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        vehicle_data.get("brand"),
        vehicle_data.get("model"),
        vehicle_data.get("engine_type"),
        vehicle_data.get("engine_code"),
        vehicle_data.get("vin"),
        json.dumps(symptoms, ensure_ascii=False),
        json.dumps(obd_data, ensure_ascii=False),
        json.dumps(prediction_results, ensure_ascii=False),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_history_for_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            brand,
            model,
            engine_type,
            engine_code,
            vin,
            symptoms,
            obd_data,
            prediction_results,
            created_at
        FROM diagnosis_history
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows
def delete_diagnosis(diagnosis_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM diagnosis_history
        WHERE id = ? AND user_id = ?
    """, (diagnosis_id, user_id))

    conn.commit()
    conn.close()