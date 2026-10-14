import sqlite3
import datetime

DB_PATH = "evidence/ad_astra_local.db"

def acquire_task_lease(task_id, worker_id, lease_duration_seconds=30):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(seconds=lease_duration_seconds)
    
    try:
        cursor.execute("SELECT fence_token, worker_id, expires_at FROM worker_leases WHERE task_id = ?;", (task_id,))
        row = cursor.fetchone()
        
        if row:
            current_token, current_worker, current_expiry = row
            if current_expiry > now.isoformat() and current_worker != worker_id:
                print(f"[-] Lease Denied: Task {task_id} is already leased by worker {current_worker}")
                return None
            
            new_token = current_token + 1
            cursor.execute("""
                UPDATE worker_leases 
                SET worker_id = ?, fence_token = ?, expires_at = ? 
                WHERE task_id = ?;
            """, (worker_id, new_token, expires_at.isoformat(), task_id))
            conn.commit()
            print(f"[+] Lease Renewed for Worker {worker_id} with Fence Token: {new_token}")
            return new_token
        else:
            cursor.execute("""
                INSERT INTO worker_leases (task_id, worker_id, fence_token, expires_at)
                VALUES (?, ?, 1, ?);
            """, (task_id, worker_id, expires_at.isoformat()))
            conn.commit()
            print(f"[+] Lease Acquired for Worker {worker_id} with Fence Token: 1")
            return 1
            
    except Exception as e:
        conn.rollback()
        print(f"[-] Lease Error: {e}")
        return None
    finally:
        conn.close()

def release_stale_leases():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    try:
        cursor.execute("DELETE FROM worker_leases WHERE expires_at < ?;", (now,))
        count = cursor.rowcount
        conn.commit()
        if count > 0:
            print(f"[+] Cleaned up {count} expired/stale worker leases.")
    except Exception as e:
        print(f"[-] Cleanup Error: {e}")
    finally:
        conn.close()
