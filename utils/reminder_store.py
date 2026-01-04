import json
import os
from datetime import datetime

FILE = "data/reminder.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def can_send(group_id):
    data = load_data()
    today = datetime.utcnow().date().isoformat()
    gid = str(group_id)

    if gid not in data:
        data[gid] = {"date": today, "count": 0}

    if data[gid]["date"] != today:
        data[gid] = {"date": today, "count": 0}

    if data[gid]["count"] >= 2:
        return False

    data[gid]["count"] += 1
    save_data(data)
    return True

def clear(group_id):
    data = load_data()
    gid = str(group_id)
    if gid in data:
        del data[gid]
        save_data(data)
