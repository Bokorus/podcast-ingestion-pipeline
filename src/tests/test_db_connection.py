from src.sql.db_config import get_db_connection

def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print(f"[✓] Database connection succeeded. Result: {result}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[✗] Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection()