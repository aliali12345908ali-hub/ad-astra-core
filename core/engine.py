import sqlite3
import uuid

DB_PATH = "evidence/ad_astra_local.db"

def create_project(name, hard_limit):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    project_id = str(uuid.uuid4())
    try:
        cursor.execute("INSERT INTO projects (project_id, name) VALUES (?, ?);", (project_id, name))
        cursor.execute("INSERT INTO budgets (project_id, hard_limit) VALUES (?, ?);", (project_id, hard_limit))
        conn.commit()
        print(f"[*] Project Created: {name} (ID: {project_id}) with Limit: {hard_limit} EUR")
        return project_id
    except Exception as e:
        conn.rollback()
        print(f"[-] Error creating project: {e}")
        return None
    finally:
        conn.close()

def create_task(project_id, task_type, idempotency_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    task_id = str(uuid.uuid4())
    try:
        cursor.execute(
            "INSERT INTO tasks (task_id, project_id, task_type, idempotency_key) VALUES (?, ?, ?, ?);",
            (task_id, project_id, task_type, idempotency_key)
        )
        conn.commit()
        print(f"[*] Task Queued: {task_id} (Idempotency Key: {idempotency_key})")
        return task_id
    except sqlite3.IntegrityError:
        print("[-] Idempotency Violation: Task with this key already exists for this project.")
        return None
    finally:
        conn.close()
