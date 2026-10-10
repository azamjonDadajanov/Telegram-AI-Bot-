import sqlite3

import datetime

database_name = 'ai_bot.db'

def init_db():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name VARCHAR(50), topic TEXT)
        """
    )

    cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, role VARCHAR(10), message TEXT, date_created DATE, user_id INTEGER)
            """
        )

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute(
        f"""
        SELECT * FROM users WHERE id={telegram_id}
        """
    )
    row = cur.fetchone()

    conn.close()
    return row

def create_user(telegram_id, name):
    conn = sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute(
        f"""
        INSERT INTO users(id, name) VALUES (?,?)
        """,
        (telegram_id, name)
    )
    conn.commit()
    conn.close()

def get_user_topic(telegram_id):
    conn = sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute(
        f"""
        SELECT topic FROM users WHERE id={telegram_id}
        """
    )
    row = cur.fetchone()

    conn.close()
    if row:
        return row[0]
    return None

def set_user_topic(telgram_id, topic):
    conn = sqlite3.connect(database_name)
    cur=conn.cursor()
    cur.execute(
        f"""
        UPDATE users SET topic=?
        WHERE id = ?
        """, (topic, telgram_id)
    )
    conn.close()

def get_messages(telegram_id, limit):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM messages
        WHERE user_id = ?
        ORDER BY id DESC LIMIT ?
        """,
        (telegram_id, limit)
    )
    conn.commit()
    conn.close()

def create_messages(telegram_id, message, role,):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO messages(role, message, date_created, user_id)
        VALUES
        (?, ?, ?, ?)
        """,
        (role, message, telegram_id, datetime.datetime.now())
    )
    conn.commit()
    conn.close()