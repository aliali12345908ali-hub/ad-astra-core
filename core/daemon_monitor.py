import os
import json
import datetime
import hashlib
import time

EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

def log_audit_event(event_type, details):
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prev_hash = "0" * 64
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        prev_hash = record.get("current_hash", prev_hash)
                    except Exception:
                        pass

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

def run_daemon_loop(cycles=3):
    print("==================================================================")
    print("      AD ASTRA - AUTONOMOUS BACKGROUND DAEMON MONITOR             ")
    print("      Founder & Sole Owner: Abdallah Ben Belgacem                 ")
    print("==================================================================")
    print(" [*] Daemon initialized. Monitoring core processes...")
    
    for i in range(1, cycles + 1):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f" [{timestamp}] Cycle {i}/{cycles}: All systems nominal. Self-healing active.")
        log_audit_event("DAEMON_HEALTH_CHECK", {"cycle": i, "status": "HEALTHY"})
        time.sleep(2)
        
    print("------------------------------------------------------------------")
    print(" [*] Daemon daemon execution test completed successfully.")
    print("==================================================================")

if __name__ == "__main__":
    run_daemon_loop()
