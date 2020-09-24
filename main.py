import os
from shutil import rmtree

import kivy
from kivy.app import App
from kivy.uix.screenmanager import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.logger import Logger


root_dir = os.path.abspath(os.getcwd())
layout_dir = os.path.join(root_dir, "layout")

py_code = None
kv_code = None


class ProjectButton(Button):
  def _init__(self, **kwargs):
    super(ProjectButton, self).__init__(**kwargs)
  
  def on_release(self):
    global py_code
    global kv_code
    app = App.get_running_app()
    this_project_dir = os.path.join(app.projects_dir, self.text)
    try:
      py_file = open(os.path.join(this_project_dir, "main.py"), "r")
      kv_file = open(os.path.join(this_project_dir, "main.kv"), "r")
      py_code = py_file.read()
      py_file.close()
      kv_code = kv_file.read()
      kv_file.close()
      Logger.info("IMPORTANT: {}\n{}".format(py_code, kv_code))
    except:
      Logger.info("IMPORTANT:it failed :(")
    m = App.get_running_app().root
    m.transition.direction = "left"
    m.current = "code"



class ProjectScreen(Screen):
  def __init__(self, **kwargs):
    super(ProjectScreen, self).__init__(**kwargs)
    self.projects = []

  def load(self, dir):
    if not os.path.exists(dir): return
    self.scroll.grid.projects.clear_widgets()
    self.projects = [n for n in os.listdir(dir) if os.path.isdir(os.path.join(dir, n))]
    for i in self.projects:
      self.scroll.grid.projects.add_widget(ProjectButton(text=i))

  def calc_scroll_size(self):
    i = 0.9 - self.scroll.grid.button.size_hint_y
    for _ in self.scroll.grid.projects.children:
      i = i+0.1
    self.scroll.grid.size_hint = (1, i)

class CodeScreen(Screen):
  def __init__(self, **kwargs):
    super(CodeScreen, self).__init__(**kwargs)
  
  def on_pre_enter(self):
    Logger.info("IMPORTANT: entered")
    self.main.manager.screens[0].input.text = py_code
    self.main.manager.screens[1].input.text = kv_code

class BaseCodeScreen(Screen):
  def __init__(self, **kwargs):
    super(BaseCodeScreen, self).__init__(**kwargs)
    self.input = CodeInput()
    self.add_widget(self.input)

class MainManager(ScreenManager):
  def __init__(self, **kwargs):
    super(MainManager, self).__init__(**kwargs)
    self.project = ProjectScreen(name="project")
    self.add_widget(self.project)
    self.code = CodeScreen(name="code")
    self.add_widget(self.code)

class CodeManager(ScreenManager):
  def __init__(self, **kwargs):
    super(CodeManager, self).__init__(**kwargs)
    self.py_screen = BaseCodeScreen(name="py")
    self.add_widget(self.py_screen)
    self.kv_screen = BaseCodeScreen(name="kv")
    self.add_widget(self.kv_screen)


root = Builder.load_file(os.path.join(layout_dir, "main.kv"))

class KivyCreator(App):
  def __init__(self, *args):
    super(KivyCreator, self).__init__(*args)
    self.kv_directory = layout_dir
    self.projects_dir = os.path.abspath(os.path.join(self.user_data_dir, "projects"))

    if not os.path.exists(self.projects_dir):
      os.mkdir(self.projects_dir)

  def build(self):
    return root

  def on_start(self):
    self.root.project.load(self.projects_dir)
    self.root.project.calc_scroll_size()
  def on_pause(self):
    return False
  def on_resume(self):
    self.root.project.load(self.projects_dir)
    self.root.project.calc_scroll_size()
  def on_stop(self):
    pass

  def new_project_popup(self):
    popup = Popup(title="Enter a name",
        content=Builder.load_file(os.path.join(layout_dir, "new_project_popup.kv")),
        size_hint=(0.8, 0.2))
    popup.open()

  def new_project(self, name):
    p = os.path.join(self.projects_dir, name)

    popup = Popup(title="Invalid name",
          content=Label(text="A project already have that name"),
          size_hint=(0.8, 0.15))

    if os.path.exists(p):
      popup.open()
      return

    try:
      os.mkdir(p)
      open(os.path.join(p, "main.py"), "a").close()
      open(os.path.join(p, "main.kv"), "a").close()
      self.root.project.load(self.projects_dir)
      self.root.project.calc_scroll_size()
    except:
      if os.path.exists(p):
        rmtree(p)

      popup = Popup(title="Oops",
          content=Label(text="Something went wrong"),
          size_hint=(0.8, 0.15))
      popup.open()
  
if __name__ == "__main__":
  KivyCreator().run()
