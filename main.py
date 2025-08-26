from fastapi import FastAPI
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz


app = FastAPI(title="Store Monitoring API 🚀")

DB_PATH = "store_data.db"

# --- Root endpoint ---
@app.get("/")
def root():
    return {"message": "Welcome to the Store Monitoring API 🚀"}

#  Utility function to run SQL and return DataFrame ---
def query_db(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Endpoints to see raw tables (for debugging) ---
@app.get("/stores/status")
def get_store_status():
    return query_db("SELECT * FROM store_status LIMIT 50").to_dict(orient="records")

@app.get("/stores/hours")
def get_business_hours():
    return query_db("SELECT * FROM business_hours LIMIT 50").to_dict(orient="records")

@app.get("/stores/timezones")
def get_timezones():
    return query_db("SELECT * FROM timezones LIMIT 50").to_dict(orient="records")

#  (main assessment requirement)
@app.get("/report")
def generate_report():
    # Load all tables
    status = query_db("SELECT * FROM store_status")
    hours = query_db("SELECT * FROM business_hours")
    tz = query_db("SELECT * FROM timezones")

    # Convert timestamp to datetime
    status["timestamp_utc"] = pd.to_datetime(status["timestamp_utc"], utc=True)

    # Default timezone = UTC if missing
    tz_dict = tz.set_index("store_id")["timezone_str"].to_dict()

    now_utc = datetime.now(tz=pytz.UTC)

    results = []

    for store_id, group in status.groupby("store_id"):
        # Get store timezone
        store_tz = pytz.timezone(tz_dict.get(store_id, "UTC"))

        # Convert timestamps to local time
        group = group.copy()
        group["timestamp_local"] = group["timestamp_utc"].dt.tz_convert(store_tz)

        # Filter last 1 hour, 1 day, 1 week
        periods = {
            "uptime_last_hour": now_utc - timedelta(hours=1),
            "uptime_last_day": now_utc - timedelta(days=1),
            "uptime_last_week": now_utc - timedelta(weeks=1),
        }

        report_row = {"store_id": store_id}

        for label, start_time in periods.items():
            df_period = group[group["timestamp_utc"] >= start_time]

            if len(df_period) == 0:
                report_row[label] = None
            else:
                uptime = (df_period["status"] == "active").sum()
                total = len(df_period)
                uptime_percent = round((uptime / total) * 100, 2)
                report_row[label] = uptime_percent

        results.append(report_row)

    return {"report_generated_at": str(now_utc), "stores": results}
