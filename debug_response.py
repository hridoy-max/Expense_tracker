import pytest
from app import app as flask_app
from database.db import init_db
from datetime import date, timedelta
import sqlite3

# Mocking the app and db
flask_app.config.update({
    'TESTING': True,
    'DATABASE': 'debug.db',
    'SECRET_KEY': 'test-secret',
})

with flask_app.app_context():
    init_db()
    # Create user
    from database.db import create_user, get_db
    user_id = create_user('Test User', 'test@example.com', 'testpass')
    
    db = get_db()
    today = date.today().isoformat()
    # 100.0 Today
    db.execute("INSERT INTO expenses (user_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)", (user_id, 100.0, today, 'Food', 'Test expense'))
    # 200.0 30 days ago
    db.execute("INSERT INTO expenses (user_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)", (user_id, 200.0, (date.today() - timedelta(days=30)).isoformat(), 'Food', 'Test expense'))
    # 300.0 120 days ago
    db.execute("INSERT INTO expenses (user_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)", (user_id, 300.0, (date.today() - timedelta(days=120)).isoformat(), 'Food', 'Test expense'))
    # 400.0 210 days ago
    db.execute("INSERT INTO expenses (user_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)", (user_id, 400.0, (date.today() - timedelta(days=210)).isoformat(), 'Food', 'Test expense'))
    db.commit()

client = flask_app.test_client()
with client.session_transaction() as sess:
    sess['user_id'] = user_id

today = date.today()
date_from = (today - timedelta(days=150)).isoformat()
date_to = (today - timedelta(days=10)).isoformat()

response = client.get(f'/profile?date_from={date_from}&date_to={date_to}')
html = response.data.decode()

if '100' in html:
    print("FOUND 100!")
    # Print 50 chars before and after
    idx = html.find('100')
    print(html[max(0, idx-50):min(len(html), idx+50)])
else:
    print("NOT FOUND 100")
