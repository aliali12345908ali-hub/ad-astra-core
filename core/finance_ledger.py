import sqlite3
import datetime
import os
import json
import hashlib

DB_PATH = "evidence/ad_astra_local.db"
EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

def init_finance_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            wallet_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            updated_at TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_transactions (
            tx_id TEXT PRIMARY KEY,
            sender_id TEXT,
            receiver_id TEXT,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)
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

def log_financial_evidence(event_type, details):
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    timestamp =

cat << 'EOF' > core/finance_ledger.py
import sqlite3
import datetime
import os
import json
import hashlib

DB_PATH = "evidence/ad_astra_local.db"
EVIDENCE_DIR = "evidence"
AUDIT_FILE = os.path.join(EVIDENCE_DIR, "audit_trail.jsonl")

def init_finance_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            wallet_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            updated_at TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_transactions (
            tx_id TEXT PRIMARY KEY,
            sender_id TEXT,
            receiver_id TEXT,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)
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

def log_financial_evidence(event_type, details):
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

def process_secure_payment(tx_id, sender_id, receiver_id, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        cursor.execute("SELECT balance FROM wallets WHERE wallet_id = ?;", (sender_id,))
        sender_row = cursor.fetchone()
        if not sender_row or sender_row[0] < amount:
            return False
        cursor.execute("UPDATE wallets SET balance = balance - ?, updated_at = ? WHERE wallet_id = ?;", (amount, now, sender_id))
        cursor.execute("INSERT OR IGNORE INTO wallets (wallet_id, owner_name, balance, updated_at) VALUES (?, ?, 0.0, ?);", 
                       (receiver_id, f"Receiver-{receiver_id}", now))
        cursor.execute("UPDATE wallets SET balance = balance + ?, updated_at = ? WHERE wallet_id = ?;", (amount, now, receiver_id))
        cursor.execute("""
            INSERT INTO financial_transactions (tx_id, sender_id, receiver_id, amount, status, timestamp)
            VALUES (?, ?, ?, ?, 'COMPLETED', ?);
        """, (tx_id, sender_id, receiver_id, amount, now))
        conn.commit()
        log_financial_evidence("FINANCIAL_TX_COMPLETED", {
            "tx_id": tx_id, "sender_id": sender_id, "receiver_id": receiver_id, "amount": amount
        })
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()
