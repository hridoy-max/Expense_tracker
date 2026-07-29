Spec: Profile Page Design

Overview
The Profile Page serves as the central dashboard for authenticated users. It should display the user's basic information (name and email) and a high-level overview of their spending. This step transforms the application from a simple authentication system into a functional user-centric expense tracker.

Depends on
Step 03 - Login and Logout

Routes
GET /profile — Renders the user profile page — logged-in

Database changes
No database changes. Existing `users` and `expenses` tables will be used. New helper functions will be added to `database/db.py` to retrieve user data and total expense sums.

Templates
Create: templates/profile.html
Modify: templates/base.html (Update navigation to include a link to the Profile page for authenticated users)

Files to change
- app.py: Update /profile route to fetch user data and render profile.html.
- database/db.py: Implement helper functions for fetching user profile and expense totals.

Files to create
- templates/profile.html
- static/css/profile.css

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
- [ ] Accessing /profile while logged in renders a page showing the user's name and email.
- [ ] Accessing /profile while logged out redirects to /login with a flash message.
- [ ] The page displays the correct total sum of all expenses for the logged-in user.
- [ ] The page layout is styled using a dedicated profile.css file utilizing CSS variables.
- [ ] The navigation bar in base.html correctly displays a "Profile" link when the user is authenticated.
