import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Database credentials
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Log file path
LOG_FILE = "logs/ai_behavior.log"

def log_to_file(message):
    """Append a message with timestamp to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        return conn
    except Exception as e:
        log_to_file(f"Database connection failed: {e}")
        return None


def setup_database():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ai_data (
                        id SERIAL PRIMARY KEY,
                        input_data TEXT,
                        output_data TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                conn.commit()
                log_to_file("Table 'ai_data' is ready.")
        except Exception as e:
            log_to_file(f"Error creating table: {e}")
        finally:
            conn.close()


def insert_data(input_data, output_data):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO ai_data (input_data, output_data)
                    VALUES (%s, %s);
                ''', (input_data, output_data))
                conn.commit()
                log_to_file(f"Inserted into DB | Input: {input_data} | Output: {output_data}")
        except Exception as e:
            log_to_file(f"Insert failed: {e}")
        finally:
            conn.close()
