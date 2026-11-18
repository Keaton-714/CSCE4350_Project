## Installation and Setup
Follow these steps after cloning or pulling the latest version of the repository.

### 1. Install Dependencies

From the project's root directory, run:

```bash
pip install -r requirements.txt
```
This installs the Python packages required to run the application. You only need to do this during initial setup or when dependencies change.

### 2. Initialize the Database

Run the following command to create the SQLite database and populate it with sample data:
```bash
python -m backend.database.init_db
```
This creates autoone.db in the backend/database/ directory.

**Note:** Existing databases will not be reset by this command.

### 3. Create an Employee Account

After initializing the database, run:
```bash
python -m backend.database.create_employee
```
Follow the prompts to create an employee account. When prompted for a Store ID, enter 1 to use the default store.

### 4. Run the Application

Start the Flask application using:
```bash
python -m backend.app
```
Open the URL displayed in your terminal (typically http://127.0.0.1:5000) in your browser.

### 5. Log In or Register

- **Employee:** Log in using your employee credentials.
- **Customer:** Register a new customer account.

Once authenticated, you will be redirected to the appropriate dashboard based on your account type.