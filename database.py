import sqlite3

# Step 1: Setup database
def setup_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    return conn, cursor

# Step 2: Create tables
def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_data TEXT,
        output_data TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

# Step 3: Insert data
def insert_data(cursor, conn, input_data, output_data):
    cursor.execute('''
    INSERT INTO ai_data (input_data, output_data)
    VALUES (?, ?)
    ''', (input_data, output_data))
    conn.commit()

# Step 4: Retrieve data
def get_all_data(cursor):
    cursor.execute('SELECT * FROM ai_data')
    rows = cursor.fetchall()
    return rows

# Main function to execute the script
def main():
    conn, cursor = setup_database()
    create_tables(cursor)
    insert_data(cursor, conn, 'Sample input', 'Sample output')
    data = get_all_data(cursor)
    for row in data:
        print(row)
    conn.close()

if __name__ == "__main__":
    main()
