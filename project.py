from os import chdir

class Project:
  def __init__(self, project_dir):
    self.project_dir = project_dir
    self.tabs = {}
    self.get_last_tabs()

  def get_last_tabs(self):
    with open("tabs.kct", "r") as f:
      lines = [x.strip() for x in f.readLines()]
      for t in lines:
        self.tabs[t] = Tab(t)

  def update_tab(self, name, new_content):
    if name in self.tabs:
      self.tabs[name].update_content(new_content)

  def open(self):
    chdir(self.project_dir)

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
    with open(self.name, "r") as c:
      self.content = c

  def update_content(self, new_content):
    self.content = new_content

  def save_content(self):
    with open(self.name, "w") as f:
      f.write(self.content)
