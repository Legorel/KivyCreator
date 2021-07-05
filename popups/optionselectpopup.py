from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class OptionSelectPopup(Popup):
  option_grid = ObjectProperty(None)

  def __init__(self, project_name):
    super().__init__()
    self.title = project_name
    self.result = None

  def set_result(self, result):
    self.result = result

  def add_option(self, text):
    button = Button(text=text)
    button.bind(on_release=lambda b: self.set_result(b.text))
    self.option_grid.add_widget(button)

  def add_options(self, options):
    for text in options:
      self.add_option(text)
