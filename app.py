from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, get_user_stats, get_user_transactions, get_category_breakdown
import sqlite3
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime, timedelta

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


def get_date_filter_params(request_args):
    """
    Validates date filters and calculates presets.
    Returns (date_from, date_to, presets)
    """
    date_from = request_args.get('date_from')
    date_to = request_args.get('date_to')

    def is_valid_date(date_str):
        if not date_str:
            return False
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    if date_from and not is_valid_date(date_from):
        date_from = None
    if date_to and not is_valid_date(date_to):
        date_to = None

    if date_from and date_to and date_from > date_to:
        flash("Start date must be before end date.", "error")
        date_from = None
        date_to = None

    today = datetime.now().date()
    presets = {
        "this_month": {
            "from": today.replace(day=1).strftime('%Y-%m-%d'),
            "to": today.strftime('%Y-%m-%d')
        },
        "last_3_months": {
            "from": (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            "to": today.strftime('%Y-%m-%d')
        },
        "last_6_months": {
            "from": (today - timedelta(days=180)).strftime('%Y-%m-%d'),
            "to": today.strftime('%Y-%m-%d')
        },
        "all_time": {
            "from": None,
            "to": None
        }
    }
    return date_from, date_to, presets

@app.route("/profile")
@login_required
def profile():
    user_id = session.get('user_id')

    # Get validated filters and presets
    date_from, date_to, presets = get_date_filter_params(request.args)

    # Fetch real data from database with filters
    user = get_user_by_id(user_id)
    stats = get_user_stats(user_id, date_from, date_to)
    transactions = get_user_transactions(user_id, date_from=date_from, date_to=date_to)
    categories = get_category_breakdown(user_id, date_from, date_to)

    if not user:
        abort(404)


    # Format data for template
    # Format member_since from created_at (ISO format) to "Month Year"
    try:
        dt = datetime.strptime(user['created_at'], '%Y-%m-%d %H:%M:%S')
        member_since = dt.strftime('%B %Y')
    except (ValueError, TypeError):
        member_since = "Unknown"

    user_data = {
        "name": user['name'],
        "email": user['email'],
        "member_since": member_since
    }

    summary_stats = {
        "total_spent": f"{stats['total_spent']:,.2f}",
        "transaction_count": stats['transaction_count'],
        "top_category": stats['top_category'] or "N/A"
    }

    return render_template(
        "profile.html",
        user=user_data,
        stats=summary_stats,
        transactions=transactions,
        categories=categories,
        presets=presets,
        active_filter={"from": date_from, "to": date_to}
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
