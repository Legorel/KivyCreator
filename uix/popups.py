from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

class MorePopup(Popup):
  def __init__(self, project_name="NoName", **kwargs):
    super(MorePopup, self).__init__(**kwargs)
    self.project_name = project_name
    self.title = "{} options".format(self.project_name)


class NewProjectPopup(Popup):
  text_input = ObjectProperty(None)

  def create_project(self):
    if self.text_input.text != "":
      self.dismiss()
      App.get_running_app().create_project(self.text_input.text)


class NewProjectErrorPopup(Popup):
  def __init__(self, project_name="NoName", **kwargs):
    self.project_name = project_name
    super(NewProjectErrorPopup, self).__init__(**kwargs)