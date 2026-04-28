import mysql.connector

# ── CHANGE THESE TO MATCH YOUR MYSQL SETUP ──
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "6570",   # <- put your MySQL root password
    "database": "parking_system"
}

def get_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Insert default slots only if table is empty
    cursor.execute("SELECT COUNT(*) FROM slots")
    count = cursor.fetchone()[0]

    if count == 0:
        slots = []
        for i in range(1, 11): slots.append((f"W{i:02d}", "2-Wheeler"))
        for i in range(1,  9): slots.append((f"F{i:02d}", "4-Wheeler"))
        for i in range(1,  5): slots.append((f"H{i:02d}", "Heavy Vehicle"))
        cursor.executemany("INSERT INTO slots (number, type) VALUES (%s, %s)", slots)
        conn.commit()
        print("✓ Default slots inserted")

    cursor.close()
    conn.close()
    print("✓ Database ready")