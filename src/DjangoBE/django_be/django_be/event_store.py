import json

EVENT_LOG_FILE = "events.json"

def append_event(event):
    with open(EVENT_LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

def get_all_events():
    with open(EVENT_LOG_FILE, "r") as f:
        return [json.loads(line) for line in f]
