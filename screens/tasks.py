from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class TasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="Tasks Screen", font_size=28))

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_home)

        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = "home"