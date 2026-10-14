import os
import json
import hashlib

AUDIT_FILE = "evidence/audit_trail.jsonl"

def verify_audit_trail():
    if not os.path.exists(AUDIT_FILE):
        print("[-] Audit trail file does not exist.")
        return False
        
    print("[VERIFIER] Starting cryptographic audit chain verification...")
    last_current_hash = None
    line_number = 0
    
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line_number += 1
            if not line.strip():
                continue
            try:
                record = json.loads(line.strip())
            except json.JSONDecodeError:
                print(f"[-] Error: Malformed JSON at line {line_number}")
                return False
                
            recorded_prev = record.get("prev_hash")
            recorded_curr = record.get("current_hash")
            
            if line_number > 1 and recorded_prev != last_current_hash:
                print(f"[-] TAMPER DETECTED at line {line_number}! Previous hash mismatch.")
                return False
                
            payload = {
                "timestamp": record.get("timestamp"),
                "event_type": record.get("event_type"),
                "details": record.get("details"),
                "prev_hash": recorded_prev
            }
            calculated = hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()
            
            if calculated != recorded_curr:
                print(f"[-] TAMPER DETECTED at line {line_number}! Current hash mismatch.")
                return False
                
            last_current_hash = recorded_curr
            
    print(f"[+] Audit trail verification PASSED successfully. {line_number} records verified.")
    return True

if __name__ == "__main__":
    verify_audit_trail()
