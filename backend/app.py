from flask import Flask, request, jsonify
import json
import hashlib
import os

app = Flask(__name__)

USERS_FILE = "users.json"
NOTES_FILE = "notes.json"


# ---------- HELPERS ---------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


# ---------- DATA ---------- #
users = load_json(USERS_FILE, {})
notes = load_json(NOTES_FILE, {})


# ---------- ROUTES ---------- #
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"status": "error", "message": "User exists"})

    users[email] = hash_password(password)
    save_json(USERS_FILE, users)

    return jsonify({"status": "success"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email in users and users[email] == hash_password(password):
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": "Invalid login"})


@app.route("/get_notes", methods=["POST"])
def get_notes():
    data = request.json
    email = data.get("email")

    return jsonify({"notes": notes.get(email, [])})


@app.route("/add_note", methods=["POST"])
def add_note():
    data = request.json
    email = data.get("email")
    note = data.get("note")

    user_notes = notes.get(email, [])
    user_notes.append(note)
    notes[email] = user_notes

    save_json(NOTES_FILE, notes)

    return jsonify({"status": "success"})


@app.route("/delete_note", methods=["POST"])
def delete_note():
    data = request.json
    email = data.get("email")
    index = data.get("index")

    user_notes = notes.get(email, [])

    if 0 <= index < len(user_notes):
        user_notes.pop(index)
        notes[email] = user_notes
        save_json(NOTES_FILE, notes)

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)