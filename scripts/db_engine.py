import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Logging
LOG_FILE = "logs/ai_behavior.log"
def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# Determine database type
DB_TYPE = os.getenv("db_type", "sqlite")  # sqlite or postgres

def get_connection():
    if DB_TYPE == "postgres":
        return psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname")
        )
    else:
        os.makedirs("data", exist_ok=True)
        return sqlite3.connect("data/my_database.db")

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    create_stmt = '''
        CREATE TABLE IF NOT EXISTS ai_data (
            id SERIAL PRIMARY KEY,
            input_data TEXT,
            output_data TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''' if DB_TYPE == "postgres" else '''
        CREATE TABLE IF NOT EXISTS ai_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT,
            output_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    '''
    cursor.execute(create_stmt)
    conn.commit()
    conn.close()
    log_to_file(f"Database setup completed using {DB_TYPE}.")

def insert_data(input_data, output_data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        insert_stmt = '''
            INSERT INTO ai_data (input_data, output_data)
            VALUES (%s, %s);
        ''' if DB_TYPE == "postgres" else '''
            INSERT INTO ai_data (input_data, output_data)
            VALUES (?, ?);
        '''
        cursor.execute(insert_stmt, (input_data, output_data))
        conn.commit()
        log_to_file(f"Inserted | {input_data} | {output_data}")
    except Exception as e:
        log_to_file(f"Error inserting data: {e}")
    finally:
        conn.close()
