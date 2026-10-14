import os
import json
import datetime
import hashlib

def create_invoice(client_name, amount, description):
    invoice_id = "INV-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    issue_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    invoice_data = {
        "invoice_id": invoice_id,
        "issue_date": issue_date,
        "owner": "Abdallah Ben Belgacem",
        "client": client_name,
        "amount": amount,
        "currency": "EUR",
        "description": description,
        "bank_details": {
            "account_holder": "MR ABDALLAH BEN BELGACEM",
            "iban": "FR76 1659 8000 0140 0014 2630 322",
            "bic_swift": "FPELFR21XXX",
            "bank_name": "FPE Charenton",
            "city": "94220 Charenton Le Pont"
        }
    }
    
    os.makedirs("evidence", exist_ok=True)
    file_path = os.path.join("evidence", f"{invoice_id}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(invoice_data, f, ensure_ascii=False, indent=4)
        
    # تسجيل الفاتورة في سجل التدقيق المشفر SHA-256
    audit_entry = {
        "timestamp": issue_date,
        "event_type": "INVOICE_GENERATED",
        "invoice_id": invoice_id,
        "client": client_name,
        "amount": amount
    }
    
    audit_line = json.dumps(audit_entry, ensure_ascii=False)
    current_hash = hashlib.sha256(audit_line.encode()).hexdigest()
    audit_record = {"entry": audit_entry, "current_hash": current_hash}
    
    with open(os.path.join("evidence", "audit_trail.jsonl"), "a", encoding="utf-8") as af:
        af.write(json.dumps(audit_record, ensure_ascii=False) + "\n")
        
    print("================================================================")
    print(f" [✓] Invoice Created Successfully: {invoice_id}")
    print(f" [👤] Owner: Abdallah Ben Belgacem")
    print(f" [🏢] Client: {client_name}")
    print(f" [💶] Amount: {amount} EUR")
    print(f" [🔒] Secured in SHA-256 Audit Trail & Saved to evidence/")
    print("================================================================")

if __name__ == "__main__":
    # مثال لتوليد فاتورة لأول عميل
    create_invoice("Global Client SARL", 1500.00, "Autonomous Core Consulting & Setup Services")
