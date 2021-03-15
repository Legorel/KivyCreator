from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from uix.popups import MorePopup


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
    MorePopup(project_name=self.project_button.text).open()
