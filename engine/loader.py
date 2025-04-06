import json
from pathlib import Path

RULES_PATH = Path("data/audit_rules.json")
LOGS_DIR = Path("data/raw_logs")

def load_rules():
    with open(RULES_PATH) as f:
        return json.load(f)

def load_youth_logs():
    logs = []
    for log_path in LOGS_DIR.glob("*.json"):
        with open(log_path) as f:
            data = json.load(f)
            logs.append(data)
    return logs