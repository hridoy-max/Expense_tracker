import sqlite3
from werkzeug.security import generate_password_hash
from flask import current_app

def get_db():
    """
    Opens a connection to the SQLite database configured in the app.
    """
    db_path = current_app.config.get('DATABASE', "spendly.db")
    conn = sqlite3.connect(db_path)
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

def get_user_by_email(email):
    """
    Retrieves a user record by their email address.
    Returns the user row if found, otherwise None.
    """
    with get_db() as conn:
        return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

def get_user_by_id(user_id):
    """
    Retrieves a user record by their ID.
    Returns the user row if found, otherwise None.
    """
    with get_db() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def get_user_stats(user_id, date_from=None, date_to=None):
    """
    Calculates summary statistics for a user's expenses.
    Returns a dictionary with total_spent, transaction_count, and top_category.
    """
    with get_db() as conn:
        # Base filter
        where_clause = "WHERE user_id = ?"
        params = [user_id]

        if date_from and date_to:
            where_clause += " AND date BETWEEN ? AND ?"
            params.extend([date_from, date_to])

        # Total spent
        res_total = conn.execute(f"SELECT SUM(amount) as total FROM expenses {where_clause}", params).fetchone()
        total_spent = res_total['total'] if res_total and res_total['total'] is not None else 0.0

        # Transaction count
        res_count = conn.execute(f"SELECT COUNT(*) as count FROM expenses {where_clause}", params).fetchone()
        transaction_count = res_count['count'] if res_count else 0

        # Top category
        res_top = conn.execute(
            f"SELECT category FROM expenses {where_clause} GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            params
        ).fetchone()
        top_category = res_top['category'] if res_top else None

        return {
            "total_spent": total_spent,
            "transaction_count": transaction_count,
            "top_category": top_category
        }


def get_user_transactions(user_id, limit=5, date_from=None, date_to=None):
    """
    Retrieves the most recent transactions for a user.
    """
    with get_db() as conn:
        where_clause = "WHERE user_id = ?"
        params = [user_id]

        if date_from and date_to:
            where_clause += " AND date BETWEEN ? AND ?"
            params.extend([date_from, date_to])

        params.append(limit)

        return conn.execute(
            f"SELECT id, date, description, category, amount FROM expenses {where_clause} ORDER BY date DESC LIMIT ?",
            params
        ).fetchall()


def get_category_breakdown(user_id, date_from=None, date_to=None):
    """
    Calculates the spending breakdown by category for a user.
    Returns a list of dictionaries with category, amount, and percentage.
    """
    with get_db() as conn:
        where_clause = "WHERE user_id = ?"
        params = [user_id]

        if date_from and date_to:
            where_clause += " AND date BETWEEN ? AND ?"
            params.extend([date_from, date_to])

        rows = conn.execute(
            f"SELECT category, SUM(amount) as total FROM expenses {where_clause} GROUP BY category",
            params
        ).fetchall()

        if not rows:
            return []

        grand_total = sum(row['total'] for row in rows)
        breakdown = []

        for row in rows:
            percentage = (row['total'] / grand_total * 100) if grand_total > 0 else 0
            breakdown.append({
                "category": row['category'],
                "amount": row['total'],
                "percentage": round(percentage, 1)
            })

        return breakdown


def insert_expense(user_id, amount, category, date, description):
    """
    Inserts a new expense record for a user.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, date, description if description and description.strip() else None)
        )
        conn.commit()
        return cursor.lastrowid


def get_expense_by_id(expense_id):
    """
    Retrieves a single expense record by its ID.
    Returns the row if found, otherwise None.
    """
    with get_db() as conn:
        return conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()


def update_expense(expense_id, user_id, amount, category, date, description):
    """
    Updates an existing expense record for a user.
    Returns the number of rows affected.
    """
    description = description if description and description.strip() else None
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ? AND user_id = ?",
            (amount, category, date, description, expense_id, user_id)
        )
        conn.commit()
        return cursor.rowcount


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
