import os
from pathlib import Path
from db_config import get_db_connection

def execute_sql_file(cursor, filepath):
    with open(filepath, 'r') as f:
        sql = f.read()
    cursor.execute(sql)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    base_path = Path(__file__).parent / "sql" / "queries"
    execute_sql_file(cursor, base_path / "create_episodes_table.sql")
    execute_sql_file(cursor, base_path / "create_transcript_segments_table.sql")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
