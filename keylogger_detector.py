import psutil
import time
import winreg
from datetime import datetime

# ================= CONFIGURATION =================

LOG_FILE = "logs.txt"
DEBUG = False   # Keep False for final version

WHITELIST = [
    "explorer.exe",
    "svchost.exe",
    "chrome.exe",
    "msedge.exe",
    "system",
    "explorer.exe",
    "svchost.exe",
    "system",
    "onedrive.exe",
    "discord.exe"
]

# ================= LOGGING =================

def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# ================= PROCESS ENUMERATION =================

def get_running_processes():
    return psutil.process_iter()

# ================= NETWORK MONITORING =================

def get_network_pids():
    pids = set()
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "ESTABLISHED" and conn.pid:
            pids.add(conn.pid)
    return pids

# ================= STARTUP PERSISTENCE =================

def get_startup_entries():
    entries = []
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run"
        )
        i = 0
        while True:
            try:
                _, value, _ = winreg.EnumValue(key, i)
                entries.append(value.lower())
                i += 1
            except:
                break
    except:
        pass
    return entries

# ================= THREAT SCORING =================

def calculate_threat_score(proc, network_pids, startup_entries):
    score = 0
    try:
        name = proc.name().lower()

        try:
            exe = proc.exe().lower()
        except:
            exe = ""

        if name in WHITELIST:
            return 0

        if "appdata" in exe or "temp" in exe:
            score += 1

        if proc.pid in network_pids:
            score += 2

        if any(exe in s for s in startup_entries):
            score += 2

        if proc.cpu_percent(interval=0.1) > 2:
            score += 1

        if DEBUG:
            print(f"[DEBUG] {name} -> Score: {score}")

    except:
        pass

    return score

# ================= RESPONSE ENGINE =================

def block_process(proc):
    try:
        proc.terminate()
        log_event(f"BLOCKED: {proc.name()} (PID {proc.pid})")
    except:
        log_event(f"FAILED TO BLOCK: PID {proc.pid}")

# ================= MAIN MONITOR =================

def monitor():
    log_event("Keylogger Detection Started")
    startup_entries = get_startup_entries()

    try:
        while True:
            network_pids = get_network_pids()

            for proc in get_running_processes():
                score = calculate_threat_score(
                    proc,
                    network_pids,
                    startup_entries
                )

                if score >= 4:
                    block_process(proc)

            time.sleep(10)

    except KeyboardInterrupt:
        log_event("Keylogger Detection Stopped")
        print("\n[INFO] Keylogger Detection Tool stopped.")

    
# ================= ENTRY POINT =================

if __name__ == "__main__":  
    monitor()
