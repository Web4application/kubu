import psycopg2
from dotenv import load_dotenv
import os
from contextlib import closing

# Load environment variables from .env
load_dotenv()

# Database credentials from environment variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
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
        print(f"Database connection failed: {e}")
        return None


def setup_database():
    """Creates the ai_data table if it doesn't already exist."""
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
                print("Table 'ai_data' created or already exists.")
        except Exception as e:
            print(f"Error during table creation: {e}")
        finally:
            conn.close()


def insert_data(input_data, output_data):
    """Inserts a new record into the ai_data table."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO ai_data (input_data, output_data)
                    VALUES (%s, %s);
                ''', (input_data, output_data))
                conn.commit()
                print("Data inserted.")
        except Exception as e:
            print(f"Insert failed: {e}")
        finally:
            conn.close()


def get_all_data():
    """Fetches all records from the ai_data table."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ai_data;")
                return cursor.fetchall()
        except Exception as e:
            print(f"Select failed: {e}")
            return []
        finally:
            conn.close()


# Example usage
if __name__ == "__main__":
    setup_database()
    insert_data("Example input", "Example output")
    data = get_all_data()
    print("All data from DB:", data)
