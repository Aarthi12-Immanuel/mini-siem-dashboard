import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'siem.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table for raw logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            ip TEXT,
            detail TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for alerts (threats detected)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            ip TEXT,
            threat_type TEXT,
            severity TEXT,
            description TEXT,
            score INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("[+] Database initialized successfully")

def insert_log(timestamp, user, action, ip, detail):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, user, action, ip, detail)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, user, action, ip, detail))
    conn.commit()
    conn.close()

def insert_alert(timestamp, user, ip, threat_type, severity, description, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (timestamp, user, ip, threat_type, severity, description, score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, user, ip, threat_type, severity, description, score))
    conn.commit()
    conn.close()

def get_all_logs(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_alerts(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM logs')
    total_logs = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM alerts')
    total_alerts = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM alerts WHERE severity='HIGH'")
    high_alerts = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM alerts WHERE severity='MEDIUM'")
    medium_alerts = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM alerts WHERE severity='LOW'")
    low_alerts = cursor.fetchone()['total']

    conn.close()
    return {
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts
    }

if __name__ == "__main__":
    init_db()