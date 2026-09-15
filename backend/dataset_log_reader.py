import csv
import time
import os
from datetime import datetime

DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'cybersecurity_attacks.csv')
LOG_FILE     = os.path.join(os.path.dirname(__file__), '..', 'logs', 'system_logs.txt')

# Map dataset Attack Type → our action format
ACTION_MAP = {
    "DDoS"            : "PORT_SCAN",
    "Malware"         : "FILE_DELETE",
    "Intrusion"       : "LOGIN_FAILED",
    "Brute Force"     : "LOGIN_FAILED",
    "Port Scan"       : "PORT_SCAN",
    "Ransomware"      : "FILE_DELETE",
    "Data Exfiltration": "LARGE_DOWNLOAD",
    "Man-in-the-Middle": "CONFIG_CHANGE",
    "SQL Injection"   : "PRIVILEGE_ESCALATION",
    "XSS"             : "LOGIN_FAILED",
}

def map_action(attack_type):
    """Convert dataset attack type to our action format"""
    for key in ACTION_MAP:
        if key.lower() in attack_type.lower():
            return ACTION_MAP[key]
    return "LOGIN_SUCCESS"  # default for unknown/benign

def map_severity(severity):
    """Normalize severity to HIGH/MEDIUM/LOW"""
    s = severity.strip().lower()
    if s == "high":
        return "HIGH"
    elif s == "medium":
        return "MEDIUM"
    else:
        return "LOW"

def format_timestamp(raw_ts):
    """Clean timestamp to our format"""
    try:
        dt = datetime.strptime(raw_ts.strip(), "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_reader(delay=0.1,limit=1000):
    print(f"[+] Reading dataset: {DATASET_PATH}")
    print(f"[+] Writing to: {LOG_FILE}")

    if not os.path.exists(DATASET_PATH):
        print(f"[!] Dataset file not found at {DATASET_PATH}")
        return

    count = 0
    with open(DATASET_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        with open(LOG_FILE, 'a', encoding='utf-8') as logfile:
            for row in reader:
                if count >= limit:      # ← add this check
                    print(f"[+] Limit reached — stopping at {limit} logs")
                    break
                try:
                    # Extract fields
                    timestamp   = format_timestamp(row['Timestamp'])
                    ip          = row['Source IP Address'].strip()
                    user        = ip.replace('.', '_')   # IP as username
                    attack_type = row['Attack Type'].strip()
                    severity    = row['Severity Level'].strip()
                    anomaly     = row['Anomaly Scores'].strip()
                    action_taken= row['Action Taken'].strip()

                    # Convert to our format
                    action = map_action(attack_type)
                    detail = f"Attack:{attack_type} | Severity:{map_severity(severity)} | Score:{anomaly} | Action:{action_taken}"

                    # Write log line in our exact format
                    log_line = f"{timestamp} | user:{user} | action:{action} | ip:{ip} | detail:{detail}\n"

                    logfile.write(log_line)
                    logfile.flush()  # write immediately

                    count += 1
                    print(f"[{count}] {action} | {ip} | {attack_type}")

                    time.sleep(delay)  # slow down so parser can keep up

                except Exception as e:
                    print(f"[!] Error on row {count}: {e}")
                    continue

    print(f"\n[+] Done! {count} logs written to system_logs.txt")

if __name__ == "__main__":
    run_reader(delay=0.05, limit=1000)