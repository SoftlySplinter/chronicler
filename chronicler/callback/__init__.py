import logging

class Callback(object):
  def __init__(self, data):
    pass

  def callback(self, tag, data):
    logging.debug("{0}: {1}".format(tag,data))

  @property
  def id(self):
    return "logging.debug"

  def dict(self):
    return {'id': self.id}

class CallbackFactory(object):
  @staticmethod
  def get_callback(type, data):
    try:
      callback_module = __import__(type, fromlist=[''])
      return callback_module.create(data)
    except ImportError as e:
      logging.exception(e)
      return Callback(data)

class ChroniclerCallback(object):
  callbacks = {}
  def callback(self, tag, data):
    for _, cb in self.callbacks.items():
      cb.callback(tag, data)

  def add_callback(self, data):
    type = data['type']
    cb = CallbackFactory.get_callback(type, data)
    if cb.id in self.callbacks:
      raise Exception('Callback {0} already exists'.format(cb.id))
    self.callbacks[cb.id] = cb
    return cb

