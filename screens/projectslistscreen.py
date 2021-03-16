from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from uix.projectitem import ProjectItem
from uix.popups import NewProjectPopup

class ProjectsListScreen(Screen):
  projects_grid = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(ProjectsListScreen, self).__init__(**kwargs)
    self.button_per_scroll = 3

  def update_projects_list(self):

    app = App.get_running_app()
    projects = app.get_projects_list()

    self.projects_grid.clear_widgets()
    for n in projects:
      p = ProjectItem(project_name=n)
      self.projects_grid.add_widget(p)
    self.update_scroll_size()

  def update_scroll_size(self):
    # button_per_scroll = maximum buttons visible without scrolling
    # TODO: add button_per_scroll to config
    n = len(self.projects_grid.children) / self.button_per_scroll
    n = 1 if n<1 else n

    self.projects_grid.size_hint_y = n
    # The top button gets cut-off when adding a new one
    # so we force update the scrollview
    self.projects_grid.parent.update_from_scroll()

  @staticmethod
  def new_project():
    NewProjectPopup().open()