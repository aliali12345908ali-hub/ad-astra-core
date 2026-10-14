import sqlite3
import datetime
import time

DB_PATH = "evidence/ad_astra_local.db"

def send_heartbeat(task_id, worker_id, lease_extension_seconds=30):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.utcnow()
    new_expiry = now + datetime.timedelta(seconds=lease_extension_seconds)
    
    try:
        cursor.execute("""
            UPDATE worker_leases 
            SET expires_at = ? 
            WHERE task_id = ? AND worker_id = ?;
        """, (new_expiry.isoformat(), task_id, worker_id))
        conn.commit()
        success = cursor.rowcount > 0
        return success
    except Exception:
        return False
    finally:
        conn.close()

def recover_stale_leases():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    
    try:
        cursor.execute("SELECT task_id, worker_id FROM worker_leases WHERE expires_at < ?;", (now,))
        stale_leases = cursor.fetchall()
        
        for task_id, worker_id in stale_leases:
            cursor.execute("DELETE FROM worker_leases WHERE task_id = ?;", (task_id,))
            print(f"[RECOVERY] Revoked stale lease for task {task_id[:8]} held by unresponsive worker {worker_id}")
            
        conn.commit()
    except Exception as e:
        print(f"[-] Recovery error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("[HEARTBEAT] Running stale lease recovery check...")
    recover_stale_leases()
