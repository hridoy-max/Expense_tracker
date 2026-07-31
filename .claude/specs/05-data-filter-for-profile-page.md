Spec: Data Filter for Profile Page

Overview
This feature introduces filtering capabilities to the user's profile page, allowing them to view their spending habits over specific time periods and by specific categories. This transforms the profile page from a static summary into a functional analytics dashboard.

Depends on
05-backend-routes-profile-page

Routes
No new routes. The existing `GET /profile` route will be modified to accept the following optional query parameters:
- `start_date`: ISO format date (YYYY-MM-DD)
- `end_date`: ISO format date (YYYY-MM-DD)
- `category`: Category name string

Database changes
No new tables or columns. 
The following functions in `database/db.py` will be updated to support filtering:
- `get_user_stats(user_id, start_date=None, end_date=None, category=None)`
- `get_user_transactions(user_id, start_date=None, end_date=None, category=None, limit=5)`
- `get_category_breakdown(user_id, start_date=None, end_date=None, category=None)`

Templates
Modify: `templates/profile.html`
- Add a filter form at the top of the transactions/stats section.
- Include a dropdown for "Time Range" (e.g., All Time, Last 30 Days, This Month).
- Include a dropdown for "Category" (dynamically populated from existing categories).
- Add a "Clear Filters" button.

Files to change
- `app.py`: Update the `profile` route to extract query parameters and pass them to the DB helper functions.
- `database/db.py`: Modify the three `get_user_*` functions to apply `WHERE` clauses based on the provided filters.

Files to create
- `.claude/specs/05-data-filter-for-profile-page.md`

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
- [ ] The profile page displays a filter form with date range and category options.
- [ ] Selecting a category filters both the "Recent Transactions" list and the "Spending Summary" stats.
- [ ] Selecting a date range filters both the "Recent Transactions" list and the "Spending Summary" stats.
- [ ] Combining date and category filters works correctly (AND logic).
- [ ] The "Clear Filters" button resets the view to "All Time" and "All Categories".
- [ ] The page handles cases with no transactions for a given filter gracefully (shows 0.00 or "No transactions found").
