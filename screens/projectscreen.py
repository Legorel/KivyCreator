import os
from os import path
from shutil import rmtree

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from buttons.projectbutton import ProjectButton
from popups.confirmpopup import ConfirmPopup
from popups.textinputpopup import TextInputPopup
from popups.optionselectpopup import OptionSelectPopup


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

  def add_project_button(self, project_name):
    button = ProjectButton(text=project_name)
    button.bind(on_project_released=lambda b: self.open_project(b.project_name))
    button.bind(on_project_settings_released=lambda b: self.open_project_settings(b.project_name))
    self.project_grid.add_widget(button)

  def update_project_buttons(self):
    self.update_project_list()
    self.project_grid.clear_widgets()
    for project_name in self.project_list:
      # TODO: Add and use ProjectButton class
      self.add_project_button(project_name)
    self.update_project_grid_size()

  def new_project_popup(self):
    popup = TextInputPopup("Create a new project")
    popup.bind(on_dismiss=lambda p: self.new_project(p.input))
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

  def open_project(self, project_name):
    pass

  def rename_project_popup(self, old_project_name):
    popup = TextInputPopup("Enter a new name")
    popup.bind(on_dismiss=lambda p: self.rename_project(old_project_name, p.input))
    popup.open()

  def rename_project(self, old_project_name, new_project_name):
    if new_project_name == "":
      return
    project_path = path.join(self.project_dir, old_project_name)
    if path.isdir(project_path):
      os.rename(project_path, path.join(self.project_dir, new_project_name))
    self.update_project_buttons()

  def delete_project_popup(self, project_name):
    popup = ConfirmPopup(f"Delete project '{project_name}' ?", "This action is irreversible")
    popup.bind(on_dismiss=lambda p: self.delete_project(project_name) if p.result else None)
    popup.open()

  def delete_project(self, project_name):
    project_path = path.join(self.project_dir, project_name)
    if path.isdir(project_path):
      rmtree(project_path)
    self.update_project_buttons()

  def open_project_settings(self, project_name):
    popup = OptionSelectPopup(project_name)
    popup.add_options(["Open", "Rename", "Delete"])
    popup.bind_to_option("Open", lambda o: self.open_project(project_name))
    popup.bind_to_option("Rename", lambda o: self.rename_project_popup(project_name))
    popup.bind_to_option("Delete", lambda o: self.delete_project_popup(project_name))
    popup.open()
