class Project():
  def __init__(self, folder_name):
    self.folder_name = folder_name
    self.tabs = {}
    self.get_last_tabs()

  def get_last_tabs():
    with open("tabs.kct", "r") as f:
      lines = [x.strip() for x in f.readLines()]
      for t in lines:
        self.tabs[t] = Tab(t)

  def update_tab(name, new_content):
    if name in self.tabs:
      self.tabs[name].update_content(new_content)


class Tab():
  def __init__(self, name):
    self.name = name
    self.get_content()

  def get_content():
    with open(self.name, "r") as c:
      self.content = c

  def update_content(new_content):
    self.content = new_content

  def save_content():
    with open(self.name, "w") as f:
      f.write(self.content)
