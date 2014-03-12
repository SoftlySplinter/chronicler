from chronicler.log import Log

class SyslogChronicler(object):
  """Watches system log files"""
  __logs = {}

  @property
  def logs(self):
    return self.__logs

  def add_log(self, log_properties):
    if Log.get_id(log_properties) not in self.__logs:
      watcher = LogWatcher(log_properties)
      self.__logs[watcher.id] = watcher
    else:
      raise Exception("Log '{0}' already exists".format(log_properties['log']))
