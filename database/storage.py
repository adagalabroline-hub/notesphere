import json
from pathlib import Path

NOTES_FILE = Path("notes.json")


def load_notes():
    if not NOTES_FILE.exists():
        return []

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)