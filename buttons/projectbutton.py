from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class ProjectButton(GridLayout):
  def __init__(self, **kwargs):
    super().__init__()
    self.rows = 1
    # TODO: Change how project's inputs are dispatched (maybe)
    self.register_event_type("on_project_released")
    self.register_event_type("on_project_settings_released")
    self.project_name = kwargs.get("text")
    self.main_button = Button(text=self.project_name)
    self.main_button.bind(on_release=lambda _: self.dispatch("on_project_released"))
    self.add_widget(self.main_button)
    self.settings_button = Button(text="...", size_hint=(0.3, 1))
    self.settings_button.bind(on_release=lambda _: self.dispatch("on_project_settings_released"))
    self.add_widget(self.settings_button)

  def on_project_released(self):
    pass

  def on_project_settings_released(self):
    pass
