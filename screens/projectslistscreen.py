from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from uix.projectbutton import ProjectButton

class ProjectsListScreen(Screen):
  projects_grid = ObjectProperty(None)

  def update_projects_list(self):
    app = App.get_running_app()
    projects = app.get_projects_list()

    self.projects_grid.clear_widgets()
    for n in projects:
      p = ProjectButton(text=n)
      self.projects_grid.add_widget(p)
