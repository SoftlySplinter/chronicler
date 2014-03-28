import logging

from chronicler.log import Log

class Process(object):
  def __init__(self, properties):
    self.name = properties["name"]
    if 'pid' not in properties:
      properties['pid'] = None
    self.pid = properties["pid"]
    self.logs = {}
    for log in properties["logs"]:
      self.logs[Log.get_id(log)] = Log(log)

  def dict(self):
    return {
      'name': self.name,
      'pid': self.pid,
      'logs': [log for log in self.logs],
    }

  @property
  def id(self):
    if self.pid:
      return self.pid
    else:
      return self.name

  def parse(self, callback):
    for _, log in self.logs.items():
      def filter_callback(tag, res):
        if 'syslogtag' in res:
          if self.pid and 'pid' in res['syslogtag']:
            if self.pid == res['syslogtag']['pid']:
              callback(tag, res)
          elif self.name == res['syslogtag']['programname']:
            callback(tag, res)
      log.parse("process", filter_callback)

  def add_log(self, properties):
    id = Log.get_id(properties)
    if id not in self.logs:
      log = Log(properties)
      self.logs[id] = log
      return log
    else:
      raise Exception("Log '{0}' already exists".format(properties['log']))

class ProcessChronicler(object):
  processes = {}

  def add_process(self, properties):
    proc = Process(properties)
    if proc.id in self.processes:
      raise Exception("Process {0} already exists".format(proc.id))
    self.processes[proc.id] = proc
    return proc

  def parse(self, callback):
    for _, process in self.processes.items():
      process.parse(callback)
