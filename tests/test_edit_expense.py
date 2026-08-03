import pytest
import sqlite3
from app import app as flask_app
from database.db import init_db, insert_expense, get_expense_by_id

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': 'test_spendly.db',
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        init_db()
        yield flask_app

    # Teardown: remove the test database file
    import os
    if os.path.exists('test_spendly.db'):
        os.remove('test_spendly.db')


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'testpass', 'confirm_password': 'testpass'})
    client.post('/login', data={'email': 'test@example.com', 'password': 'testpass'})
    return client

class TestEditExpense:

    def test_edit_expense_unauthenticated_redirect(self, client):
        """Unauthenticated users should be redirected to login."""
        response = client.get('/expenses/1/edit')
        assert response.status_code == 302
        assert '/login' in response.location

        response = client.post('/expenses/1/edit', data={'amount': '10.0'})
        assert response.status_code == 302
        assert '/login' in response.location

    def test_edit_expense_not_found_or_forbidden(self, auth_client, app):
        """Editing non-existent or other user's expense should return 404."""
        # 1. Non-existent expense
        response = auth_client.get('/expenses/999/edit')
        assert response.status_code == 404

        # 2. Other user's expense
        with app.app_context():
            # Create a second user
            from database.db import create_user
            user2_id = create_user("Other User", "other@example.com", "pass123")
            # Create an expense for user 2
            insert_expense(user2_id, 50.0, "Food", "2026-01-01", "Other user expense")
            expense_id = 1 # First expense created in this clean DB

        response = auth_client.get(f'/expenses/{expense_id}/edit')
        assert response.status_code == 404

    def test_edit_expense_get_success(self, auth_client, app):
        """Authenticated user can view the edit page for their own expense."""
        with app.app_context():
            user_id = 1 # The auth_client user
            expense_id = insert_expense(user_id, 25.55, "Food", "2026-08-01", "Original Description")

        response = auth_client.get(f'/expenses/{expense_id}/edit')
        assert response.status_code == 200
        assert b"Original Description" in response.data
        assert b"25.55" in response.data
        assert b"Food" in response.data
        assert b"2026-08-01" in response.data

    def test_edit_expense_post_success(self, auth_client, app):
        """Valid update should redirect to profile and update DB."""
        with app.app_context():
            user_id = 1
            expense_id = insert_expense(user_id, 10.0, "Food", "2026-08-01", "Old Desc")

        new_data = {
            'amount': '15.75',
            'category': 'Transport',
            'date': '2026-08-02',
            'description': 'Updated Description'
        }
        response = auth_client.post(f'/expenses/{expense_id}/edit', data=new_data)

        assert response.status_code == 302
        assert '/profile' in response.location

        # Verify DB update
        with app.app_context():
            expense = get_expense_by_id(expense_id)
            assert expense['amount'] == 15.75
            assert expense['category'] == 'Transport'
            assert expense['date'] == '2026-08-02'
            assert expense['description'] == 'Updated Description'

    @pytest.mark.parametrize("field, value, expected_error", [
        ("amount", "-10.0", "Amount must be a positive number."),
        ("amount", "abc", "Please enter a valid numeric amount."),
        ("category", "InvalidCat", "Please select a valid category."),
        ("date", "01-01-2026", "Invalid date format."),
        ("date", "", "Please select a date."),
    ])
    def test_edit_expense_validation_errors(self, auth_client, app, field, value, expected_error):
        """Invalid inputs should trigger validation errors."""
        with app.app_context():
            user_id = 1
            expense_id = insert_expense(user_id, 10.0, "Food", "2026-08-01", "Desc")

        # Valid default data
        data = {
            'amount': '10.0',
            'category': 'Food',
            'date': '2026-08-01',
            'description': 'Desc'
        }
        data[field] = value

        response = auth_client.post(f'/expenses/{expense_id}/edit', data=data)

        assert response.status_code == 200
        assert expected_error.encode() in response.data

    def test_edit_expense_description_null_handling(self, auth_client, app):
        """Empty or whitespace descriptions should be stored as NULL."""
        with app.app_context():
            user_id = 1
            expense_id = insert_expense(user_id, 10.0, "Food", "2026-08-01", "Initial")

        # Test empty string
        auth_client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '10.0', 'category': 'Food', 'date': '2026-08-01', 'description': ''
        })
        with app.app_context():
            assert get_expense_by_id(expense_id)['description'] is None

        # Test whitespace
        auth_client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '10.0', 'category': 'Food', 'date': '2026-08-01', 'description': '   '
        })
        with app.app_context():
            assert get_expense_by_id(expense_id)['description'] is None
