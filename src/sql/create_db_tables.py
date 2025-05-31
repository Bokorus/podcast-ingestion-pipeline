import logging
import os
from mysql.connector.cursor import MySQLCursor
from pathlib import Path
from typing import cast
from db_config import get_db_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def execute_sql_file(cursor: MySQLCursor, filepath: Path):
    """ 
    Execute the sql from a file given the cursor. 

    Args:
        cursor (MySQLCursor): MySQL connection cursor
        filepath (str): filepath to sql file. 
    """
    with open(filepath, 'r') as f:
        sql = f.read()
    cursor.execute(sql)

def create_tables():
    """
    Create MySQL tables in AWS RDS using sql queries.

    Args:
        None
    """
    logging.info("Getting database connection...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor = cast(MySQLCursor, cursor)

    files2_exec = ["create_episodes_table.sql", "create_transcript_segments_table.sql"]
    base_path = Path(__file__).parent / "queries"
    for sql_file in files2_exec:
        full_path = base_path / sql_file
        logging.info("Executing SQL file: %s", full_path)
        execute_sql_file(cursor, full_path)

    conn.commit()
    logging.info("Closing database connection...")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
