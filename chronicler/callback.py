from statsd import StatsClient
import logging

class Callback(object):
  def __init__(self, data):
    pass

  def callback(self, data):
    logging.debug(data)

  @property
  def id(self):
    return "logging.debug"

class StatsdCallback(Callback):
  def __init__(self, data):
    host = data['host']
    port = int(data['port'])
    self.name = "statsd.{0}:{1}".format(host, port)
    self.client = StatsClient(host, port)

  @property
  def id(self):
    return self.name

  def callback(self, data):
    assert 'PRI' in data
    assert 'syslogtag' in data

    sev = data['PRI']['severity']
    name = data['syslogtag']['programname']
    self.client.incr('chronicler.{0}.{1}'.format(name, sev))

class CallbackFactory(object):
  __callbacks = {
    'statsd': StatsdCallback
  }

  @staticmethod
  def get_callback(type, data):
    return CallbackFactory.__callbacks[type](data)

class ChroniclerCallback(object):
  callbacks = {}
  def callback(self, data):
    for _, cb in self.callbacks.items():
      cb.callback(data)

  def add_callback(self, data):
    type = data['type']
    cb = CallbackFactory.get_callback(type, data)
    if cb.id in self.callbacks:
      raise Exception('Callback {0} already exists'.format(cb.id))
    self.callbacks[cb.id] = cb

