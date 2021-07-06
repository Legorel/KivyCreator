from kivy.uix.popup import Popup


class TextInputPopup(Popup):
  def __init__(self, title):
    super().__init__()
    self.title = title
    self.input = ""
