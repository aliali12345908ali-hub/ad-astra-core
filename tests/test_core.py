import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contracts.schema import init_db
from core.engine import create_project, create_task

def run_tests():
    print("--- STARTING AD ASTRA LOCAL TESTS ---")
    
    # 1. تهيئة قاعدة البيانات
    init_db()
    
    # 2. إنشاء مشروع تجريبي
    pid = create_project("Test Project Alpha", 100.0)
    assert pid is not None, "Failed to create project"
    
    # 3. اختبار منع التكرار (Idempotency Test)
    key = "idem-key-001"
    t1 = create_task(pid, "test_action", key)
    assert t1 is not None, "First task creation failed"
    
    # محاولة إنشاء مهمة بنفس المفتاح (يجب أن ترفضها النواة)
    t2 = create_task(pid, "test_action", key)
    assert t2 is None, "Idempotency check failed: Duplicate task was allowed!"
    
    print("[+] All Local Core Tests Passed Successfully.")

if __name__ == "__main__":
    run_tests()
