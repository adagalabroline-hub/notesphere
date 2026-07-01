from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import json
import os
import hashlib


USERS_FILE = "users.json"
NOTES_FILE = "notes.json"


# ---------------- HELPERS ---------------- #
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


# ---------------- DATA ---------------- #
users = load_json(USERS_FILE, {})
current_user = None


def load_user_notes(user):
    all_notes = load_json(NOTES_FILE, {})
    return all_notes.get(user, [])


def save_user_notes(user, notes):
    all_notes = load_json(NOTES_FILE, {})
    all_notes[user] = notes
    save_json(NOTES_FILE, all_notes)


# ---------------- LOGIN ---------------- #
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.email = MDTextField(hint_text="Email")
        self.password = MDTextField(hint_text="Password", password=True)

        login_btn = MDRaisedButton(text="Login", on_release=self.login)
        signup_btn = MDRaisedButton(text="Sign Up", on_release=self.signup)

        self.status = MDLabel(text="", halign="center")

        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(signup_btn)
        layout.add_widget(self.status)

        self.add_widget(layout)

    def signup(self, instance):
        email = self.email.text
        password = self.password.text

        if email and password:
            if email in users:
                self.status.text = "User exists"
            else:
                users[email] = hash_password(password)
                save_json(USERS_FILE, users)
                self.status.text = "Account created"

    def login(self, instance):
        global current_user

        email = self.email.text
        password = self.password.text

        if email in users and users[email] == hash_password(password):
            current_user = email
            self.manager.current = "notes"
        else:
            self.status.text = "Invalid login"


# ---------------- NOTES ---------------- #
class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.notes = []

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.input = MDTextField(hint_text="Write a note")

        add_btn = MDRaisedButton(text="Add Note", on_release=self.add_note)

        self.scroll = ScrollView()
        self.box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.box.bind(minimum_height=self.box.setter("height"))

        self.scroll.add_widget(self.box)

        self.layout.add_widget(self.input)
        self.layout.add_widget(add_btn)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        global current_user
        if current_user:
            self.notes = load_user_notes(current_user)
            self.refresh()

    def add_note(self, instance):
        global current_user

        if not current_user:
            return

        text = self.input.text

        if text:
            self.notes.append(text)
            save_user_notes(current_user, self.notes)
            self.input.text = ""
            self.refresh()

    def delete_note(self, index):
        self.notes.pop(index)
        save_user_notes(current_user, self.notes)
        self.refresh()

    def refresh(self):
        self.box.clear_widgets()

        for i, note in enumerate(self.notes):
            row = BoxLayout(size_hint_y=None, height=50)

            label = MDLabel(text=note)

            delete_btn = MDRaisedButton(
                text="X",
                size_hint_x=None,
                width=60,
                on_release=lambda x, i=i: self.delete_note(i)
            )

            row.add_widget(label)
            row.add_widget(delete_btn)
            self.box.add_widget(row)


# ---------------- APP ---------------- #
class NotesApp(MDApp):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(NotesScreen(name="notes"))

        sm.current = "login"
        return sm


NotesApp().run()