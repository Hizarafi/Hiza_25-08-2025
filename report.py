# report.py
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz

DB_NAME = "store_data.db"

def get_uptime_downtime(store_id: int, period: str = "1h"):
    """
    Calculate uptime and downtime for a store.
    period = '1h', '1d', or '1w'
    """
    conn = sqlite3.connect(DB_NAME)

    # Determine time window
    now = datetime.utcnow()
    if period == "1h":
        start_time = now - timedelta(hours=1)
    elif period == "1d":
        start_time = now - timedelta(days=1)
    elif period == "1w":
        start_time = now - timedelta(weeks=1)
    else:
        raise ValueError("Invalid period. Use '1h', '1d', or '1w'.")

    # Load store status data
    query = f"""
        SELECT store_id, timestamp_utc, status
        FROM store_status
        WHERE store_id = ? AND timestamp_utc >= ?
    """
    df = pd.read_sql_query(query, conn, params=(store_id, start_time))
    conn.close()

    if df.empty:
        return {"store_id": store_id, "uptime_minutes": 0, "downtime_minutes": 0}

    # Convert timestamp
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce")

    # Assume each row = 1 minute granularity (simplified)
    uptime = (df["status"] == "active").sum()
    downtime = (df["status"] == "inactive").sum()

    return {
        "store_id": store_id,
        "period": period,
        "uptime_minutes": int(uptime),
        "downtime_minutes": int(downtime)
    }
