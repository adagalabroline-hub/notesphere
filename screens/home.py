from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="NoteSphere Home", font_size=32))

        btn = Button(text="Go to Notes")
        btn.bind(on_press=lambda x: self.switch_to_notes())

        layout.add_widget(btn)

        self.add_widget(layout)

    def switch_to_notes(self):
        self.manager.current = "notes"