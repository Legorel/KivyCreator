import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import os

app = ""
root_path = os.getcwd()
projects_path = os.path.join(root_path, "projects")
projects = []

new_project_name = ""

py_code = ""
kv_code = ""

class ProjectScreen(Screen):
  def __init__(self, **kwargs):
    super(ProjectScreen, self).__init__(**kwargs)
    self.scroll = ScrollView(do_scroll_x=False);
    self.scroll.grid = GridLayout(size_hint=(1, 1.75), cols=1)
    self.scroll.add_widget(self.scroll.grid)
    self.scroll.grid.add = AddProjectButton(text="New project", size_hint_y=None)
    self.scroll.grid.add_widget(self.scroll.grid.add)
    self.add_widget(self.scroll);

  def on_enter(self):
    projects = [o for o in os.listdir(projects_path) if os.path.isdir(os.path.join(projects_path, o))]
    Logger.info("On enter called")
    for dir in projects:
      self.scroll.grid.add_widget(ProjectButton(text=dir))


class Manager(ScreenManager):
  def __init__(self, **kwargs):
    super(Manager, self).__init__(**kwargs)
    self.add_widget(ProjectScreen(name="ProjectS"))
    self.transition = NoTransition()
    self.switch_to(ProjectScreen())
    self.transition = SlideTransition()


class ProjectButton(Button):
  def __init__(self, **kwargs):
    super(ProjectButton, self).__init__(**kwargs)
    self.size_hint_y = None
    self.height = "50dp"

  def on_release(self):
    pass


class AddProjectButton(Button):
  def __init__(self, **kwargs):
    super(AddProjectButton, self).__init__(**kwargs)
    self.size_hint_y = None
    self.height = "50dp"

  def on_release(self):
    Factory.NewProjectPopup().open()


kv = Builder.load_string(
"""
#:import Factory kivy.factory.Factory
#:import Window kivy.core.window.Window
Manager:
    EditScreen:
        name: "EditS"

<ProjectScreen>:
    name: "ProjectS"

<EditScreen@Screen>:

<NewProjectPopup@Popup>:
    lay: lay
    title: "Project name:"
    size_hint: None, None
    size: Window.width / 2, Window.height / 3
    FloatLayout:
        id: lay
        edit: edit
        cols: 1
        TextInput:
            size_hint: 1, 0.15
            pos_hint: {"center_y":0.85, "center_x":0.5}
            id: edit
            multiline: False

        Button:
            size_hint: 0.60, .20
            pos_hint: {"center_y":0.20,"center_x":0.5}
            text: "Create"
            on_release:
                root.dismiss()
""")

class KivyCreator(App):
  def __init__(self, **kwargs):
    super(KivyCreator, self).__init__(**kwargs)

  def build(self):
    return kv;

  def on_start(self):
    app = App.get_running_app()
    if not os.path.exists("projects"):
      os.mkdir("projects")
    root_path = os.getcwd()
    projects_path = os.path.join(root_path, "projects")

  def on_resume(self):
    load_projects()

  def on_pause(self):
    return False

  def on_stop(self):
    pass

if __name__ == "__main__":
  KivyCreator().run()
