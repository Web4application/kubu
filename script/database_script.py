import sqlite3

# Step 1: Setup database
def setup_database(db_name='my_database.db'):
    """Set up the SQLite database and return the connection and cursor."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error setting up database: {e}")
        return None, None

# Step 2: Create tables
def create_tables(cursor):
    """Create tables in the database if they do not exist."""
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT,
            output_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# Step 3: Insert data
def insert_data(cursor, conn, input_data, output_data):
    """Insert a row of data into the ai_data table."""
    try:
        cursor.execute('''
        INSERT INTO ai_data (input_data, output_data)
        VALUES (?, ?)
        ''', (input_data, output_data))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

# Step 4: Retrieve data
def get_all_data(cursor):
    """Retrieve all rows of data from the ai_data table."""
    try:
        cursor.execute('SELECT * FROM ai_data')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error retrieving data: {e}")
        return []

# Main function to execute the script
def main():
    conn, cursor = setup_database()
    if conn and cursor:
        create_tables(cursor)
        insert_data(cursor, conn, 'Sample input', 'Sample output')
        data = get_all_data(cursor)
        for row in data:
            print(row)
        conn.close()
    else:
        print("Failed to set up the database connection and cursor.")

if __name__ == "__main__":
    main()
