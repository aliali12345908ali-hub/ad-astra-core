import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contracts.schema import init_db
from core.engine import create_project
from core.budget_engine import reserve_budget

def run_budget_tests():
    print("--- STARTING AD ASTRA ATOMIC BUDGET TESTS ---")
    
    init_db()
    # إنشاء مشروع بحد أقصى 100 يورو للميزانية
    pid = create_project("Financial Project", 100.0)
    
    # 1. محاولة حجز مبلغ ضمن المحدود (مثلاً 60 يورو) -> يجب أن ينجح
    r1 = reserve_budget(pid, 60.0)
    assert r1 == True, "Budget reservation of 60 EUR should have succeeded"
    
    # 2. محاولة حجز مبلغ إضافي (مثلاً 50 يورو) ليصبح المجموع 110 (يتجاوز الحد 100) -> يجب أن يرفض
    r2 = reserve_budget(pid, 50.0)
    assert r2 == False, "Budget reservation exceeding hard limit should have been denied"
    
    # 3. محاولة حجز مبلغ دقيق يكمل الحد تماماً (مثلاً 40 يورو) ليصبح المجموع 100 -> يجب أن ينجح
    r3 = reserve_budget(pid, 40.0)
    assert r3 == True, "Budget reservation completing the exact limit should have succeeded"
    
    print("[+] All Atomic Budget & Enforcement Tests Passed Successfully.")

if __name__ == "__main__":
    run_budget_tests()
