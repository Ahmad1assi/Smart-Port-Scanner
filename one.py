import socket
import sys
from datetime import datetime
import io

# إجبار المخرجات على استخدام ترميز UTF-8 لدعم اللغة العربية
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. تحديد الهدف
target_host = "192.168.91.131"


# 2. تحديد قائمة بالمنافذ الشهيرة التي نريد فحصها
# 21: FTP, 22: SSH, 80: HTTP, 443: HTTPS
ports_to_scan = [21, 22, 80, 443, 8080]

print("-" * 50)
print(f"جاري فحص الهدف: {target_host}")
print(f"وقت بدء الفحص: {str(datetime.now())}")
print("-" * 50)

try:
    # 3. الحلقة التكرارية للمرور على كل منفذ وفحصه
    for port in ports_to_scan:
        # إنشاء Socket اتصال (AF_INET يعني IPv4، و SOCK_STREAM يعني بروتوكول TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # تعيين وقت انتظار (Timeout) ثانية واحدة؛ حتى لا يعلق البرنامج إذا كان المنفذ مغلقاً
        s.settimeout(1.0)
        
        # محاولة الاتصال بالمنفذ. الدالة connect_ex ترجع القيمة 0 إذا نجح الاتصال
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f"[+] المنفذ {port}: مفتوح (OPEN)")
        else:
            print(f"[-] المنفذ {port}: مغلق (CLOSED)")
            
        # إغلاق الـ Socket بعد انتهاء فحص المنفذ الحالي
        s.close()

except KeyboardInterrupt:
    print("\nتم إيقاف الفحص بواسطة المستخدم.")
    sys.exit()

except socket.gaierror:
    print("\nتعذر الوصول إلى اسم المضيف (Hostname).")
    sys.exit()

except socket.error:
    print("\nتعذر الاتصال بالسيرفر.")
    sys.exit()