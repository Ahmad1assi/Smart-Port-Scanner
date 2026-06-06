
import socket
import sys
from datetime import datetime
import threading
from queue import Queue
import io

# حل مشكلة ترميز اللغة العربية في الويندوز
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. تحديد الهدف ونطاق الفحص
target_host = "192.168.91.131"
start_port = 1
end_port = 500

# إنشاء طابور المنافذ
port_queue = Queue()
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# 2. دالة التقاط البانر (Banner Grabbing)
def grab_banner(s, port):
    try:
        # تقليل وقت انتظار الاستجابة للبانر لضمان سرعة الأداة
        s.settimeout(0.8)
        
        # بعض المنافذ (مثل الويب 80) لا ترسل شيئاً إلا إذا طلبنا نحن أولاً
        if port in [80, 8080]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
            
        # استقبال البيانات القادمة من المنفذ (أول 1024 بايت)
        banner = s.recv(1024)
        
        # تحويل البيانات إلى نص وتنظيفها من السطور الزائدة ليظهر السطر الأول فقط
        clean_banner = banner.decode('utf-8', errors='ignore').strip().split('\n')[0]
        return clean_banner
    except Exception:
        # في حال كان المنفذ مفتوحاً ولكنه لم يرسل نصاً ترحيبياً
        return "لا توجد بيانات ترحيبية (No Banner)"

# 3. دالة العمل (Worker) للمرور على المنافذ
def scan_worker():
    while not port_queue.empty():
        port = port_queue.get()
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0) # وقت انتظار الاتصال بالمنفذ
            
            result = s.connect_ex((target_host, port))
            
            if result == 0:
                # إذا نجح الاتصال، نقوم بالتقاط البانر فوراً قبل إغلاق الـ socket
                service_banner = grab_banner(s, port)
                print(f"[+] المنفذ {port}: مفتوح (OPEN) -> [الخدمة: {service_banner}]")
            
            s.close()
        except Exception:
            pass
        
        # إعلام الطابور بانتهاء فحص المنفذ الحالي
        port_queue.task_done()

# --- بداية التنفيذ ---
print("-" * 60)
print(f"جاري الفحص الذكي والتقاط البانر للهدف: {target_host}")
print(f"نطاق الفحص: من {start_port} إلى {end_port}")
print(f"وقت البدء: {str(datetime.now().strftime('%H:%M:%S'))}")
print("-" * 60)

# إطلاق 50 خيطاً (Threads) للتنفيذ المتوازي
number_of_threads = 50
threads = []

for _ in range(number_of_threads):
    t = threading.Thread(target=scan_worker)
    t.start()
    threads.append(t)

# انتظار انتهاء جميع الخيوط
for t in threads:
    t.join()

print("-" * 60)
print(f"انتهى الفحص بنجاح في: {str(datetime.now().strftime('%H:%M:%S'))}")
print("-" * 60)