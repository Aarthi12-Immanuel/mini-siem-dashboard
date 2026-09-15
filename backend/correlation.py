from datetime import datetime, timedelta
from collections import defaultdict
from database import insert_alert

# In-memory tracking
login_failures  = defaultdict(list)
port_scans      = defaultdict(list)
file_deletes    = defaultdict(list)
large_downloads = defaultdict(list)

# Known attacker IPs
KNOWN_BAD_IPS = [
    "45.33.32.156",
    "103.21.244.0",
    "185.220.101.5"
]

def get_now():
    return datetime.now()

def is_after_hours(timestamp_str):
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.hour < 8 or dt.hour >= 20
    except:
        return False

def clean_old_events(event_list, window_seconds=120):
    cutoff = get_now() - timedelta(seconds=window_seconds)
    return [t for t in event_list if t > cutoff]

def fire_alert(log, threat_type, severity, description, score):
    print(f"[🚨 ALERT] {severity} | {threat_type} | {log['user']} | {log['ip']}")
    insert_alert(
        timestamp=log['timestamp'],
        user=log['user'],
        ip=log['ip'],
        threat_type=threat_type,
        severity=severity,
        description=description,
        score=score
    )

def analyze_log(log):
    action    = log['action']
    ip        = log['ip']
    user      = log['user']
    timestamp = log['timestamp']

    # ─────────────────────────────────────────
    # RULE 1: Brute Force Detection
    # 2+ failed logins from same IP within 2 mins
    # ─────────────────────────────────────────
    if action == "LOGIN_FAILED":
        login_failures[ip].append(get_now())
        login_failures[ip] = clean_old_events(login_failures[ip], 120)

        count = len(login_failures[ip])
        if count >= 2:
            fire_alert(
                log,
                threat_type="BRUTE_FORCE",
                severity="HIGH",
                description=f"{count} failed login attempts from {ip} in 2 minutes",
                score=90
            )
        elif count >= 1:
            fire_alert(
                log,
                threat_type="SUSPICIOUS_LOGIN",
                severity="MEDIUM",
                description=f"Failed login attempt from {ip}",
                score=50
            )

    # ─────────────────────────────────────────
    # RULE 2: Port Scanning Detection
    # Any port scan activity = immediate HIGH alert
    # ─────────────────────────────────────────
    elif action == "PORT_SCAN":
        port_scans[ip].append(get_now())
        port_scans[ip] = clean_old_events(port_scans[ip], 60)

        fire_alert(
            log,
            threat_type="PORT_SCAN",
            severity="HIGH",
            description=f"Port scanning detected from {ip} — possible reconnaissance",
            score=85
        )

    # ─────────────────────────────────────────
    # RULE 3: Privilege Escalation
    # Always critical — immediate HIGH alert
    # ─────────────────────────────────────────
    elif action == "PRIVILEGE_ESCALATION":
        fire_alert(
            log,
            threat_type="PRIVILEGE_ESCALATION",
            severity="HIGH",
            description=f"User {user} attempted privilege escalation from {ip}",
            score=95
        )

    # ─────────────────────────────────────────
    # RULE 4: Mass File Deletion
    # 2+ file deletes by same IP within 2 mins
    # ─────────────────────────────────────────
    elif action == "FILE_DELETE":
        file_deletes[ip].append(get_now())        # ← tracking by IP now
        file_deletes[ip] = clean_old_events(file_deletes[ip], 120)

        count = len(file_deletes[ip])
        if count >= 2:
            fire_alert(
                log,
                threat_type="MASS_FILE_DELETION",
                severity="HIGH",
                description=f"IP {ip} deleted {count} files in 2 minutes — possible data destruction",
                score=88
            )
        elif count >= 1:
            fire_alert(
                log,
                threat_type="FILE_DELETION",
                severity="MEDIUM",
                description=f"File deletion detected from {ip}",
                score=55
            )

    # ─────────────────────────────────────────
    # RULE 5: Large Data Exfiltration
    # 2+ large downloads by same IP = insider threat
    # ─────────────────────────────────────────
    elif action == "LARGE_DOWNLOAD":
        large_downloads[ip].append(get_now())     # ← tracking by IP now
        large_downloads[ip] = clean_old_events(large_downloads[ip], 300)

        count = len(large_downloads[ip])
        if count >= 2:
            fire_alert(
                log,
                threat_type="DATA_EXFILTRATION",
                severity="HIGH",
                description=f"IP {ip} performed {count} large downloads in 5 minutes — possible data theft",
                score=92
            )
        else:
            fire_alert(
                log,
                threat_type="LARGE_DOWNLOAD",
                severity="MEDIUM",
                description=f"Large file download detected from {ip}",
                score=45
            )

    # ─────────────────────────────────────────
    # RULE 6: Known Malicious IP
    # Any action from a blacklisted IP
    # ─────────────────────────────────────────
    if ip in KNOWN_BAD_IPS:
        fire_alert(
            log,
            threat_type="KNOWN_MALICIOUS_IP",
            severity="HIGH",
            description=f"Activity from known malicious IP {ip} — action: {action}",
            score=95
        )

    # ─────────────────────────────────────────
    # RULE 7: After Hours Login
    # Successful login outside 8AM-8PM
    # ─────────────────────────────────────────
    if action == "LOGIN_SUCCESS" and is_after_hours(timestamp):
        fire_alert(
            log,
            threat_type="AFTER_HOURS_ACCESS",
            severity="MEDIUM",
            description=f"User {user} logged in after hours from {ip}",
            score=55
        )

if __name__ == "__main__":
    test_log = {
        'timestamp': '2026-07-02 03:00:00',
        'user': 'john',
        'action': 'LOGIN_FAILED',
        'ip': '45.33.32.156',
        'detail': 'attempt #5'
    }
    from database import init_db
    init_db()
    for i in range(3):
        analyze_log(test_log)