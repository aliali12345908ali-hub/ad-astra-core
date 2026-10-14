import sqlite3
import os

DB_PATH = os.path.join("evidence", "ad_astra.db")

def init_db():
    os.makedirs("evidence", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # جدول الفواتير والمعاملات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id TEXT PRIMARY KEY,
            issue_date TEXT,
            client TEXT,
            amount REAL,
            currency TEXT,
            status TEXT
        )
    ''')
    
    # جدول التدقيق الأمني
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            details TEXT,
            current_hash TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("[*] SQLite database initialized successfully for Abdallah Ben Belgacem.")
