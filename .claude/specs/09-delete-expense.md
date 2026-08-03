Spec: Delete Expense

Overview
This feature allows authenticated users to permanently remove an expense record from their history. It provides a confirmation step to prevent accidental deletions and ensures users can only delete expenses that belong to their own account.

Depends on
- 08-edit-expense

Routes
- GET /expenses/<int:id>/delete — Renders a confirmation page before deletion — logged-in
- POST /expenses/<int:id>/delete — Deletes the specified expense and redirects to profile — logged-in

Database changes
- Create a new helper function `delete_expense(expense_id, user_id)` in `database/db.py` that executes `DELETE FROM expenses WHERE id = ? AND user_id = ?`.

Templates
Create:
- templates/delete_expense.html — A simple confirmation page that shows the expense details and asks the user if they are sure they want to delete it.

Files to change
- app.py — Implement the delete_expense route with GET and POST methods.
- database/db.py — Add the delete_expense helper function.

Files to create
- templates/delete_expense.html

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- All templates extend base.html
- Use CSS variables — never hardcode hex values
- Verify expense ownership before deletion (must match session user_id)
- Use abort(404) if the expense does not exist or doesn't belong to the user.

Definition of done
- [ ] Navigating to /expenses/<id>/delete for a valid expense owned by the user shows a confirmation page.
- [ ] Navigating to /expenses/<id>/delete for an expense owned by another user (or non-existent) returns a 404 error.
- [ ] Clicking the "Delete" button on the confirmation page removes the expense from the database.
- [ ] After deletion, the user is redirected back to the profile page with a success flash message.
- [ ] Deletion is handled via a POST request to prevent accidental deletions via links/crawlers.
