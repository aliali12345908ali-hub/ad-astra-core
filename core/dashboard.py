import sqlite3

DB_PATH = "evidence/ad_astra_local.db"

def show_dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("==================================================")
    print("      AD ASTRA CORE: LOCAL CLI DASHBOARD          ")
    print("==================================================")
    
    try:
        print("\n[+] Projects & Budgets Status:")
        cursor.execute("SELECT p.project_id, p.name, b.hard_limit, b.current_spent, b.reserved_amount FROM projects p JOIN budgets b ON p.project_id = b.project_id;")
        rows = cursor.fetchall()
        if not rows:
            print("    (No projects found)")
        for row in rows:
            print(f"    - ID: {row[0][:8]}... | Name: {row[1]}")
            print(f"      Limit: {row[2]} EUR | Spent: {row[3]} EUR | Reserved: {row[4]} EUR")
            
        print("\n[+] Tasks Status:")
        cursor.execute("SELECT task_id, project_id, task_type, status, idempotency_key FROM tasks;")
        tasks = cursor.fetchall()
        if not tasks:
            print("    (No tasks found)")
        for t in tasks:
            print(f"    - Task: {t[0][:8]}... | Type: {t[2]} | Status: {t[3]} | Key: {t[4]}")
            
    except Exception as e:
        print(f"[-] Dashboard Error: {e}")
    finally:
        conn.close()
    print("==================================================")

if __name__ == "__main__":
    show_dashboard()
