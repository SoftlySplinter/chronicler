class Log(object):
  """Stores information about a logfile."""

  @staticmethod
  def get_id(properties):
    return hash(properties['log'])

  def __init__(self, properties):
    self.file = properties.log

  @property
  def id(self):
    return hash(self.logfile)
