#!/usr/bin/env python3
"""
PostgreSQL Database Access Script
Manages employee records with environment-based configuration
"""

import os
import sys
import psycopg2
from psycopg2 import sql, Error
from typing import Optional

def get_env_variable(var_name: str) -> str:
    """
    Retrieve environment variable or exit if missing.
    
    Args:
        var_name: Name of the environment variable
        
    Returns:
        Value of the environment variable
    """
    value = os.getenv(var_name)
    if value is None:
        print(f"ERROR: Environment variable '{var_name}' is not set.")
        print("Please set all required environment variables:")
        print("  - DB_HOST")
        print("  - DB_PORT")
        print("  - DB_NAME")
        print("  - DB_USER")
        print("  - DB_PASSWORD")
        sys.exit(1)
    return value


def connect_to_database() -> Optional[psycopg2.extensions.connection]:
    """
    Establish connection to PostgreSQL database using environment variables.
    
    Returns:
        Database connection object or None if connection fails
    """
    try:
        # Retrieve connection settings from environment variables
        db_host = get_env_variable('DB_HOST')
        db_port = get_env_variable('DB_PORT')
        db_name = get_env_variable('DB_NAME')
        db_user = get_env_variable('DB_USER')
        db_password = get_env_variable('DB_PASSWORD')
        
        print(f"Connecting to database '{db_name}' on {db_host}:{db_port}...")
        
        # Establish connection
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        print(" Database connection established successfully.\n")
        return connection
        
    except Error as e:
        print(f"ERROR: Failed to connect to database: {e}")
        return None


def create_table(connection: psycopg2.extensions.connection) -> bool:
    """
    Create employees table if it doesn't exist.
    
    Args:
        connection: Active database connection
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Create table with parameterized query (safe from SQL injection)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        );
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        
        print("Table 'employees' is ready.\n")
        return True
        
    except Error as e:
        print(f"ERROR: Failed to create table: {e}")
        return False


def insert_employee(connection: psycopg2.extensions.connection, 
                   name: str, department: str) -> bool:
    """
    Insert a new employee record using parameterized query.
    
    Args:
        connection: Active database connection
        name: Employee name
        department: Employee department
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Parameterized INSERT query (prevents SQL injection)
        insert_query = """
        INSERT INTO employees (name, department)
        VALUES (%s, %s);
        """
        
        cursor.execute(insert_query, (name, department))
        connection.commit()
        cursor.close()
        
        print(f" Employee '{name}' added successfully.\n")
        return True
        
    except Error as e:
        print(f"ERROR: Failed to insert employee: {e}")
        connection.rollback()
        return False


def display_all_employees(connection: psycopg2.extensions.connection) -> None:
    """
    Query and display all employees in a formatted table.
    
    Args:
        connection: Active database connection
    """
    try:
        cursor = connection.cursor()
        
        # Parameterized SELECT query
        select_query = "SELECT id, name, department FROM employees ORDER BY id;"
        cursor.execute(select_query)
        
        rows = cursor.fetchall()
        cursor.close()
        
        if not rows:
            print("No employees found in the database.")
            return
        
        # Calculate column widths for alignment
        id_width = max(len("ID"), max(len(str(row[0])) for row in rows))
        name_width = max(len("Name"), max(len(row[1]) for row in rows))
        dept_width = max(len("Department"), max(len(row[2]) for row in rows))
        
        # Print table header
        print("=" * (id_width + name_width + dept_width + 10))
        print(f"{'ID':<{id_width}} | {'Name':<{name_width}} | {'Department':<{dept_width}}")
        print("=" * (id_width + name_width + dept_width + 10))
        
        # Print table rows
        for row in rows:
            emp_id, name, department = row
            print(f"{emp_id:<{id_width}} | {name:<{name_width}} | {department:<{dept_width}}")
        
        print("=" * (id_width + name_width + dept_width + 10))
        print(f"Total employees: {len(rows)}\n")
        
    except Error as e:
        print(f"ERROR: Failed to retrieve employees: {e}")


def get_user_input() -> tuple[str, str]:
    """
    Prompt user for employee information.
    
    Returns:
        Tuple of (name, department)
    """
    print("Enter new employee details:")
    name = input("Name: ").strip()
    department = input("Department: ").strip()
    
    if not name or not department:
        print("ERROR: Name and Department cannot be empty.")
        sys.exit(1)
    
    print()  # Blank line for readability
    return name, department


def main():
    """
    Main execution function.
    """
    print("=" * 60)
    print("PostgreSQL Employee Database Manager")
    print("=" * 60)
    print()
    
    # Step 1: Connect to database
    connection = connect_to_database()
    if connection is None:# Check if connection was successful
        sys.exit(1) # Exit if connection failed
    
    try:
        # Step 2: Create table if not exists
        if not create_table(connection):
            sys.exit(1) # Exit if table creation failed 
        
        # Step 3: Get user input for new employee
        name, department = get_user_input() 
        
        # Step 4: Insert new employee
        if not insert_employee(connection, name, department): # Check if insertion was successful
            sys.exit(1) # Exit if insertion failed
        
        # Step 5: Display all employees
        print("Current Employee Records:")
        print("-" * 60)
        display_all_employees(connection)
        
    finally:
        # Clean exit: close database connection
        if connection:# Check if connection exists
            connection.close()
            print(" Database connection closed.")


if __name__ == "__main__":
    main()