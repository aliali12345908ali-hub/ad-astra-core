import os
import json
import datetime
import hashlib

EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

BANK_DETAILS = {
    "account_holder": "MR ABDALLAH BEN BELGACEM",
    "iban": "FR76 1659 8000 0140 0014 2630 322",
    "bic_swift": "FPELFR21XXX",
    "bank_code": "16598",
    "branch_code": "00001",
    "account_number": "40001426303",
    "key": "22",
    "domiciliation": "FPE Charenton, 94220 Charenton Le Pont"
}

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

def process_payout_configuration():
    event_details = {
        "status": "PAYMENT_GATEWAY_CONFIGURED",
        "beneficiary": BANK_DETAILS["account_holder"],
        "iban_last4": BANK_DETAILS["iban"][-4:],
        "swift": BANK_DETAILS["bic_swift"]
    }
    log_audit_event("BANK_GATEWAY_LINKED", event_details)
    return event_details

def display_payment_status():
    os.system("clear" if os.name == "posix" else "cls")
    print("==================================================================")
    print("      AD ASTRA - AUTONOMOUS CORE (PAYMENT & PAYOUT ENGINE)       ")
    print("      Owner & Beneficiary: Abdallah Ben Belgacem                  ")
    print("==================================================================")
    print(f" [*] Account Holder : {BANK_DETAILS['account_holder']}")
    print(f" [*] IBAN           : {BANK_DETAILS['iban']}")
    print(f" [*] BIC / SWIFT    : {BANK_DETAILS['bic_swift']}")
    print(f" [*] Bank Branch    : {BANK_DETAILS['domiciliation']}")
    print("------------------------------------------------------------------")
    print(" [*] Audit Trail Status  : SHA-256 Encrypted & Logged")
    print(" [*] Payout Status       : READY FOR DIRECT WIRE TRANSFERS")
    print("==================================================================")

if __name__ == "__main__":
    process_payout_configuration()
    display_payment_status()
