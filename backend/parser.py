import os
import time
from database import init_db, insert_log
from correlation import analyze_log

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'system_logs.txt')

def parse_line(line):
    """Parse a single log line into a dictionary"""
    try:
        parts = line.strip().split(' | ')
        if len(parts) < 4:
            return None

        timestamp = parts[0].strip()
        user = parts[1].replace('user:', '').strip()
        action = parts[2].replace('action:', '').strip()
        ip = parts[3].replace('ip:', '').strip()
        detail = parts[4].replace('detail:', '').strip() if len(parts) > 4 else ''

        return {
            'timestamp': timestamp,
            'user': user,
            'action': action,
            'ip': ip,
            'detail': detail
        }
    except Exception as e:
        print(f"[!] Parse error: {e}")
        return None

def tail_log_file():
    """Continuously read new lines from log file (like Linux tail -f)"""
    print(f"[+] Watching log file: {LOG_FILE}")
    init_db()

    with open(LOG_FILE, 'r') as f:
        # Move to end of file first
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            log = parse_line(line)
            if log:
                # Save to database
                insert_log(
                    log['timestamp'],
                    log['user'],
                    log['action'],
                    log['ip'],
                    log['detail']
                )
                print(f"[LOG] {log['action']} | {log['user']} | {log['ip']}")

                # Send to correlation engine for threat analysis
                analyze_log(log)

def parse_existing_logs():
    """Parse all existing logs in the file (for testing)"""
    print(f"[+] Parsing existing logs from: {LOG_FILE}")
    init_db()

    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    parsed = 0
    for line in lines:
        log = parse_line(line)
        if log:
            insert_log(
                log['timestamp'],
                log['user'],
                log['action'],
                log['ip'],
                log['detail']
            )
            analyze_log(log)
            parsed += 1

    print(f"[+] Parsed {parsed} logs successfully")

if __name__ == "__main__":
    parse_existing_logs()