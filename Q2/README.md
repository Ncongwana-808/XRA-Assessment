# db_access.py

PostgreSQL helper script for simple employee record management.

This script connects to a PostgreSQL database (using environment variables for configuration), ensures an `employees` table exists, prompts the user to add a new employee (name and department), inserts that record, then prints a formatted list of all employees before closing the connection.

## What it does

- Reads database connection settings from environment variables.
- Connects to PostgreSQL using `psycopg2`.
- Creates the `employees` table if it doesn't exist.
- Prompts the user for `Name` and `Department` and inserts a new employee.
- Displays all employees in a formatted table.

## Requirements

- Python 3.7+ (script uses modern typing; works with common 3.x versions)
- `psycopg2` (the project provides a `requirements.txt` in this folder)

Install dependencies (from the `Q2` folder):

```powershell
pip install -r requirements.txt
```

If you prefer, use `psycopg2-binary` in development environments.

## Configuration (environment variables)

Set the following environment variables before running the script. Example PowerShell commands:

```cmd

set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=mydatabase
set DB_USER=myuser
set DB_PASSWORD=mypassword

```

Notes:
- If any of the above variables are missing, the script will exit and print an error message listing the required variables.
- For production usage, avoid setting sensitive values in shell history; prefer a secure store or an environment file that your deployment tooling loads.

## How to run

From the `Q2` directory:


python db_access.py
```

The script will:

1. Connect to the database.
2. Create `employees` table if missing.
3. Prompt for `Name` and `Department`.
4. Insert the record and then display all employees.


## Security and safety notes

- Uses parameterized queries (`%s` placeholders) to avoid SQL injection when inserting data.
- Do not commit secrets (passwords) into version control. Use environment variables or secret management services for production.
