import sqlite3
import logging
import os

from config import DATABASE_PATH

# Loglama yapilandirmasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection():
    """Yapilandirilan veritabani dosyasina baglanti ac"""
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    """Veritabanini ve ornek tabloyu olustur"""
    # Veritabani dosyasinin dizini yoksa olustur (or. volume mount noktasi)
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    # Ornek kullanicilar ekle (sifre hash olarak saklanmali)
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password_hash) "
        "VALUES (1, 'admin', 'admin@example.com', 'hashed_admin123')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email, password_hash) "
        "VALUES (2, 'user1', 'user1@example.com', 'hashed_pass456')"
    )
    conn.commit()
    conn.close()
    logger.info("Veritabani basariyla olusturuldu: %s", DATABASE_PATH)


def get_user_secure(username):
    """
    DUZELTILDI: Parametrik sorgu - SQL Injection imkansiz
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Guvenli: ? placeholder ile parametrik sorgu
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchall()
    conn.close()
    return result
