import sqlite3

# connect to (or create) database file
conn = sqlite3.connect("store_data.db")
cursor = conn.cursor()

# create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS store_status (
    store_id INTEGER,
    timestamp_utc TEXT,
    status TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS business_hours (
    store_id INTEGER,
    day_of_week INTEGER,
    start_time_local TEXT,
    end_time_local TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS timezones (
    store_id INTEGER,
    timezone_str TEXT
);
""")

conn.commit()
conn.close()
