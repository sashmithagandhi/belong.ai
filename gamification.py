import json
import os
from datetime import datetime, date

BADGES = {
    "first_entry": {
        "name": "First Step",
        "emoji": "🌱",
        "description": "Wrote your first diary entry",
        "requirement": 1
    },
    "three_day_streak": {
        "name": "Consistent Soul",
        "emoji": "🔥",
        "description": "Journaled 3 days in a row",
        "requirement": 3
    },
    "seven_day_streak": {
        "name": "Weekly Warrior",
        "emoji": "⚡",
        "description": "Journaled 7 days in a row",
        "requirement": 7
    },
    "thirty_day_streak": {
        "name": "Emotional Champion",
        "emoji": "👑",
        "description": "Journaled 30 days in a row",
        "requirement": 30
    },
    "ten_entries": {
        "name": "Deep Diver",
        "emoji": "🌊",
        "description": "Wrote 10 diary entries",
        "requirement": 10
    },
    "fifty_entries": {
        "name": "Soul Writer",
        "emoji": "✍️",
        "description": "Wrote 50 diary entries",
        "requirement": 50
    },
    "emotional_explorer": {
        "name": "Emotional Explorer",
        "emoji": "🧭",
        "description": "Experienced 5 different emotional states",
        "requirement": 5
    }
}

DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "entries": [],
        "streak": 0,
        "last_entry_date": None,
        "badges": [],
        "emotions_experienced": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_streak(data):
    today = str(date.today())
    last = data.get("last_entry_date")

    if last is None:
        data["streak"] = 1
    elif last == today:
        pass  # Already logged today
    elif (date.today() - date.fromisoformat(last)).days == 1:
        data["streak"] += 1
    else:
        data["streak"] = 1

    data["last_entry_date"] = today
    return data

def check_badges(data):
    newly_earned = []
    total_entries = len(data["entries"])
    streak = data["streak"]
    unique_emotions = len(set(data["emotions_experienced"]))

    badge_checks = {
        "first_entry": total_entries >= 1,
        "three_day_streak": streak >= 3,
        "seven_day_streak": streak >= 7,
        "thirty_day_streak": streak >= 30,
        "ten_entries": total_entries >= 10,
        "fifty_entries": total_entries >= 50,
        "emotional_explorer": unique_emotions >= 5
    }

    for badge_id, condition in badge_checks.items():
        if condition and badge_id not in data["badges"]:
            data["badges"].append(badge_id)
            newly_earned.append(badge_id)

    return data, newly_earned

def add_entry(emotion, entry_text):
    data = load_data()
    data = update_streak(data)

    data["entries"].append({
        "date": str(date.today()),
        "emotion": emotion,
        "text": entry_text[:100]
    })

    if emotion not in data["emotions_experienced"]:
        data["emotions_experienced"].append(emotion)

    data, newly_earned = check_badges(data)
    save_data(data)
    return data, newly_earned
    