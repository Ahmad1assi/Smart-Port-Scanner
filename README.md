
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
   git clone [https://github.com/Ahmad1assi/Smart-Port-Scanner.git](https://github.com/Ahmad1assi/Smart-Port-Scanner.git)