import os
from os import path
from os.path import abspath
from shutil import rmtree

import kivy
from kivy.app import App
from kivy.logger import Logger
from kivy.lang import Builder

from project import Project
from uix.popups import NewProjectErrorPopup
from screens.projectslistscreen import ProjectsListScreen

kivy.require("1.9.1")


def info(text):
  Logger.info("KivyCreator: {}".format(text))


class KivyCreator(App):
  def __init__(self):
    super(KivyCreator, self).__init__()
    self.default_dir = None
    self.project_dir = None
    self.projects = None
    self.current_project = None

  def build(self):
    self.default_dir = abspath(os.getcwd())
    self.kv_directory = path.join(self.default_dir, "kv")
    self.kv_file = path.join(self.kv_directory, "main.kv")
    self.title = "KivyCreator"
    self.load_kvs()
    self.set_project_dir()
    self.read_project_dir()
    self.update_project_list()
    return self.root

  def load_kvs(self):
    for f in os.listdir(self.kv_directory):
      p = path.join(self.kv_directory, f)
      if f != "main.kv" and path.isfile(p):
        Builder.load_file(p)
    self.root = Builder.load_file(self.kv_file)

  def set_project_dir(self):
    self.project_dir = path.join(self.user_data_dir, "projects")
    if not path.isdir(self.project_dir):
      os.mkdir("projects")

  def read_project_dir(self):
    self.projects = [f for f in os.listdir(self.project_dir) if path.isdir(path.join(self.project_dir, f))]

  def get_projects_list(self):
    self.read_project_dir()
    return self.projects

  def update_project_list(self):
    self.root.projects.update_projects_list()

  def create_project(self, name):
    info("Creating project: {}".format(name))
    if self.current_project is not None:
      self.close_project()
    try:
      os.chdir(self.project_dir)
      os.mkdir(name)
      self.open_project(name)
    except FileExistsError:
      NewProjectErrorPopup(project_name=name).open()
    finally:
      self.update_project_list()

  def delete_project(self, name):
    info("Deleting project: {}".format(name))
    # TODO: add delete project popup
    if name in self.projects:
      try:
        rmtree(path.join(self.project_dir, name))
      except:
        info("An error occurred when deleting project: {}".format(name))
    self.update_project_list()

  def run_project(self, name):
    info("Running project: {}".format(name))
    #TODO: run project

  def export_project(self, name):
    info("Exporting project: {}".format(name))
    #TODO: export project

  def open_project(self, name):
    info("opening project: {}".format(name))
    if name in self.projects:
      project_dir = path.join(self.project_dir, name)
      self.current_project = Project(project_dir).open()
      # switch screens

  def save_project(self):
    info("saving current project")
    # TODO: Save popup
    # TODO: read new content
    new_tab_content = {}
    self.current_project.save(new_tab_content)

  def close_project(self):
    info("closing current project")
    self.save_project()
    self.current_project = None
    os.chdir(self.default_dir)


if __name__ == "__main__":
  KivyCreator().run()
