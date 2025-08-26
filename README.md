# Hiza_25-08-2025
Store Monitoring API 🚀

A FastAPI backend to monitor store uptime and downtime using store status, business hours, and timezone data. This project provides API endpoints to fetch store information and generate reports.

Features ✨
/ → Welcome message
/stores/status → View store status data (open/closed)
/stores/hours → View business hours for each store
/stores/timezones → View store timezones
/report → Generate uptime/downtime report


Tech Stack 🛠️
Python 3.x
FastAPI – Web framework for APIs
SQLite – Database for storing store data
Pandas – Data processing
Uvicorn – ASGI server for running FastAP

Install dependencies
pip install -r requirements.txt

Run the API
uvicorn main:app --reload

Access endpoints
Open http://127.0.0.1:8000/docs
 to explore the API with Swagger UI.
