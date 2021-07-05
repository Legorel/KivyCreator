import sys
import os
from os import path
import importlib
import traceback

import kivy
from kivy.app import App
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.settings import Settings

from kcscreenmanager import KCScreenManager

kivy.require("2.0.0")


class KivyCreator(App):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.run_user_app = False
    self.user_app_path = ""

  def build(self):
    self.kv_directory = path.join(os.getcwd(), "kv")
    self.load_kv_files()

    return KCScreenManager()

  def build_config(self, config: ConfigParser):
    config.setdefaults("customization", {
      "button_per_scroll": 4
    })

  def build_settings(self, settings: Settings):
    settings.add_json_panel("Kivy Creator", self.config, "settings.json")

  def load_kv_files(self):
    self.unload_kv_files()
    for file in os.listdir(self.kv_directory):
      file_path = path.join(self.kv_directory, file)
      if path.isfile(file_path):
        Logger.info(f"KC: Loading kv from {file}")
        Builder.load_file(file_path)

  def unload_kv_files(self):
    for file in os.listdir(self.kv_directory):
      file_path = path.join(self.kv_directory, file)
      if os.path.isfile(file_path):
        Logger.info(f"KC: Unloading kv from {file}")
        Builder.unload_file(file_path)


def run_from_file(app_path):
  if path.exists(app_path):
    new_dir = path.dirname(app_path)
    new_file = path.basename(app_path)
    os.chdir(new_dir)
    new_module_name = path.splitext(new_file)[0]
    if new_module_name not in sys.modules:
      new_module = importlib.import_module(new_module_name)
    else:
      importlib.reload(sys.modules[new_module_name])


if __name__ == "__main__":
  should_run = True
  while should_run:
    if App.get_running_app() is not None:
      App.get_running_app().stop()
    kc = KivyCreator()
    kc.run()
    # Main app stops
    if kc.run_user_app:
      try:
        Logger.info("KC: Running user's app")
        run_from_file(kc.user_app_path)
      except:
        Logger.error(f"KC: An error occurred while running an user app:")
        traceback.print_exc()

      Logger.info("KC: Running main app")
      continue
    should_run = False
