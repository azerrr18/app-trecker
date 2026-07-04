import sqlite3


def create_connection():
    conn = sqlite3.connect("database.db")
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS learning_sessions(
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INTEGER NOT NULL,
    additional_notes TEXT
    ) """
    )

    conn.commit()
    conn.close()


def add_learning_session(title, category, duration_minutes, additional_notes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO learning_sessions (title, category, duration_minutes, additional_notes) VALUES (?, ?, ?, ?)",
        (title, category, duration_minutes, additional_notes),
    )
    conn.commit()
    conn.close()


def get_all_learning_sessions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT session_id, title, category, date_added, duration_minutes, additional_notes "
        "FROM learning_sessions ORDER BY date_added DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_learning_session(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM learning_sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def update_learning_session(session_id, title, category, duration_minutes, additional_notes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE learning_sessions SET title = ?,category = ?, duration_minutes = ?,additional_notes = ? WHERE session_id = ?",
     (title, category, duration_minutes, additional_notes, session_id))
    conn.commit()
    conn.close()
