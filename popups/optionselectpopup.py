from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class OptionSelectPopup(Popup):
  option_grid = ObjectProperty(None)

  def __init__(self, project_name):
    super().__init__()
    self.project_name = project_name
    self.title = project_name
    self.options = {}

  def add_option(self, text):
    self.options[text] = Button(text=text)
    self.options[text].bind(on_release=self.dismiss)
    self.option_grid.add_widget(self.options[text])

  def add_options(self, options):
    for text in options:
      self.add_option(text)

  def bind_to_option(self, option, func):
    if option in self.options.keys():
      self.options[option].bind(on_release=func)
