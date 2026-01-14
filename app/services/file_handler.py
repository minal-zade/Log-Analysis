import os
import glob
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Generator, Dict

def parse_line(line: str, line_index: int, file_name: str) -> Optional[dict]:
    parts = line.strip().split('\t')
    if len(parts) != 5:
        logging.warning(f"Malformed line in {file_name} at line {line_index + 1}: {line.strip()}")
        return None

    ts_str, level, component, message, log_id = parts
    try:
        timestamp = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logging.warning(f"Invalid timestamp in {file_name} at line {line_index + 1}: {ts_str}")
        return None

    return {
        "id": log_id,
        "timestamp": timestamp,
        "level": level,
        "component": component,
        "message": message
    }

def stream_logs(log_dir: str) -> Generator[dict, None, None]:
    if not os.path.exists(log_dir):
        logging.error(f"Log directory does not exist: {log_dir}")
        return

    log_files = glob.glob(os.path.join(log_dir, "*"))

    for file_path in log_files:
        if os.path.isdir(file_path):
            continue

        file_name = os.path.basename(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    parsed = parse_line(line, i, file_name)
                    if parsed:
                        yield parsed
        except Exception as e:
            logging.error(f"Failed to read file {file_name}: {e}")
            continue

def filter_logs(
    log_dir: str,
    level: Optional[str] = None,
    component: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
) -> List[dict]:
    
    results = []
    skipped_count = 0
    for log in stream_logs(log_dir):
        if level and log['level'].lower() != level.lower():
            continue
        if component and log['component'].lower() != component.lower():
            continue
        if start_time and log['timestamp'] < start_time:
            continue
        if end_time and log['timestamp'] > end_time:
            continue

        if skipped_count < offset:
            skipped_count += 1
            continue
        
        results.append(log)
        
        if len(results) >= limit:
            break
    return results

def get_stats(log_dir: str) -> Dict:
    total = 0
    by_level = {}
    by_component = {}
    
    for log in stream_logs(log_dir):
        total += 1
        
        lvl = log['level']
        by_level[lvl] = by_level.get(lvl, 0) + 1
        
        comp = log['component']
        by_component[comp] = by_component.get(comp, 0) + 1
        
    return {
        "total_entries": total,
        "by_level": by_level,
        "by_component": by_component
    }

def find_log_by_id(log_dir: str, target_id: str) -> Optional[dict]:
    for log in stream_logs(log_dir):
        if log['id'] == target_id:
            return log
    return None
