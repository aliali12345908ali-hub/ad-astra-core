import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import threading
import time
import sqlite3
from core.lease_engine import acquire_task_lease
from core.evidence_logger import log_evidence

DB_PATH = "evidence/ad_astra_local.db"

def get_all_task_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT task_id FROM tasks;")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def simulate_worker(worker_id, task_ids):
    print(f"[WORKER {worker_id}] Started and ready to compete.")
    for tid in task_ids:
        token = acquire_task_lease(tid, worker_id, lease_duration_seconds=30)
        if token:
            print(f"[WORKER {worker_id}] Acquired lease for task {tid[:8]}... with Fence Token: {token}")
            log_evidence("WORKER_ACQUIRED_LEASE", {"worker_id": worker_id, "task_id": tid, "fence_token": token})
        else:
            print(f"[WORKER {worker_id}] Denied lease for task {tid[:8]}... (Already locked)")
        time.sleep(0.3)

def run_concurrency_test():
    task_ids = get_all_task_ids()
    if not task_ids:
        print("[-] No tasks found in database to test concurrency.")
        return
        
    print("==================================================")
    print("   AD ASTRA CORE: Multi-Worker Concurrency Pool   ")
    print("==================================================")
    print(f"[+] Found {len(task_ids)} tasks. Launching workers competition...")
    
    workers = ["worker-alpha", "worker-beta", "worker-gamma"]
    threads = []
    
    for w in workers:
        t = threading.Thread(target=simulate_worker, args=(w, task_ids))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("==================================================")
    print("[+] Concurrency pool test completed successfully.")
    print("==================================================")

if __name__ == "__main__":
    run_concurrency_test()
