import sqlite3
import os
import json
import logging

logger = logging.getLogger("db_manager")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resume_analyzer.db")

def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    # Ensure database folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database tables if they do not exist."""
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Users Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        full_name TEXT,
        target_role TEXT,
        industry TEXT,
        theme_pref TEXT DEFAULT 'dark',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Resumes and Analyses Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS resumes_and_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resume_text TEXT NOT NULL,
        job_title TEXT,
        job_desc TEXT,
        analysis_results_json TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
    logger.info(f"SQLite Database initialized successfully at {DB_PATH}")

# User DB Interactions
def create_user_db(username, password_hash, email, full_name, target_role, industry, theme_pref="dark"):
    """Inserts a new user record into the DB."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, password_hash, email, full_name, target_role, industry, theme_pref)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, password_hash, email, full_name, target_role, industry, theme_pref))
        conn.commit()
        user_id = c.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_db(username):
    """Retrieves a user by username."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id_db(user_id):
    """Retrieves a user's full details by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_db(user_id, email, full_name, target_role, industry):
    """Updates profile information for a user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET email = ?, full_name = ?, target_role = ?, industry = ?
        WHERE id = ?
    """, (email, full_name, target_role, industry, user_id))
    conn.commit()
    conn.close()
    return True

def update_user_password_db(user_id, new_password_hash):
    """Updates password hash for a user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, user_id))
    conn.commit()
    conn.close()
    return True

def update_user_preference_db(user_id, theme_pref):
    """Saves user theme preferences."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET theme_pref = ? WHERE id = ?", (theme_pref, user_id))
    conn.commit()
    conn.close()
    return True

# Analysis History Interactions
def add_analysis_record_db(user_id, filename, resume_text, job_title, job_desc, results_dict):
    """Saves and associates a resume processing audit record to a logged-in user."""
    conn = get_connection()
    c = conn.cursor()
    results_json = json.dumps(results_dict)
    c.execute("""
        INSERT INTO resumes_and_analyses (user_id, filename, resume_text, job_title, job_desc, analysis_results_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, filename, resume_text, job_title, job_desc, results_json))
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    return record_id

def get_analysis_history_db(user_id):
    """Fetches high-level metadata of the active user's scans."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, filename, uploaded_at, job_title, job_desc, analysis_results_json
        FROM resumes_and_analyses
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    
    history_list = []
    for r in rows:
        try:
            res_dict = json.loads(r["analysis_results_json"])
        except Exception:
            res_dict = {}
        history_list.append({
            "id": r["id"],
            "filename": r["filename"],
            "uploaded_at": r["uploaded_at"],
            "job_title": r["job_title"],
            "job_desc": r["job_desc"],
            "analysis_results": res_dict
        })
    return history_list

def delete_analysis_record_db(user_id, record_id):
    """Deletes an audit result row."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM resumes_and_analyses WHERE id = ? AND user_id = ?", (record_id, user_id))
    conn.commit()
    conn.close()
    return True

# Call auto initialization of SQlite Schema upon import
init_db()
