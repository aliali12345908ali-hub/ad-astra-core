import os
import json
import datetime
import hashlib

EVIDENCE_DIR = "evidence"
INVOICES_DIR = os.path.join(EVIDENCE_DIR, "invoices")
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

BANK_DETAILS = {
    "account_holder": "MR ABDALLAH BEN BELGACEM",
    "iban": "FR76 1659 8000 0140 0014 2630 322",
    "bic_swift": "FPELFR21XXX"
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

def generate_invoice(client_name, amount, currency="EUR", service_desc="Ad Astra Autonomous Infrastructure License"):
    os.makedirs(INVOICES_DIR, exist_ok=True)
    inv_id = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    invoice_data = {
        "invoice_id": inv_id,
        "issue_date": timestamp,
        "issuer": BANK_DETAILS["account_holder"],
        "client": client_name,
        "service": service_desc,
        "amount": amount,
        "currency": currency,
        "payment_info": {
            "iban": BANK_DETAILS["iban"],
            "swift": BANK_DETAILS["bic_swift"]
        }
    }
    
    file_path = os.path.join(INVOICES_DIR, f"{inv_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(invoice_data, f, indent=4, ensure_ascii=False)
        
    log_audit_event("INVOICE_GENERATED", {"invoice_id": inv_id, "client": client_name, "amount": amount})
    return invoice_data

if __name__ == "__main__":
    sample_inv = generate_invoice("Enterprise Client Ltd", 2500.00, "EUR")
    print("==================================================================")
    print("        AD ASTRA - AUTOMATED INVOICE GENERATOR                  ")
    print("        Owner: Abdallah Ben Belgacem                             ")
    print("==================================================================")
    print(f" [*] Invoice ID  : {sample_inv['invoice_id']}")
    print(f" [*] Client      : {sample_inv['client']}")
    print(f" [*] Amount      : {sample_inv['amount']} {sample_inv['currency']}")
    print(f" [*] Beneficiary : {sample_inv['issuer']}")
    print(f" [*] IBAN Target : {sample_inv['payment_info']['iban']}")
    print("==================================================================")
