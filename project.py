from os import chdir


class Project:
  def __init__(self, project_dir):
    self.project_dir = project_dir
    self.tabs = {}

  def get_last_tabs(self):
    try:
      with open("tabs.kct", "r") as f:
        lines = list(f)
        for t in lines:
          self.tabs[t] = Tab(t)
    except FileNotFoundError:
      open("tabs.kct", "w").close()

  def update_tab(self, name, new_content):
    if name in self.tabs:
      self.tabs[name].update_content(new_content)

  def open(self):
    chdir(self.project_dir)
    self.get_last_tabs()

  def save(self, tab_content):
    for k in tab_content.keys():
      if k in self.tabs:
        self.tabs[k].update_content(tab_content[k])


class Tab:
  def __init__(self, name):
    self.name = name
    self.content = None
    self.get_content()

  def get_content(self):
    try:
      c = open(self.name, "r")
      self.content = c.read()
      c.close()
    except FileNotFoundError:
      print("Couldn't open file")

  def update_content(self, new_content):
    self.content = new_content
    self.save_content()

  def save_content(self):
    try:
      f = open(self.name, "w")
      f.write(self.content)
      f.close()
    except FileNotFoundError:
      print("Couldn't write to file")
