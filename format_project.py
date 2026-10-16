import sys, subprocess

def run_checks():
    print("🧹 جاري فحص وتنسيق الملفات...")
    # تنسيق الكود تلقائياً وضبط المسافات
    subprocess.run(["black", "run_master.py"], stderr=subprocess.DEVNULL)
    
    # فحص وجود أخطاء صياغة أو أقواس مفقودة
    result = subprocess.run(["python3", "-m", "py_compile", "run_master.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ الكود سليِم وخالي من أخطاء Bytax syntax!")
    else:
        print("⚠️ توجد مشكلة في السنتكس:")
        print(result.stderr)

if __name__ == "__main__":
    run_checks()







