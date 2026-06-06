import socket
import sys
from datetime import datetime
import threading
from queue import Queue

print("-" * 60)
print("             Smart Port Scanner v1.1             ")
print("-" * 60)

# 1. Dynamic Target Input
user_target = input("[?] Enter Target IP or Domain (e.g., scanme.nmap.org): ").strip()

try:
    target_host = socket.gethostbyname(user_target)
    print(f"[*] Target resolved: {user_target} -> ({target_host})")
except socket.gaierror:
    print("\n[!] Error: Unable to resolve target. Check host name or internet connection.")
    sys.exit()

# 2. Dynamic Port Range Input
try:
    start_port = int(input("[?] Enter Start Port (e.g., 1): "))
    end_port = int(input("[?] Enter End Port (e.g., 100): "))
    
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("\n[!] Error: Invalid port range (Must be 1-65535, and Start <= End).")
        sys.exit()
except ValueError:
    print("\n[!] Error: Please enter valid numbers for ports.")
    sys.exit()

# اسم الملف الذي ستُحفظ فيه النتائج تلقائياً بناءً على اسم الهدف
log_file_name = f"scan_results_{target_host}.txt"

# إنشاء قفل الخيوط (Thread Lock) لمنع تداخل المخرجات
file_lock = threading.Lock()

# تجهيز ملف الحفظ وكتابة الترويسة (Header) فيه
with open(log_file_name, "w", encoding="utf-8") as f:
    f.write("-" * 60 + "\n")
    f.write(f"Scan Report for Target: {target_host} ({user_target})\n")
    f.write(f"Started At: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
    f.write("-" * 60 + "\n\n")

# تعبئة طابور المنافذ
port_queue = Queue()
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# 3. Banner Grabbing Function
def grab_banner(s, port):
    try:
        s.settimeout(0.8)
        if port in [80, 8080]:
            s.send(f"HEAD / HTTP/1.1\r\nHost: {target_host}\r\n\r\n".encode())
        banner = s.recv(1024)
        clean_banner = banner.decode('utf-8', errors='ignore').strip().split('\n')[0]
        return clean_banner
    except Exception:
        return "No Banner"

# 4. Thread Worker Function
def scan_worker():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((target_host, port))
            
            if result == 0:
                service_banner = grab_banner(s, port)
                output_line = f"[+] Port {port}: OPEN -> [Service: {service_banner}]"
                
                # تفعيل القفل: خيط واحد فقط يطبع ويكتب في الملف الآن
                with file_lock:
                    print(output_line) # الطباعة على الشاشة
                    with open(log_file_name, "a", encoding="utf-8") as f:
                        f.write(output_line + "\n") # الكتابة في الملف
            
            s.close()
        except Exception:
            pass
        port_queue.task_done()

# --- Start Scanning ---
print("-" * 60)
print(f"[*] Scanning Target: {target_host}")
print(f"[*] Scan Started At: {str(datetime.now().strftime('%H:%M:%S'))}")
print(f"[*] Results will be saved to: {log_file_name}")
print("-" * 60)

# إطلاق 100 خيط
number_of_threads = 100
threads = []

for _ in range(number_of_threads):
    t = threading.Thread(target=scan_worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# كتابة خاتمة التقرير في الملف
with open(log_file_name, "a", encoding="utf-8") as f:
    f.write("\n" + "-" * 60 + "\n")
    f.write(f"Scan Completed Successfully At: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
    f.write("-" * 60 + "\n")

print("-" * 60)
print(f"[*] Scan completed. Report saved to '{log_file_name}'")
print("-" * 60)