import os
from os import path
from os.path import abspath

import kivy

kivy.require("1.11.1")
from kivy.app import App
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.lang import Builder

from project import Project


def info(text):
  Logger.info(text)


class KivyCreator(App):
  def __init__(self):
    super().__init__()
    self.default_dir = None
    self.project_dir = None
    self.projects = None
    self.current_project = None

  def build(self):
    self.default_dir = abspath(os.getcwd())
    self.kv_directory = path.join(self.default_dir, "kv")
    self.kv_file = path.join(self.kv_directory, "main.kv")
    self.title = "KivyCreator"
    self.set_project_dir()
    self.read_project_dir()
    return Builder.load_file(self.kv_file)

  def set_project_dir(self):
    self.project_dir = path.join(self.user_data_dir, "projects")
    if not path.isdir(self.project_dir):
      os.mkdir("projects")

  def read_project_dir(self):
    self.projects = [f for f in os.listdir(self.project_dir) if path.isdir(path.join(self.project_dir, f))]

  def open_project(self, name):
    if name in self.projects:
      #switch screens
      project_dir = path.join(self.project_dir, name)
      self.current_project = Project(project_dir).open()

  def save_project(self):
    #TODO: Save popup
    #TODO: read new content
    new_tab_content = {}
    self.current_project.save(new_tab_content)

  def close_project(self):
    self.save_project()
    self.current_project = None
    os.chdir(self.default_dir)
    

if __name__ == "__main__":
	KivyCreator().run()
























