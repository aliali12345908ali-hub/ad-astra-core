import time
import datetime
import sqlite3
import threading
from worker_heartbeat import recover_stale_leases

DB_PATH = "evidence/ad_astra_local.db"

def daemon_worker_pool():
    print(f"[DAEMON] Background worker pool active at {datetime.datetime.utcnow().isoformat()}")
    # هنا يتم مراقبة وتنفيذ المهام بشكل دوري ومستمر
    while True:
        try:
            # 1. تنظيف الحيازات المنتهية أو المعلقة تلقائياً
            recover_stale_leases()
            
            # 2. فحص المهام الجديدة وتوزيعها
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT task_id FROM tasks WHERE status = 'QUEUED';")
            queued_tasks = cursor.fetchall()
            conn.close()
            
            if queued_tasks:
                print(f"[DAEMON] Found {len(queued_tasks)} queued tasks to process.")
                
            time.sleep(10) # الفحص كل 10 ثوانٍ
        except Exception as e:
            print(f"[-] Daemon loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("==================================================")
    print("   AD ASTRA CORE: CONTINUOUS DAEMON MODE          ")
    print("==================================================")
    daemon_worker_pool()
