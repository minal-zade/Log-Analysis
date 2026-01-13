📊 Log Analysis REST API (File-Based)

A FastAPI-based log analysis system that processes and analyzes large log files directly from disk, without using a database.
Designed to be memory-efficient, scalable, and production-structured.

🚀 Features

📁 File-based log processing (no database required)

🔄 Streaming log reader (handles large files efficiently)

🔍 Filter logs by:

Log level

Component

Time range

📄 Pagination support (limit & offset)

📊 Aggregated log statistics

🔎 Fetch a single log entry by UUID

📘 Auto-generated API docs (Swagger)

🏗 Project Structure
log_analysis_project/
├── app/
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── models/
│   │   └── schemas.py       # Pydantic schemas
│   ├── services/
│   │   └── file_handler.py  # Log parsing & processing logic
│   ├── main.py              # FastAPI app entry point
│   └── __init__.py
├── log_data/
│   └── server.log           # Log files (data source)
├── requirements.txt
└── README.md

🧾 Log File Format

Each log entry must be TAB-separated and follow this format:

TIMESTAMP<TAB>LEVEL<TAB>COMPONENT<TAB>MESSAGE<TAB>ID

Example
2025-05-01 09:00:07 INFO UserAuth User logged in successfully 3d6c1c7a-0c42-4d6f-9b91-7e9f91a2b2f4

Field Description
Field Description
TIMESTAMP YYYY-MM-DD HH:MM:SS
LEVEL INFO / WARNING / ERROR / DEBUG
COMPONENT System module name
MESSAGE Log message
ID UUID (v4 recommended)

⚙️ Installation & Setup
1️⃣ Clone / Extract Project
unzip log_analysis_project.zip
cd log_analysis_project

2️⃣ (Optional) Create Virtual Environment
python3 -m venv venv
source venv/bin/activate     # Linux / macOS
# venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
uvicorn app.main:app --reload

🌐 API Documentation

Once running, open:

http://127.0.0.1:8000/docs

This provides:

Interactive Swagger UI

Try-it-out support

Request/response schemas

🔌 API Endpoints
🔹 Get Logs
GET /logs

Query Parameters
Parameter Description
level Filter by log level
component Filter by component
start_time YYYY-MM-DD HH:MM:SS
end_time YYYY-MM-DD HH:MM:SS
limit Number of logs (default: 100)
offset Pagination offset

Example:

/logs?level=ERROR&limit=10

🔹 Get Log Statistics
GET /logs/stats

Sample Response
{
  "total_entries": 1200,
  "by_level": {
    "INFO": 400,
    "WARNING": 300,
    "ERROR": 300,
    "DEBUG": 200
  },
  "by_component": {
    "UserAuth": 250,
    "Payment": 200,
    "GeoIP": 150
  }
}

🔹 Get Log by ID
GET /logs/{log_id}

Returns 404 if the log is not found.

🧠 Architecture Decisions
Why No Database?

Logs are immutable

Avoids DB overhead

Faster ingestion

Easier deployment

Why Streaming?

Handles millions of lines

Low memory usage

Scales with file size

Why UUID?

Globally unique

Stateless lookup

No collision risk

🧪 Performance Considerations

Logs are processed line-by-line

Pagination stops reading early

Stats endpoint scans full dataset (expected behavior)

🔐 Error Handling

Malformed lines are skipped safely

Invalid timestamps return 400

Missing log IDs return 404

🛠 Future Enhancements

Async file streaming

Regex / keyword search

Log upload API

Caching for stats

Docker & CI/CD

Elasticsearch integration

📌 Tech Stack

FastAPI

Pydantic

Uvicorn

Python 3.9+

👨‍💻 Author Notes

This project demonstrates:

Clean backend architecture

Efficient file processing

Real-world API design

Production-ready code practices
