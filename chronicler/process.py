
def Process(object):
  def __init__(self, name, pid=None, logs=[]):
    self.name = name
    self.pid = pid
    self.logs = logs

  def to_dict(self):
    return {
      'name': self.name,
      'pid': self.pid,
      'logs': [log.id for log in self.logs],
    }
