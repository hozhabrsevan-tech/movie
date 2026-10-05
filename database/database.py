import sqlite3


DATABASE_NAME = "database.db"


def connect_db():

    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            movie_title TEXT,
            UNIQUE(user_id, movie_id)
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (user_id, username)
        VALUES (?, ?)
    """, (user_id, username))

    conn.commit()
    conn.close()


def add_favorite(user_id, movie_id, movie_title):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO favorites
        (user_id, movie_id, movie_title)
        VALUES (?, ?, ?)
    """, (
        user_id,
        movie_id,
        movie_title
    ))

    conn.commit()
    conn.close()


def remove_favorite(user_id, movie_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorites
        WHERE user_id = ? AND movie_id = ?
    """, (
        user_id,
        movie_id
    ))

    conn.commit()
    conn.close()


def get_favorites(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT movie_id, movie_title
        FROM favorites
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def is_favorite(user_id, movie_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM favorites
        WHERE user_id = ? AND movie_id = ?
    """, (
        user_id,
        movie_id
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None