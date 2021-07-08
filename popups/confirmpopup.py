from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


class ConfirmPopup(Popup):
  message_label = ObjectProperty(None)

  def __init__(self, title, message):
    super().__init__()
    self.result = False
    self.title = title
    self.message_label.text = message
