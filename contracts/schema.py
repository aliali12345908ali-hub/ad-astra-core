import sqlite3
import os

DB_PATH = "evidence/ad_astra_local.db"

def init_db():
    os.makedirs("evidence", exist_ok=True)
    os.makedirs("contracts", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # تفعيل القيود المفتاحية الأجنبية في SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. جدول المشاريع وعزل النطاق
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. جدول الميزانيات (EUR) مع قيد عدم تجاوز الحد
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        project_id TEXT PRIMARY KEY,
        currency TEXT NOT NULL DEFAULT 'EUR',
        hard_limit REAL NOT NULL DEFAULT 0.0,
        current_spent REAL NOT NULL DEFAULT 0.0,
        reserved_amount REAL NOT NULL DEFAULT 0.0,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE RESTRICT,
        CONSTRAINT check_budget_limit CHECK ((current_spent + reserved_amount) <= hard_limit)
    );
    """)
    
    # 3. جدول المهام مع مفتاح منع التكرار (Idempotency Key)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'QUEUED',
        idempotency_key TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE RESTRICT,
        CONSTRAINT uq_project_idempotency UNIQUE (project_id, idempotency_key)
    );
    """)
    
    # 4. جدول حيازة العمال ورموز Fencing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS worker_leases (
        task_id TEXT PRIMARY KEY,
        worker_id TEXT NOT NULL,
        fence_token INTEGER NOT NULL DEFAULT 1,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE RESTRICT
    );
    """)
    
    conn.commit()
    conn.close()
    print("[+] Local Schema Initialized Successfully in SQLite.")

if __name__ == "__main__":
    init_db()

