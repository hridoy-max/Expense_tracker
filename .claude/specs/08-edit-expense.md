Spec: Edit Expense

Overview
Allow users to edit their existing expenses. This is a critical part of the expense management lifecycle, enabling users to correct mistakes or update transaction details without deleting and recreating the entry. This follows the "Add Expense" (Step 07) feature.

Depends on
Step 07: Add Expense

Routes
GET /expenses/<int:id>/edit — Render the edit form with current expense data — logged-in
POST /expenses/<int:id>/edit — Process the updated expense data and save to DB — logged-in

Database changes
New helper function in database/db.py: `update_expense(expense_id, user_id, amount, category, date, description)`. This function must verify that the expense belongs to the user before applying the update to ensure data isolation.

Templates
Create: templates/edit_expense.html
Modify: templates/profile.html (add Edit link to each transaction)

Files to change
- app.py
- database/db.py
- templates/profile.html

Files to create
- templates/edit_expense.html

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html
- Verify ownership: Ensure the expense ID being edited belongs to the session's user_id.

Definition of done
- [ ] User can navigate from the profile page to the edit page for a specific expense.
- [ ] Edit page pre-fills the form with the current expense's amount, category, date, and description.
- [ ] Successfully updating an expense reflects the changes on the profile page.
- [ ] Attempting to edit an expense that does not exist or doesn't belong to the user results in a 404 error.
- [ ] Form validation is applied to the edit form (e.g., positive amount, valid category, valid date).
- [ ] Updating the description to be empty or whitespace is handled as NULL in the database.
