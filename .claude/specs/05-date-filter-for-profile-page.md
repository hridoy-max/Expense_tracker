Spec: Date Filter for Profile Page

Overview
This feature introduces date-based filtering capabilities to the user's profile page, allowing them to view their spending habits over specific time periods. This transforms the profile page from a static summary into a functional analytics dashboard focused on temporal trends.

Depends on
05-backend-routes-profile-page

Routes
No new routes. The existing `GET /profile` route will be modified to accept the following optional query parameters:
- `start_date`: ISO format date (YYYY-MM-DD)
- `end_date`: ISO format date (YYYY-MM-DD)

Database changes
No new tables or columns. 
The following functions in `database/db.py` will be updated to support date filtering:
- `get_user_stats(user_id, start_date=None, end_date=None)`
- `get_user_transactions(user_id, start_date=None, end_date=None, limit=5)`
- `get_category_breakdown(user_id, start_date=None, end_date=None)`

Templates
Modify: `templates/profile.html`
- Add a date filter form at the top of the transactions/stats section.
- Include a dropdown or input for "Time Range" (e.g., All Time, Last 30 Days, Custom Range).
- Add a "Clear Filters" button.

Files to change
- `app.py`: Update the `profile` route to extract `start_date` and `end_date` query parameters and pass them to the DB helper functions.
- `database/db.py`: Modify the three `get_user_*` functions to apply `WHERE date BETWEEN ? AND ?` clauses based on the provided filters.

Files to create
- `.claude/specs/05-date-filter-for-profile-page.md`

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
- [ ] The profile page displays a date filter form with a range selection.
- [ ] Selecting a date range filters both the "Recent Transactions" list and the "Spending Summary" stats.
- [ ] The "Clear Filters" button resets the view to "All Time".
- [ ] The page handles cases with no transactions for a given date range gracefully (shows 0.00 or "No transactions found").
