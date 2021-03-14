from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


class ProjectItem(GridLayout):
  def __init__(self, project_name="NoName", **kwargs):
    super(ProjectItem, self).__init__(**kwargs)
    self.size_hint_y = .1
    self.rows = 1
    self.project_button = Button(text=project_name, on_release=self.project_button_released)
    self.add_widget(self.project_button)
    self.more_button = Button(text="...", on_release=self.more_button_released)
    self.add_widget(self.more_button)
    self.more_button.size_hint_x = 0.2

  def project_button_released(self, _):
    App.get_running_app().open_project(self.project_button.text)

  def more_button_released(self, _):
    MorePopup(title=self.project_button.text).open()


class MorePopup(Popup):
  def __init__(self, **kwargs):
    super(MorePopup, self).__init__(**kwargs)
    self.title = "{} options".format(self.title)
