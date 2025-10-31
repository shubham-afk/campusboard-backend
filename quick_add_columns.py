# quick_add_columns.py
# Run: python quick_add_columns.py
import sqlite3

conn = sqlite3.connect("campusboard.db")
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE notices ADD COLUMN claim_requested_by TEXT")
    print("Added claim_requested_by")
except Exception as e:
    print("claim_requested_by likely already exists:", e)
try:
    # SQLite does not allow adding NOT NULL with default easily; keep simple
    cur.execute("ALTER TABLE notices ADD COLUMN claim_status TEXT DEFAULT 'none'")
    print("Added claim_status")
except Exception as e:
    print("claim_status likely already exists:", e)
conn.commit()
conn.close()
