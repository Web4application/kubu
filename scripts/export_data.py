import pandas as pd
from db_engine import get_connection, DB_TYPE

def export_to_csv(filepath="data/ai_data_export.csv"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ai_data")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filepath, index=False)
    print(f"Exported data to {filepath}")
    conn.close()

if __name__ == "__main__":
    export_to_csv()
