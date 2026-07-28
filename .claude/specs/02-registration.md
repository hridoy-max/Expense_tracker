Spec: Registration

Overview
This feature allows new users to create an account by providing their name, email, and password. It ensures that users are uniquely identified by their email and that passwords are securely hashed before being stored in the database. This is a foundational step for Spendly, enabling user-specific expense tracking.

Depends on
01-database-setup

Routes
POST /register — Handles user registration by validating input and creating a new user record — public

Database changes
No database changes.

Templates
Modify: templates/register.html — Update form to use method="POST" and correct input names (name, email, password).

Files to change
- app.py
- templates/register.html
- database/db.py

Files to create
No new files.

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
- [ ] User can successfully register a new account via the /register page.
- [ ] Registered user is added to the users table in spendly.db with a hashed password.
- [ ] Registration fails if the email is already taken (handled gracefully via flash message or error page).
- [ ] Form validation ensures all required fields (name, email, password) are provided.
- [ ] After successful registration, user is redirected to the login page with a success message.
