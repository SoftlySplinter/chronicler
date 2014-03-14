from chronicler.log import Log

class SyslogChronicler(object):
  """Watches system log files"""
  logs = {}

  def add_log(self, log_properties):
    if Log.get_id(log_properties) not in self.logs:
      watcher = LogWatcher(log_properties)
      self.logs[watcher.id] = watcher
    else:
      raise Exception("Log '{0}' already exists".format(log_properties['log']))
