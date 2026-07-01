from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeScreen
from screens.notes import NotesScreen
from screens.tasks import TasksScreen
from screens.diary import DiaryScreen
from screens.settings import SettingsScreen


class NoteSphereApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NotesScreen(name="notes"))
        sm.add_widget(TasksScreen(name="tasks"))
        sm.add_widget(DiaryScreen(name="diary"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm


if __name__ == "__main__":
    NoteSphereApp().run()