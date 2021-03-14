from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class ProjectButton(Button):
  def on_release_callback(self):
    App.get_running_app().open_project(self.text)
