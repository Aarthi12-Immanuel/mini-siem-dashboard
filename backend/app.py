from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db, get_all_logs, get_all_alerts, get_stats

app = Flask(__name__)
CORS(app)  # Allow React frontend to talk to Flask

# Initialize database on startup
init_db()

# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.route('/')
def home():
    return jsonify({"message": "Mini SIEM API is running ✅"})

@app.route('/api/logs', methods=['GET'])
def logs():
    data = get_all_logs(limit=100)
    return jsonify(data)

@app.route('/api/alerts', methods=['GET'])
def alerts():
    data = get_all_alerts(limit=100)
    return jsonify(data)

@app.route('/api/stats', methods=['GET'])
def stats():
    data = get_stats()
    return jsonify(data)

if __name__ == "__main__":
    print("[+] Starting Mini SIEM Flask API on http://localhost:5000")
    app.run(debug=True, port=5000)