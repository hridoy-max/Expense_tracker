Spec: Profile Page Design

Overview
The Profile Page serves as the primary dashboard for authenticated users. It provides a personalized welcome, displays account details (name and email), and shows a high-level summary of the user's spending. This step transitions the application from a simple landing page to a user-centric experience.

Depends on
Step 02: Registration
Step 03: Login and Logout

Routes
GET /profile — Display user profile and expense summary — logged-in

Database changes
No new tables. A new helper function `get_user_profile_data(user_id)` will be added to `database/db.py` to fetch the user's name, email, and the sum of their expenses.

Templates
Create: templates/profile.html
Modify: templates/base.html (Update navigation to show Profile and Logout links when authenticated, and Sign in/Register when not)

Files to change
- app.py: Implement the /profile route to fetch data and render the profile template.
- database/db.py: Add function to retrieve user profile and expense totals.

Files to create
- templates/profile.html: The profile dashboard layout.
- static/css/profile.css: Styles for the profile page components.

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
- [ ] Authenticated users can access /profile.
- [ ] The profile page correctly displays the user's name and email from the database.
- [ ] The profile page displays the correct total amount of all expenses associated with the user.
- [ ] The navigation bar in base.html dynamically updates based on the user's session status.
- [ ] Unauthenticated users attempting to access /profile are redirected to the login page with a flash message.
- [ ] The page layout is responsive and follows the Spendly visual style.
