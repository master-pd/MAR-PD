import json

files = [
    "data/default.json",
    "data/extra.json",
    "data/quotes.json",
    "data/duas.json",
    "data/media.json",
    "data/events.json",
    "data/announcements.json",
    "data/hacking.json"
]

for f in files:
    try:
        with open(f, "r", encoding="utf-8") as file:
            json.load(file)
        print(f"[OK] {f}")
    except Exception as e:
        print(f"[ERROR] {f} -> {e}")
