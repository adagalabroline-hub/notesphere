from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from database.storage import load_notes, save_notes


class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.edit_index = None

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title_input = TextInput(
            hint_text="Note title",
            size_hint_y=None,
            height=40
        )

        self.content_input = TextInput(
            hint_text="Write your note...",
            multiline=True
        )

        self.save_btn = Button(text="Save Note", size_hint_y=None, height=50)
        self.save_btn.bind(on_press=self.save_note)

        self.status = Label(size_hint_y=None, height=30)

        self.notes_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5
        )
        self.notes_container.bind(minimum_height=self.notes_container.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.notes_container)

        self.layout.add_widget(self.title_input)
        self.layout.add_widget(self.content_input)
        self.layout.add_widget(self.save_btn)
        self.layout.add_widget(self.status)
        self.layout.add_widget(scroll)

        self.add_widget(self.layout)

        self.refresh_notes()

    def save_note(self, instance):
        notes = load_notes()

        data = {
            "title": self.title_input.text,
            "content": self.content_input.text
        }

        if self.edit_index is None:
            notes.append(data)
            self.status.text = "Note added!"
        else:
            notes[self.edit_index] = data
            self.status.text = "Note updated!"
            self.edit_index = None
            self.save_btn.text = "Save Note"

        save_notes(notes)

        self.title_input.text = ""
        self.content_input.text = ""

        self.refresh_notes()

    def delete_note(self, index):
        notes = load_notes()
        notes.pop(index)
        save_notes(notes)
        self.refresh_notes()

    def load_note_for_edit(self, index):
        notes = load_notes()
        note = notes[index]

        self.title_input.text = note["title"]
        self.content_input.text = note["content"]

        self.edit_index = index
        self.save_btn.text = "Update Note"

    def refresh_notes(self):
        self.notes_container.clear_widgets()

        notes = load_notes()

        for i, note in enumerate(notes):
            row = BoxLayout(size_hint_y=None, height=80)

            text = Label(text=f"{note['title']}\n{note['content']}")

            edit_btn = Button(text="Edit", size_hint_x=None, width=80)
            edit_btn.bind(on_press=lambda x, idx=i: self.load_note_for_edit(idx))

            del_btn = Button(text="Delete", size_hint_x=None, width=80)
            del_btn.bind(on_press=lambda x, idx=i: self.delete_note(idx))

            row.add_widget(text)
            row.add_widget(edit_btn)
            row.add_widget(del_btn)

            self.notes_container.add_widget(row)