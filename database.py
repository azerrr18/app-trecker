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

def get_learning_session_by_id(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, category, date_added, duration_minutes, additional_notes FROM learning_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return row

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

def get_today_minutes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(duration_minutes) FROM learning_sessions WHERE date(date_added) = date('now')")
    total_minutes = cursor.fetchone()[0]
    conn.close()
    return total_minutes

def get_weekly_minutes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(duration_minutes) FROM learning_sessions WHERE date(date_added) >= date('now','-6 days')"

    )
    total_minutes = cursor.fetchone()[0]
    conn.close()
    return total_minutes

def get_minutes_by_category():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(duration_minutes) FROM learning_sessions GROUP BY category"
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_number_of_sessions_today():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM learning_sessions WHERE date(date_added) = date('now')")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def order_sessions_by_duration():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT session_id, title, category, date_added, duration_minutes, additional_notes FROM learning_sessions ORDER BY duration_minutes DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_monthly_minutes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(duration_minutes) FROM learning_sessions WHERE strftime('%Y-%m', date_added) = strftime('%Y-%m', 'now')"
    )
    total_minutes = cursor.fetchone()[0]
    conn.close()
    return total_minutes

def get_number_of_sessions_this_month():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM learning_sessions WHERE strftime('%Y-%m', date_added) = strftime('%Y-%m', 'now')"
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count




