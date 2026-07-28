Spec: Login and Logout

Overview
This feature implements the authentication flow, allowing registered users to securely sign into their accounts and sign out. It leverages Flask sessions and password hashing to maintain state and protect user credentials.

Depends on
- 01 Database Setup
- 02 Registration

Routes
- GET /login — render login page — public
- POST /login — authenticate user and start session — public
- GET /logout — end session and redirect to landing — logged-in

Database changes
No database changes.

Templates
- Modify: templates/login.html — remove legacy {{ error }} block in favor of flashed messages handled by base.html.

Files to change
- app.py
- templates/login.html
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
- [ ] User can successfully log in with correct credentials and be redirected to the profile page (even if the profile page is currently a stub).
- [ ] User sees a flash error message when providing incorrect credentials.
- [ ] User sees a flash error message when providing a non-existent email.
- [ ] User can successfully log out and be redirected to the landing page.
- [ ] Login page renders correctly and follows the project style.
- [ ] Logout route is no longer a stub.
