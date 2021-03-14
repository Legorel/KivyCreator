from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from uix.projectitem import ProjectItem

class ProjectsListScreen(Screen):
  projects_grid = ObjectProperty(None)
  button_per_scroll = 3

  def update_projects_list(self):
    app = App.get_running_app()
    projects = app.get_projects_list()

    self.projects_grid.clear_widgets()
    for n in projects:
      p = ProjectItem(project_name=n)
      self.projects_grid.add_widget(p)
    self.update_scroll_size()

  def update_scroll_size(self):
    # button_per_scroll = maximum buttons are visible without scrolling
    # TODO: add button_per_scroll to config
    n = len(self.projects_grid.children) / self.button_per_scroll
    n = 1 if n<1 else n

    self.projects_grid.size_hint_y = n