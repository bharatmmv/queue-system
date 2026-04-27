from flask import Flask, render_template, request, jsonify
import sqlite3
import qrcode
from datetime import datetime
from model import predict_crowd

app = Flask(__name__)

# ---------------- DB ----------------
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        service TEXT,
        token INTEGER,
        status TEXT,
        time TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- QR ----------------
@app.route("/generate_qr")
def generate_qr():
    url = "http://127.0.0.1:5000/"
    img = qrcode.make(url)
    img.save("qr/entry_qr.png")
    return "QR Generated!"

# ---------------- UI ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

# ---------------- Join Queue ----------------
@app.route("/join", methods=["POST"])
def join_queue():
    data = request.json
    name = data["name"]
    service = data["service"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM queue WHERE status='waiting'")
    position = cur.fetchone()[0]

    token = position + 1
    wait_time = position * 10  # simple logic

    cur.execute("INSERT INTO queue(name, service, token, status, time) VALUES(?,?,?,?,?)",
                (name, service, token, "waiting", str(datetime.now())))

    conn.commit()
    conn.close()

    return jsonify({
        "token": token,
        "position": position,
        "wait_time": wait_time
    })

# ---------------- View Queue ----------------
@app.route("/queue")
def get_queue():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM queue WHERE status='waiting'")
    rows = cur.fetchall()

    conn.close()
    return jsonify(rows)

# ---------------- Next Customer ----------------
@app.route("/next", methods=["POST"])
def next_customer():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE queue SET status='done' WHERE id = (SELECT id FROM queue WHERE status='waiting' LIMIT 1)")
    conn.commit()
    conn.close()

    return "Next customer called"

# ---------------- Prediction ----------------
@app.route("/predict")
def predict():
    result = predict_crowd()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)