from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class LogEntry(BaseModel):
    id: str
    timestamp: datetime
    level: str
    component: str
    message: str

class LogStats(BaseModel):
    total_entries: int
    by_level: Dict[str, int]
    by_component: Dict[str, int]
