Spec: Add Expense

Overview
This feature allows authenticated users to record new expenses. It involves creating a form where users can input the amount, category, date, and an optional description. Once submitted, the expense is saved to the database and linked to the current user.

Depends on
Which previous steps this feature requires to be complete:
- 01 User Registration
- 02 User Login
- 03 User Logout
- 04 User Profile
- 05 Database Setup

Routes
- GET /expenses/add — Renders the "Add Expense" form — logged-in
- POST /expenses/add — Processes the form submission and adds expense to DB — logged-in

Database changes
No new tables or columns needed. The `expenses` table already exists with the required columns: `user_id`, `amount`, `category`, `date`, `description`.
A new helper function `add_expense(user_id, amount, category, date, description)` will be added to `database/db.py`.

Templates
Create:
- templates/add_expense.html

Modify:
- None

Files to change
- app.py
- database/db.py

Files to create
- templates/add_expense.html
- static/css/add_expense.css

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html
- Use url_for() for all internal links
- DB logic must be in database/db.py
- Use abort(400) or flash() for validation errors

Definition of done
- [ ] GET /expenses/add renders a form with fields: Amount (number), Category (dropdown/text), Date (date picker), and Description (text).
- [ ] POST /expenses/add successfully saves a valid expense to the `expenses` table linked to the session user.
- [ ] Validates that Amount, Category, and Date are provided; flashes error if missing.
- [ ] Amount is validated as a positive number.
- [ ] After successful submission, user is redirected to the profile page with a success message.
- [ ] Non-authenticated users are redirected to the login page when trying to access /expenses/add.
- [ ] The new expense appears in the transactions list on the profile page.
