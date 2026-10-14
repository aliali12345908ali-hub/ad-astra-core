import os
import datetime
import json
import hashlib

EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

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
    timestamp = datetime.datetime.utcnow().isoformat()
    prev_hash = get_last_hash()
    
    payload = {
        "timestamp": timestamp,
        "event_type": event_type,
        "details": details,
        "prev_hash": prev_hash
    }
    
    # حساب بصمة الشفرة الحالية بناءً على محتوى الحدث وبصمة السجل السابق
    payload_string = json.dumps(payload, sort_keys=True)
    current_hash = hashlib.sha256(payload_string.encode('utf-8')).hexdigest()
    
    evidence_record = {
        **payload,
        "current_hash": current_hash
    }
    
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(evidence_record, ensure_ascii=False) + "\n")
        
    print(f"[EVIDENCE SECURE] Logged [{event_type}] with Hash: {current_hash[:12]}...")

if __name__ == "__main__":
    log_evidence("SECURE_INIT", {"status": "Cryptographic audit chain active"})
