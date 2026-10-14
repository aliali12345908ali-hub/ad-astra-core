import os
import sqlite3
import threading
import time
import datetime
import json
import hashlib
from core.finance_ledger import process_secure_payment, init_finance_tables

DB_PATH = "evidence/ad_astra_local.db"
EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

def init_database():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    init_finance_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            task_type TEXT NOT NULL,
            status TEXT NOT NULL,
            idempotency_key TEXT UNIQUE,
            FOREIGN KEY(project_id) REFERENCES projects(project_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS worker_leases (
            task_id TEXT PRIMARY KEY,
            worker_id TEXT NOT NULL,
            fence_token INTEGER NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY(task_id) REFERENCES tasks(task_id)
        );
    """)
    cursor.execute("INSERT OR IGNORE INTO wallets (wallet_id, owner_name, balance, updated_at) VALUES ('master-treasury', 'Master Treasury', 5000.0, ?);", 
                   (datetime.datetime.now(datetime.timezone.utc).isoformat(),))
    conn.commit()
    conn.close()

def get_last_hash():
    if not os.path.exists(AUDIT_FILE):
        return "0" * 64
    last_line = None
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line
    if not last_line:
        return "0" * 64
    try:
        record = json.loads(last_line)
        return record.get("current_hash", "0" * 64)
    except:
        return "0" * 64

def log_evidence(event_type, details):
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prev_hash = get_last_hash()
    payload = {
        "timestamp": timestamp,
        "event_type": event_type,
        "details": details,
        "prev_hash": prev_hash
    }
    current_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()
    evidence_record = {**payload, "current_hash": current_hash}
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(evidence_record, ensure_ascii=False) + "\n")

def acquire_task_lease(task_id, worker_id, lease_duration_seconds=30):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=lease_duration_seconds)
    try:
        cursor.execute("SELECT fence_token, worker_id, expires_at FROM worker_leases WHERE task_id = ?;", (task_id,))
        row = cursor.fetchone()
        if row:
            current_token, current_worker, current_expiry = row
            if current_expiry > now.isoformat() and current_worker != worker_id:
                return None
            new_token = current_token + 1
            cursor.execute("""
                UPDATE worker_leases 
                SET worker_id = ?, fence_token


rm -f evidence/audit_trail.jsonl
python run_master.py
python core/audit_verifier.py


python run_master.py


cat << 'EOF' > core/master_server.py
import http.server
import socketserver
import sqlite3
import json
import datetime

PORT = 8080
DB_PATH = "evidence/ad_astra_local.db"

class MasterOrchestratorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # جلب حالة المهام والخزينة من قاعدة البيانات
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='QUEUED';")
            queued_count = cursor.fetchone()[0]
            cursor.execute("SELECT balance FROM wallets WHERE wallet_id='master-treasury';")
            treasury_row = cursor.fetchone()
            treasury_balance = treasury_row[0] if treasury_row else 0.0
            conn.close()
            
            status_data = {
                "server": "Ad Astra Master Core",
                "status": "ONLINE",
                "queued_tasks": queued_count,
                "treasury_balance": treasury_balance,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            self.wfile.write(json.dumps(status_data, indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found - Ad Astra Core")

if __name__ == "__main__":
    print(f"==================================================")
    print(f"   AD ASTRA: MASTER ORCHESTRATION SERVER          ")
    print(f"   Running on port {PORT}...                      ")
    print(f"==================================================")
    with socketserver.TCPServer(("", PORT), MasterOrchestratorHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Master Server stopped securely.")
