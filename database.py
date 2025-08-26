import sqlite3
import pandas as pd

DB_FILE = "store_data.db"

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

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
    print("✅ Tables created successfully")

def load_data():
    conn = sqlite3.connect(DB_FILE)

    # Load CSVs into tables
    df_status = pd.read_csv("data/store_status.csv")
    df_status.to_sql("store_status", conn, if_exists="replace", index=False)

    df_hours = pd.read_csv("data/business_hours.csv")
    df_hours.to_sql("business_hours", conn, if_exists="replace", index=False)

    df_timezones = pd.read_csv("data/timezones.csv")
    df_timezones.to_sql("timezones", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("✅ Data loaded into SQLite DB")

if __name__ == "__main__":
    create_tables()
    load_data()
