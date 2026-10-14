import sqlite3

DB_PATH = "evidence/ad_astra_local.db"

def reserve_budget(project_id, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        # بدء معاملة ذرية صريحة
        cursor.execute("BEGIN TRANSACTION;")
        
        # جلب الميزانية الحالية والقيود
        cursor.execute("SELECT hard_limit, current_spent, reserved_amount FROM budgets WHERE project_id = ?;", (project_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"[-] Budget Error: Project {project_id} not found.")
            conn.rollback()
            return False
            
        hard_limit, current_spent, reserved_amount = row
        
        # التحقق من أن المبلغ المطلوب حجزه لا يتجاوز الحد الأقصى
        if (current_spent + reserved_amount + amount) > hard_limit:
            print(f"[-] Budget Denied: Reservation of {amount} EUR exceeds hard limit ({hard_limit} EUR).")
            conn.rollback()
            return False
            
        # تحديث قيمة المبالغ المحجوزة
        new_reserved = reserved_amount + amount
        cursor.execute("""
            UPDATE budgets 
            SET reserved_amount = ? 
            WHERE project_id = ?;
        """, (new_reserved, project_id))
        
        conn.commit()
        print(f"[+] Budget Reserved Successfully: {amount} EUR (Total Reserved: {new_reserved} EUR)")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"[-] Budget Transaction Error: {e}")
        return False
    finally:
        conn.close()
