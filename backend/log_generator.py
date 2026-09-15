import random
import time
from datetime import datetime
from faker import Faker
import os

fake = Faker()

# Simulated users and IPs
USERS = ["alice", "bob", "john", "admin", "root", "sarah", "mike"]
INTERNAL_IPS = ["192.168.1." + str(i) for i in range(1, 20)]
ATTACKER_IPS = ["45.33.32.156", "103.21.244.0", "185.220.101.5", "10.0.0.99"]

ACTIONS = [
    "LOGIN_SUCCESS",
    "LOGIN_FAILED",
    "FILE_ACCESS",
    "FILE_DELETE",
    "LARGE_DOWNLOAD",
    "PORT_SCAN",
    "CONFIG_CHANGE",
    "PRIVILEGE_ESCALATION"
]

# Weights — most logs are normal, few are suspicious
ACTION_WEIGHTS = [30, 25, 20, 5, 5, 5, 5, 5]

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'system_logs.txt')

def generate_log():
    action = random.choices(ACTIONS, weights=ACTION_WEIGHTS, k=1)[0]
    user = random.choice(USERS)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Suspicious actions use attacker IPs sometimes
    if action in ["PORT_SCAN", "PRIVILEGE_ESCALATION", "LOGIN_FAILED"]:
        ip = random.choice(ATTACKER_IPS + INTERNAL_IPS)
    else:
        ip = random.choice(INTERNAL_IPS)

    # Extra detail based on action
    detail = ""
    if action == "FILE_ACCESS":
        detail = f"file://{fake.file_path()}"
    elif action == "LARGE_DOWNLOAD":
        detail = f"{random.randint(500, 5000)}MB downloaded"
    elif action == "PORT_SCAN":
        detail = f"ports scanned: {random.randint(10,100)}"
    elif action == "LOGIN_FAILED":
        detail = f"attempt #{random.randint(1,10)}"

    log_line = f"{timestamp} | user:{user} | action:{action} | ip:{ip} | detail:{detail}\n"
    return log_line

def run_generator(interval=1, count=100):
    """Generate `count` logs with `interval` seconds between each"""
    print(f"[+] Starting log generation → {LOG_FILE}")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, 'a') as f:
        for i in range(count):
            log = generate_log()
            f.write(log)
            print(log.strip())
            time.sleep(interval)

    print("[+] Log generation complete!")

if __name__ == "__main__":
    run_generator(interval=0.5, count=100)