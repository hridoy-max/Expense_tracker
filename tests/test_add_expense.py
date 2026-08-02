import pytest
import os
from app import app
from database.db import get_db, insert_expense
import sqlite3

@pytest.fixture
def client(tmp_path):
    # Use a unique temporary database for each test to avoid locking and integrity issues
    db_file = tmp_path / "test_spendly.db"
    app.config['TESTING'] = True
    app.config['DATABASE'] = str(db_file)

    with app.app_context():
        # Initialize test database
        from database.db import init_db
        init_db()

        # Create a test user
        conn = get_db()
        try:
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Test User", "test@example.com", "pbkdf2:sha256:123456")
            )
            conn.commit()
        finally:
            conn.close()

    with app.test_client() as client:
        yield client

def test_insert_expense_valid(client):
    """Unit test: insert_expense with valid data."""
    with app.app_context():
        conn = get_db()
        try:
            user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = user['id']

            expense_id = insert_expense(user_id, 50.0, "Food", "2026-03-20", "Lunch")

            row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
            assert row is not None
            assert row['amount'] == 50.0
            assert row['category'] == "Food"
            assert row['date'] == "2026-03-20"
            assert row['description'] == "Lunch"
        finally:
            conn.close()

def test_insert_expense_no_description(client):
    """Unit test: insert_expense with description=None."""
    with app.app_context():
        conn = get_db()
        try:
            user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = user['id']

            expense_id = insert_expense(user_id, 50.0, "Food", "2026-03-20", None)

            row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
            assert row is not None
            assert row['description'] is None
        finally:
            conn.close()

def test_get_add_expense_unauthenticated(client):
    """Route test: GET /expenses/add redirects to login when unauthenticated."""
    response = client.get('/expenses/add', follow_redirects=False)
    assert response.status_code == 302
    assert response.location.endswith('/login')

def test_get_add_expense_authenticated(client):
    """Route test: GET /expenses/add returns 200 for authenticated users."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    response = client.get('/expenses/add')
    assert response.status_code == 200
    assert b'amount' in response.data
    assert b'category' in response.data
    assert b'date' in response.data
    assert b'Food' in response.data
    assert b'Transport' in response.data
    assert b'Bills' in response.data
    assert b'Health' in response.data
    assert b'Entertainment' in response.data
    assert b'Shopping' in response.data
    assert b'Other' in response.data

def test_post_add_expense_unauthenticated(client):
    """Route test: POST /expenses/add redirects to login when unauthenticated."""
    response = client.post('/expenses/add', data={'amount': 50, 'category': 'Food', 'date': '2026-03-20'}, follow_redirects=False)
    assert response.status_code == 302
    assert response.location.endswith('/login')

def test_post_add_expense_valid(client):
    """Route test: POST /expenses/add saves expense and redirects to profile."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    response = client.post('/expenses/add', data={
        'amount': '50.0',
        'category': 'Food',
        'date': '2026-03-20',
        'description': 'Lunch'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert response.location.endswith('/profile')

    with app.app_context():
        conn = get_db()
        try:
            row = conn.execute("SELECT * FROM expenses WHERE amount = 50.0 AND category = 'Food' AND date = '2026-03-20'").fetchone()
            assert row is not None
            assert row['description'] == 'Lunch'
        finally:
            conn.close()

def test_post_add_expense_invalid_amount(client):
    """Route test: POST /expenses/add handles invalid amount."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    # Case 1: Missing amount
    response = client.post('/expenses/add', data={
        'amount': '',
        'category': 'Food',
        'date': '2026-03-20'
    })
    assert response.status_code == 200
    assert b'Please enter a valid numeric amount' in response.data

    # Case 2: Zero amount
    response = client.post('/expenses/add', data={
        'amount': '0',
        'category': 'Food',
        'date': '2026-03-20'
    })
    assert response.status_code == 200
    assert b'Amount must be a positive number' in response.data

    # Case 3: Non-numeric amount
    response = client.post('/expenses/add', data={
        'amount': 'abc',
        'category': 'Food',
        'date': '2026-03-20'
    })
    assert response.status_code == 200
    assert b'Please enter a valid numeric amount' in response.data

def test_post_add_expense_invalid_category(client):
    """Route test: POST /expenses/add handles invalid category."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    response = client.post('/expenses/add', data={
        'amount': '50.0',
        'category': 'InvalidCat',
        'date': '2026-03-20'
    })
    assert response.status_code == 200
    assert b'Please select a valid category' in response.data

def test_post_add_expense_invalid_date(client):
    """Route test: POST /expenses/add handles invalid date."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    response = client.post('/expenses/add', data={
        'amount': '50.0',
        'category': 'Food',
        'date': 'not-a-date'
    })
    assert response.status_code == 200
    assert b'Invalid date format' in response.data

def test_post_add_expense_optional_description(client):
    """Route test: POST /expenses/add handles missing description."""
    with client.session_transaction() as sess:
        with app.app_context():
            conn = get_db()
            try:
                user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
                sess['user_id'] = user['id']
            finally:
                conn.close()

    response = client.post('/expenses/add', data={
        'amount': '50.0',
        'category': 'Food',
        'date': '2026-03-20',
        'description': ''
    }, follow_redirects=False)

    assert response.status_code == 302
    assert response.location.endswith('/profile')

    with app.app_context():
        conn = get_db()
        try:
            row = conn.execute("SELECT * FROM expenses WHERE amount = 50.0 AND category = 'Food' AND date = '2026-03-20'").fetchone()
            assert row is not None
            assert row['description'] is None
        finally:
            conn.close()
