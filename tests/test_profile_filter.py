import pytest
from datetime import date, timedelta
from app import app as flask_app
from database.db import init_db
from flask import session

@pytest.fixture
def app(tmp_path):
    db_file = tmp_path / "test_spendly.db"
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': str(db_file),
        'SECRET_KEY': 'test-secret',
    })
    with flask_app.app_context():
        init_db()
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    return client

def add_expense(app, user_id, amount, date_str, category="Food"):
    """Helper to insert expenses for testing."""
    from database.db import get_db
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO expenses (user_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, date_str, category, "Test expense")
        )
        db.commit()

class TestProfileDateFilter:

    @pytest.fixture(autouse=True)
    def setup_data(self, app, auth_client):
        """
        Sets up a timeline of expenses.
        """
        from database.db import get_db
        with app.app_context():
            db = get_db()
            user = db.execute("SELECT id FROM users WHERE email = 'test@example.com'").fetchone()
            user_id = user[0]

            today = date.today()

            # Expense 1: Today
            add_expense(app, user_id, 100.0, today.isoformat())
            # Expense 2: 30 days ago
            add_expense(app, user_id, 200.0, (today - timedelta(days=30)).isoformat())
            # Expense 3: 120 days ago (approx 4 months)
            add_expense(app, user_id, 300.0, (today - timedelta(days=120)).isoformat())
            # Expense 4: 210 days ago (approx 7 months)
            add_expense(app, user_id, 400.0, (today - timedelta(days=210)).isoformat())

    def test_profile_default_view_returns_all(self, app, auth_client):
        """Default view (no params) returns all data."""
        response = auth_client.get('/profile')
        assert response.status_code == 200
        # Total: 100+200+300+400 = 1000
        assert b'1,000.00' in response.data or b'1000.00' in response.data
        assert response.data.count(b'Test expense') == 4

    def test_profile_custom_date_range(self, app, auth_client):
        """Custom date range filters data correctly."""
        today = date.today()
        # Range that only includes the 30-day and 120-day expenses
        date_from = (today - timedelta(days=150)).isoformat()
        date_to = (today - timedelta(days=10)).isoformat()

        response = auth_client.get(f'/profile?date_from={date_from}&date_to={date_to}')
        assert response.status_code == 200
        # Should include the 200.0 and 300.0 expenses
        assert b'200.00' in response.data
        assert b'300.00' in response.data
        # Should NOT include Today (100) or 210-day (400)
        assert b'100.00' not in response.data
        assert b'400.00' not in response.data
        # Should NOT include the All-Time total (1000)
        assert b'1,000.00' not in response.data
        assert b'1000.00' not in response.data

    def test_profile_inverted_date_range(self, app, auth_client):
        """Inverted date range triggers flash error and falls back to All Time."""
        today = date.today()
        date_from = today.isoformat()
        date_to = (today - timedelta(days=10)).isoformat()

        response = auth_client.get(f'/profile?date_from={date_from}&date_to={date_to}')
        assert response.status_code == 200
        # Should see all data (fallback)
        assert response.data.count(b'Test expense') == 4
        assert b'Start date must be before end date.' in response.data

    def test_profile_malformed_date_strings(self, app, auth_client):
        """Malformed date strings fall back to All Time."""
        response = auth_client.get('/profile?date_from=not-a-date&date_to=invalid')
        assert response.status_code == 200
        # Should see all data
        assert response.data.count(b'Test expense') == 4

    def test_profile_no_data_in_range(self, app, auth_client):
        """Ranges with no data return empty stats and empty lists."""
        today = date.today()
        # Range in the far future
        date_from = (today + timedelta(days=1000)).isoformat()
        date_to = (today + timedelta(days=1100)).isoformat()

        response = auth_client.get(f'/profile?date_from={date_from}&date_to={date_to}')
        assert response.status_code == 200
        # Stats should be 0.00
        assert b'0.00' in response.data
        # List should be empty
        assert b'Test expense' not in response.data
        assert b'No transactions found' in response.data
