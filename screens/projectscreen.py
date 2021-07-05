import os
from os import path

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class ProjectScreen(Screen):
  action_bar = ObjectProperty(None)
  project_grid = ObjectProperty(None)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.project_dir = ""
    self.project_list = []
    self.button_per_scroll = 4
    app = App.get_running_app()
    app.bind(on_config_change=lambda a, c, s, k, v: self.update_config(c, s, k, v))
    # Default value for when the app starts
    self.button_per_scroll = int(app.config.get("customization", "button_per_scroll"))

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
    if len(self.project_list) < self.button_per_scroll:
      self.project_grid.size_hint_y = 1
    else:
      hidden_buttons = len(self.project_list) - self.button_per_scroll
      amount = (hidden_buttons / self.button_per_scroll)
      self.project_grid.size_hint_y = 1 + amount
    # Move and go back to update the scrollview
    # There is probably a better way to do this
    scroll_y = self.project_grid.parent.scroll_y
    self.project_grid.parent.scroll_y = scroll_y + 1
    self.project_grid.parent.scroll_y = scroll_y

  def update_config(self, config, section, key, value):
    if section == "customization" and key == "button_per_scroll":
      self.button_per_scroll = int(value)
      self.update_project_buttons()

  def update_project_buttons(self):
    self.update_project_list()
    self.project_grid.clear_widgets()
    for project_name in self.project_list:
      # TODO: Add and use ProjectButton class
      self.project_grid.add_widget(Button(text=project_name))
    self.update_project_grid_size()

  def new_project_popup(self):
    popup = NewProjectPopup()
    popup.bind(on_dismiss=lambda p: self.new_project(p.project_name))
    popup.open()

  def new_project(self, new_project_name):
    if new_project_name is None:
      return
    self.update_project_dir()
    new_project_dir = path.join(self.project_dir, new_project_name)
    if path.exists(new_project_dir):
      # TODO: might want to add a warning popup
      return
    os.mkdir(new_project_dir)
    self.update_project_buttons()


class NewProjectPopup(Popup):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.project_name = None
