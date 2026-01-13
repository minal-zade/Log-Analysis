from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.models.schemas import LogEntry, LogStats
from app.services.file_handler import filter_logs, get_stats, find_log_by_id
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(BASE_DIR, "log_data")

@router.get("/logs", response_model=List[LogEntry])
def get_logs(
    level: Optional[str] = None,
    component: Optional[str] = None,
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    limit: int = 100,
    offset: int = 0
):
    try:
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else None
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    return filter_logs(
        LOG_DIR,
        level=level,
        component=component,
        start_time=start_dt,
        end_time=end_dt,
        limit=limit,
        offset=offset
    )

@router.get("/logs/stats", response_model=LogStats)
def get_log_stats():
    return get_stats(LOG_DIR)

@router.get("/logs/{log_id}", response_model=LogEntry)
def get_single_log(log_id: str):
    log = find_log_by_id(LOG_DIR, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log ID not found")
    return log
