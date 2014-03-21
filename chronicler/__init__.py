import time
import logging
from threading import Thread, Lock

from chronicler.system import SyslogChronicler 
from chronicler.process import ProcessChronicler 
from chronicler.callback import statsd_callback as callback

logging.getLogger().setLevel(0)

class Chronicler(Thread):
  """The main threaded class which handles log watching."""
  lastrun = time.time()
  syslog = SyslogChronicler()
  process = ProcessChronicler()
  __queue = []
  running = False

  def stop(self):
    """Stops watching"""
    self.running = False

  def run(self):
    """Loop until stop is called. Automatically called by Thread.start"""
    self.running = True
    logging.info("test")
    lock = Lock()
    while self.running:
      self.process.parse(callback)
#      with lock:
#        for (_, log) in self.syslog.logs.items():
#          log.parse(self.no_op)
          
      time.sleep(0.01)

  def no_op(self, args):
    pass

__chronicler = Chronicler

def start():
  global __chronicler
  if __chronicler.running:
    raise Exception("Chronicler already started")
  __chronicler = Chronicler()
  __chronicler.start()
  return status()

def stop():
  global __chronicler
  if not __chronicler.running:
    raise Exception("Chronicler not started")
  __chronicler.stop()
  return status()
#  __chronicler = None

def system():
  global __chronicler
  if not __chronicler.running:
    raise Exception("Chronicler not started")
  return __chronicler.syslog

def process():
  global __chronicler
  if not __chronicler.running:
    raise Exception("Chronicler not started")
  return __chronicler.process

def add_syslog(properties):
  global __chronicler
  if not __chronicler.running:
    raise Exception("Chronicler not started")
  return __chronicler.syslog.add_log(properties)

def add_process(properties):
  global __chronicler
  if not __chronicler.running:
    raise Exception("Chronicler not started")
  if 'logs' not in properties:
    properties['logs'] = [log.dict() for _, log in __chronicler.syslog.logs.items()]
  return __chronicler.process.add_process(properties)

def status():
  global __chronicler
  return {'chronicler': __chronicler.running}

from chronicler.api import api

def run():
#  for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
#    signal.signal(sig, stop)
  api.run(debug=True)
