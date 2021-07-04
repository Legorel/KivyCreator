from kivy.uix.screenmanager import ScreenManager

from screens.projectscreen import ProjectScreen


class KCScreenManager(ScreenManager):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add_widget(ProjectScreen(name="projects_screen"))
