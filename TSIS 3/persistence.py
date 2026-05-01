import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_json(path, default_value):
    if not os.path.exists(path):
        save_json(path, default_value)
        return default_value.copy() if isinstance(default_value, dict) else list(default_value)

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default_value.copy() if isinstance(default_value, dict) else list(default_value)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])
    if not isinstance(data, list):
        return []
    return data


def save_score(name, score, distance, coins):
    leaderboard = load_leaderboard()
    leaderboard.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })
    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]
    save_json(LEADERBOARD_FILE, leaderboard)


def save_leaderboard(leaderboard):
    leaderboard.sort(key=lambda item: item.get("score", 0), reverse=True)
    save_json(LEADERBOARD_FILE, leaderboard[:10])
