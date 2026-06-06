
import socket
import sys
from datetime import datetime
import threading
from queue import Queue
import io

# حل مشكلة ترميز اللغة العربية في الويندوز (من الدرس السابق)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. تحديد الهدف ونطاق الفحص
target_host = "192.168.91.131"
start_port = 1
end_port = 500

# 2. إنشاء طابور (Queue) لتوزيع المنافذ على الخيوط بشكل منظم
port_queue = Queue()

# تعبئة الطابور بالمنافذ المراد فحصها
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# 3. دالة العمل (Worker) التي سينفذها كل خيط بالتوازي
def scan_worker():
    while not port_queue.empty():
        # سحب المنفذ القادم من الطابور
        port = port_queue.get()
        
        try:
            # إنشاء الاتصال وفحص المنفذ
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0) # وقت الانتظار ثانية واحدة
            result = s.connect_ex((target_host, port))
            
            if result == 0:
                # طباعة المنفذ المفتوح فوراً عند اكتشافه
                print(f"[+] المنفذ {port}: مفتوح (OPEN)")
            
            s.close()
        except Exception:
            pass
        
        # إبلاغ الطابور بأن المهمة الخاصة بهذا المنفذ قد انتهت
        port_queue.task_done()

# --- بداية التنفيذ الفعلي ---
print("-" * 50)
print(f"جاري الفحص السريع (Multithreading) للهدف: {target_host}")
print(f"نطاق الفحص: من {start_port} إلى {end_port}")
print(f"وقت البدء: {str(datetime.now().strftime('%H:%M:%S'))}")
print("-" * 50)

# 4. تحديد عدد الخيوط (Threads) - سنطلق 50 خيطاً يعملون معاً
number_of_threads = 50
threads = []

# إنشاء الخيوط وتشغيلها
for _ in range(number_of_threads):
    t = threading.Thread(target=scan_worker)
    t.start()
    threads.append(t)

# 5. إجبار البرنامج الرئيسي على انتظار انتهاء جميع الخيوط
for t in threads:
    t.join()

print("-" * 50)
print(f"انتهى الفحص بنجاح في: {str(datetime.now().strftime('%H:%M:%S'))}")
print("-" * 50)