import os
from shutil import rmtree
import importlib
import threading

import kivy
from kivy.app import App
from kivy.uix.screenmanager import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.extras.highlight import KivyLexer
from kivy.lang import Builder
from kivy.logger import Logger

root_dir = os.path.abspath(os.getcwd())
layout_dir = os.path.join(root_dir, "layout")

py_code = None
kv_code = None
kc = None
run = False


class CodeButton(Button):
  def __init__(self, **kwargs):
    super(CodeButton, self).__init__(**kwargs)
    self.text = "py"
  
  def on_release(self):
    a = App.get_running_app()
    if self.text == "kv":
      a.root.code.main.manager.transition.direction = "right"
      a.root.code.main.manager.current = "py"
      self.text = "py"
      
    else:
      a.root.code.main.manager.transition.direction = "left"
      a.root.code.main.manager.current = "kv"
      self.text = "kv"


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
    except:
      pass
    m = App.get_running_app().root
    m.transition.direction = "left"
    m.current = "code"
    App.get_running_app().current_project = this_project_dir


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
      i = i + 0.1
    self.scroll.grid.size_hint = (1, i)


class CodeScreen(Screen):
  def __init__(self, **kwargs):
    super(CodeScreen, self).__init__(**kwargs)

  def on_pre_enter(self):
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
    self.kv_screen.input.lexer = KivyLexer()
    self.add_widget(self.kv_screen)


root = Builder.load_file(os.path.join(layout_dir, "main.kv"))


class KivyCreator(App):
  def __init__(self, *args):
    super(KivyCreator, self).__init__(*args)
    #self.kv_directory = layout_dir
    self.projects_dir = os.path.abspath(os.path.join(self.user_data_dir, "projects"))

    if not os.path.exists(self.projects_dir):
      os.mkdir(self.projects_dir)
    
    self.is_restart = False

  def build(self):
    return root

  def on_start(self):
    self.root.project.load(self.projects_dir)
    self.root.project.calc_scroll_size()
    
    if self.is_restart:
      self.is_restart = False
      self.root.current = "project"
      self.root.current = "code"

  def on_pause(self):
    return True

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
    
  def save_project_popup(self):
    p = Builder.load_file(os.path.join(layout_dir, "save_project_popup.kv"))
    p.open()

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

  def close_project(self):
    if self.root.code.main.manager.py_screen.input.text == py_code\
        and self.root.code.main.manager.kv_screen.input.text == kv_code:
      self.root.transition.direction = "right"
      self.root.current = "project"
    else:
      p = Builder.load_file(os.path.join(layout_dir, "close_project_popup.kv"))
      p.open()

  def save_project(self):
    global py_code
    global kv_code
    try:
      py_file = open(os.path.join(self.current_project, "main.py"), "w")
      kv_file = open(os.path.join(self.current_project, "main.kv"), "w")
      py_code = self.root.code.main.manager.py_screen.input.text
      kv_code = self.root.code.main.manager.kv_screen.input.text
      py_file.write(py_code)
      kv_file.write(kv_code)
      py_file.close()
      kv_file.close()
    except:
      Logger.info("whoops")

  def check_code(self):
    if self.root.code.main.manager.py_screen.input.text != py_code or self.root.code.main.manager.kv_screen.input.text != kv_code:
      p = Builder.load_file(os.path.join(layout_dir, "check_project_popup.kv"))
      p.open()
    else:
      self.run_code()

  def run_code(self):
    global kc
    global run
    run = True
    kc.stop()
    

class second(App):
  def build(self):
    return Button(text="yey", on_press=lambda s: self.stop())

def start(restart):
  global kc
  global run
  os.chdir(root_dir)
  kc = KivyCreator()
  kc.run()
  # class attributes will not reliad if
  # the screen doesn't change by the user's
  # inputs
  kc.root.transition.direction = "right"
  kc.root.current = "project"
  if run:
    run = False
    kc.stop()
    os.chdir(kc.current_project)
    try:
      exec(open("main.py", "r").read())
    except:
      pass
    start(True)
    

if __name__ == "__main__":
  start(False)