Spec: Backend Routes for Profile Page

Overview
This feature replaces the mock data in the `/profile` route with actual data fetched from the database for the currently logged-in user. It involves implementing database helper functions to retrieve user profile details, calculate spending statistics, and fetch transaction history and category breakdowns, ensuring the profile page reflects the user's real financial data.

Depends on
Step 04 — Profile Page Design (and preceding steps 01-03 for Auth)

Routes
GET /profile — Fetches real user data, stats, and transactions from DB and renders profile.html — logged-in

Database changes
No new tables or columns. New helper functions will be added to `database/db.py` to:
- `get_user_by_id(user_id)`: Retrieve basic profile info.
- `get_user_stats(user_id)`: Calculate total spent, transaction count, and identify the top category.
- `get_user_transactions(user_id, limit=5)`: Fetch the most recent transactions.
- `get_category_breakdown(user_id)`: Aggregate spending per category with percentages.

Templates
Modify: `templates/profile.html` — Update to handle real data passed from the route (ensure no breaks in the existing design).

Files to change
- `app.py`
- `database/db.py`

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
- [ ] Log in with a registered user and verify the `/profile` page loads without errors.
- [ ] Verify that the displayed name and email match the logged-in user's account.
- [ ] Verify that "Total Spent" correctly sums all expenses for the logged-in user.
- [ ] Verify that "Transaction Count" matches the number of expenses in the DB for that user.
- [ ] Verify that "Top Category" correctly identifies the category with the highest total spend.
- [ ] Verify that the "Recent Transactions" table displays the latest 5 transactions for the user.
- [ ] Verify that the "Category Breakdown" reflects the actual distribution of the user's expenses.
- [ ] Verify that a user with zero expenses displays $0.00 and "No transactions found" gracefully.
