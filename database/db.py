import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

def get_db():
    """
    Opens a connection to the SQLite database and configures it.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates the necessary database tables.
    """
    with get_db() as conn:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create expenses table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

def create_user(name, email, password):
    """
    Hashes the password and creates a new user in the database.
    Returns the ID of the new user.
    Raises sqlite3.IntegrityError if the email is already taken.
    """
    password_hash = generate_password_hash(password)
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        return cursor.lastrowid

def seed_db():
    """
    Seeds the database with sample data if it's empty.
    """
    with get_db() as conn:
        # Check if users table is empty
        user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
        if user:
            return

        # Insert demo user
        demo_user_data = {
            "name": "Demo User",
            "email": "demo@spendly.com",
            "password": generate_password_hash("demo123")
        }

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (demo_user_data["name"], demo_user_data["email"], demo_user_data["password"])
        )
        user_id = cursor.lastrowid

        # 8 sample expenses
        expenses = [
            (user_id, 12.50, "Food", "2026-07-01", "Lunch at cafe"),
            (user_id, 45.00, "Transport", "2026-07-02", "Weekly fuel"),
            (user_id, 120.00, "Bills", "2026-07-05", "Electricity bill"),
            (user_id, 30.00, "Health", "2026-07-08", "Pharmacy"),
            (user_id, 15.00, "Entertainment", "2026-07-10", "Movie ticket"),
            (user_id, 60.00, "Shopping", "2026-07-12", "New clothes"),
            (user_id, 10.00, "Other", "2026-07-15", "Misc item"),
            (user_id, 25.00, "Food", "2026-07-20", "Dinner date"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses
        )

        conn.commit()
