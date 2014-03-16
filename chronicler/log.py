import json

class Log(object):
  """Stores information about a logfile."""

  @staticmethod
  def get_id(properties):
    return hash(properties['log'])

  def __init__(self, properties):
    self.file = properties['log']

  @property
  def id(self):
    return hash(self.file)

  def dict(self):
    return {
      'id': self.id,
      'file': self.file,
    }
