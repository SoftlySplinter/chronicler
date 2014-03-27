from threading import Lock

from chronicler.log import Log

class SyslogChronicler(object):
  """Watches system log files"""
  logs = {}

  def add_log(self, log_properties):
    lock = Lock()
    with lock:
      if Log.get_id(log_properties) not in self.logs:
        watcher = Log(log_properties)
        self.logs[watcher.id] = watcher
        return watcher
      else:
        raise Exception("Log '{0}' already exists".format(log_properties['log']))

  def parse(self, callback):
    lock = Lock()
    with lock:
      for log in self.logs:
        self.logs[log].parse("system.{0}".format(self.logs[log].file), callback)
