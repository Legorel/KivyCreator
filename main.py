import os
from os import path

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.logger import Logger


def info(text):
  Logger.info(text)


class KivyCreator(App):
  def build(self):
    self.kv_directory = path.join(self.user_data_dir, "kv")
    self.title = "KivyCreator"
    self.set_project_dir()
    self.read_project_dir()
    return Button(text=str(self.projects))

  def set_project_dir(self):
    self.project_dir = path.join(self.user_data_dir, "projects")
    info(self.user_data_dir)
    info(self.project_dir)
    if not path.isdir(self.project_dir):
      os.mkdir("projects")

  def read_project_dir(self):
    self.projects = folders = [f for f in os.listdir(self.project_dir) if path.isdir(path.join(self.project_dir, f))]

  def open_project(self, name):
    if name in self.projects:
      #switch screens
      #open files

  def save_project(self):
    pass

  def close_project(self):
    

if __name__ == "__main__":
	KivyCreator().run()
























