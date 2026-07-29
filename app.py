from flask import Flask, render_template, request, flash, redirect, url_for, session
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email
import sqlite3
from werkzeug.security import check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'dev-secret-key-for-spendly'

def login_required(f):
    """
    Decorator to restrict route access to authenticated users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def guest_only(f):
    """
    Decorator to restrict route access to non-authenticated users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('profile'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------------------------------------------------------ #

# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return render_template("landing.html")


@app.route("/register", methods=['GET', 'POST'])
@guest_only
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation: Non-empty fields
        if not all([name, email, password, confirm_password]):
            flash("All fields are required", "error")
            return render_template("register.html")

        # Validation: Passwords match
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered", "error")
            return render_template("register.html")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "error")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
@guest_only
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash("Welcome back!", "success")
            return redirect(url_for('profile'))

        flash("Invalid email or password", "error")
        return render_template("login.html")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out", "success")
    return redirect(url_for('landing'))


@app.route("/profile")
@login_required
def profile():
    # Mock data for design validation (Step 04)
    user_data = {
        "name": "Naimur Rahman",
        "email": "naimur@example.com",
        "member_since": "July 2026"
    }

    summary_stats = {
        "total_spent": "1,240.50",
        "transaction_count": 42,
        "top_category": "Food & Dining"
    }

    transactions = [
        {"date": "2026-07-28", "description": "Grocery Store", "category": "Food", "amount": "65.20"},
        {"date": "2026-07-27", "description": "Netflix Subscription", "category": "Entertainment", "amount": "15.99"},
        {"date": "2026-07-25", "description": "Gas Station", "category": "Transport", "amount": "45.00"},
        {"date": "2026-07-24", "description": "Pharmacy", "category": "Health", "amount": "12.40"},
        {"date": "2026-07-22", "description": "Restaurant", "category": "Food", "amount": "32.00"},
    ]

    category_breakdown = [
        {"category": "Food", "amount": "450.00", "percentage": 36},
        {"category": "Transport", "amount": "300.00", "percentage": 24},
        {"category": "Entertainment", "amount": "200.00", "percentage": 16},
        {"category": "Health", "amount": "150.00", "percentage": 12},
        {"category": "Other", "amount": "140.50", "percentage": 12},
    ]

    return render_template(
        "profile.html",
        user=user_data,
        stats=summary_stats,
        transactions=transactions,
        categories=category_breakdown
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
