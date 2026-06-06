
# Smart Port Scanner v1.1

A fast, multi-threaded port scanner written in Python, designed for network discovery and reconnaissance. The tool allows users to scan custom port ranges, perform banner grabbing to identify running services, and automatically save the findings into a structured log file.

## 🚀 Features
- **High Performance:** Powered by multi-threading (100 parallel threads) to scan hundreds of ports in seconds.
- **Dynamic Inputs:** Accepts both target IP addresses and domain names (e.g., `scanme.nmap.org`).
- **Banner Grabbing:** Probes open ports to capture service banners and discover software versions.
- **Thread-Safe Logging:** Automatically saves results into a separate `.txt` file for each target without text overlapping.
- **Error Handling:** Gracefully handles invalid inputs, connection timeouts, and user interruptions (`Ctrl+C`).

## 🛠️ Prerequisites
- Python 3.11 or higher installed on your system.

## 🔧 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ahmad1assi/Smart-Port-Scanner.git

2. Run the tool:
 bash 
   python scan_ip.py


3. Provide inputs:
Enter the target IP/Domain.
Enter the start and end port numbers.

4. 📄 Sample Output
------------------------------------------------------------
Scanning Target: 127.0.0.1
Scan Started At: 14:30:15
Results will be saved to: scan_results_127.0.0.1.txt
------------------------------------------------------------
 Port 22: OPEN -> [Service: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5]
 Port 80: OPEN -> [Service: HTTP/1.1 200 OK]
Port 443: OPEN -> [Service: No Banner]
------------------------------------------------------------
[*] Scan completed. Report saved to 'scan_results_127.0.0.1.txt'

⚠️ Disclaimer
This tool is developed strictly for educational and authorized penetration testing purposes. Scanning targets without prior explicit permission is illegal. The developer assumes no liability for any misuse or damage caused by this tool.