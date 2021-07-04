import os
from os import path

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class ProjectScreen(Screen):
  action_bar = ObjectProperty(None)
  project_grid = ObjectProperty(None)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.project_dir = ""
    self.project_list = []
    self.max_button_per_scroll = 4

  def on_enter(self, *args):
    self.update_project_buttons()

  def update_project_dir(self):
    app = App.get_running_app()
    if app is not None:
      self.project_dir = path.join(app.user_data_dir, "projects")
      if not path.exists(self.project_dir):
        os.mkdir(self.project_dir)

  def update_project_list(self):
    self.update_project_dir()
    self.project_list.clear()
    for name in os.listdir(self.project_dir):
      if path.isdir(path.join(self.project_dir, name)):
        self.project_list.append(name)

  def update_project_grid_size(self):
    if len(self.project_list) < self.max_button_per_scroll:
      self.project_grid.size_hint_y = 1
    else:
      hidden_buttons = len(self.project_list) - self.max_button_per_scroll
      self.project_grid.size_hint_y = 1 + (hidden_buttons/self.max_button_per_scroll)

  def update_project_buttons(self):
    self.update_project_list()
    self.project_grid.clear_widgets()
    for project_name in self.project_list:
      # TODO: Add and use ProjectButton class
      self.project_grid.add_widget(Button(text=project_name))
    self.update_project_grid_size()
