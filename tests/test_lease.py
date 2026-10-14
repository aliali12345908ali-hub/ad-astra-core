import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contracts.schema import init_db
from core.engine import create_project, create_task
from core.lease_engine import acquire_task_lease

def run_lease_tests():
    print("--- STARTING AD ASTRA LEASE & FENCING TESTS ---")
    
    init_db()
    pid = create_project("Lease Test Project", 50.0)
    tid = create_task(pid, "compute_action", "idem-lease-001")
    
    # 1. العامل الأول يحوز المهمة لأول مرة
    token1 = acquire_task_lease(tid, "worker-alpha", 30)
    assert token1 == 1, "First lease token should be 1"
    
    # 2. عامل آخر يحاول حيازة نفس المهمة وهي سارية (يجب أن ترفض)
    token_denied = acquire_task_lease(tid, "worker-beta", 30)
    assert token_denied is None, "Lease should have been denied for concurrent worker"
    
    # 3. نفس العامل يجدد الحيازة (يجب أن يرتفع رمز الـ Fencing)
    token2 = acquire_task_lease(tid, "worker-alpha", 30)
    assert token2 == 2, "Renewed lease token should increment to 2"
    
    print("[+] All Lease & Fencing Tests Passed Successfully.")

if __name__ == "__main__":
    run_lease_tests()
