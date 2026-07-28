### Task: Create a Single Dummy User in the Database

#### Description
Write and execute a Python script to insert a single realistic Bangladeshi user into the database.

#### Allowed Tools
- Read
- Bash (`python3:*`)

#### Instructions
1. **Analyze Schema:**
   - Read `database/db.py` to understand the `users` table schema and the `get_db()` helper function.

2. **Generate User Data:**
   - **Name:** A realistic Bangladeshi full name (first name + last name) using common Bangladeshi names across different regions (e.g., Tanvir Ahmed, Nusrat Jahan, Shakib Hasan, Rakibul Islam).
   - **Email:** Derived from the name with a random 2-3 digit suffix (e.g., `tanvir.ahmed91@gmail.com`).
   - **Password:** `"password123"` hashed using Werkzeug's `generate_password_hash`.
   - **created_at:** Current datetime.

3. **Database Operations:**
   - Check if the generated email already exists in the `users` table. If it exists, regenerate the data until a unique email is found.
   - Insert the user using the `get_db()` connection pattern defined in `database/db.py`.

4. **Output Confirmation:**
   - Print the details of the newly created user:
     - `id`
     - `name`
     - `email`