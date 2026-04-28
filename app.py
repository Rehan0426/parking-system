from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db, init_db
from datetime import datetime
import math

app = Flask(__name__)
CORS(app)

RATES = {"2-Wheeler": 20, "4-Wheeler": 50, "Heavy Vehicle": 100}

# ── helper: convert cursor rows to list of dicts ──
def rows_to_dict(cursor, rows):
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in rows]

def row_to_dict(cursor, row):
    if row is None: return None
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, row))

def fmt(dt):
    if dt is None: return None
    if isinstance(dt, str): return dt
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

@app.route("/")
def home():
    return "Parking System API is running!"

# ── GET all slots ──
@app.route("/slots", methods=["GET"])
def get_slots():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM slots")
    slots = rows_to_dict(cur, cur.fetchall())
    cur.close(); conn.close()
    return jsonify(slots)

# ── POST vehicle entry ──
@app.route("/entry", methods=["POST"])
def vehicle_entry():
    data = request.json
    plate = data["plate"].upper()
    vtype = data["type"]

    conn = get_db()
    cur = conn.cursor()

    # Check already parked
    cur.execute("SELECT id FROM records WHERE plate=%s AND exit_time IS NULL", (plate,))
    if cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"error": "Vehicle already parked"}), 400

    # Find free slot
    cur.execute("SELECT * FROM slots WHERE type=%s AND status='Available' LIMIT 1", (vtype,))
    slot = row_to_dict(cur, cur.fetchone())
    if not slot:
        cur.close(); conn.close()
        return jsonify({"error": f"No {vtype} slots available"}), 400

    # Insert record
    cur.execute("""
        INSERT INTO records (plate, slot_id, slot_number, type, owner, phone, entry_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (plate, slot["id"], slot["number"], vtype,
          data.get("owner", "Walk-in"), data.get("phone", ""), datetime.now()))

    # Mark slot occupied
    cur.execute("UPDATE slots SET status='Occupied' WHERE id=%s", (slot["id"],))
    conn.commit()
    cur.close(); conn.close()

    return jsonify({"message": f"{plate} parked at Slot {slot['number']}"})

# ── POST vehicle exit ──
@app.route("/exit/<int:record_id>", methods=["POST"])
def vehicle_exit(record_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM records WHERE id=%s", (record_id,))
    rec = row_to_dict(cur, cur.fetchone())
    if not rec:
        cur.close(); conn.close()
        return jsonify({"error": "Record not found"}), 404

    exit_time  = datetime.now()
    entry_time = rec["entry_time"] if isinstance(rec["entry_time"], datetime) else datetime.fromisoformat(str(rec["entry_time"]))
    hours  = max(1, math.ceil((exit_time - entry_time).total_seconds() / 3600))
    amount = hours * RATES[rec["type"]]

    # Update record
    cur.execute("UPDATE records SET exit_time=%s, hours=%s, amount=%s WHERE id=%s",
                (exit_time, hours, amount, record_id))

    # Free the slot
    cur.execute("UPDATE slots SET status='Available' WHERE id=%s", (rec["slot_id"],))

    # Insert payment
    cur.execute("INSERT INTO payments (record_id, plate, amount, method, time) VALUES (%s,%s,%s,%s,%s)",
                (record_id, rec["plate"], amount, data.get("method", "Cash"), exit_time))

    conn.commit()
    cur.close(); conn.close()

    return jsonify({"amount": amount, "hours": hours})

# ── GET all records ──
@app.route("/records", methods=["GET"])
def get_records():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM records ORDER BY id DESC")
    records = rows_to_dict(cur, cur.fetchall())
    # Convert datetime to string for JSON
    for r in records:
        r["entry_time"] = fmt(r.get("entry_time"))
        r["exit_time"]  = fmt(r.get("exit_time"))
    cur.close(); conn.close()
    return jsonify(records)

# ── GET all payments ──
@app.route("/payments", methods=["GET"])
def get_payments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments ORDER BY id DESC")
    payments = rows_to_dict(cur, cur.fetchall())
    for p in payments:
        p["time"] = fmt(p.get("time"))
    cur.close(); conn.close()
    return jsonify(payments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)