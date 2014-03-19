import time
import logging
from threading import Thread, Lock

from chronicler.system import SyslogChronicler 
from chronicler.process import ProcessChronicler 

logging.getLogger().setLevel(0)

class Chronicler(Thread):
  """The main threaded class which handles log watching."""
  lastrun = time.time()
  syslog = SyslogChronicler()
  process = ProcessChronicler()
  __queue = []

  def stop(self):
    """Stops watching"""
    self.running = False

  def run(self):
    """Loop until stop is called. Automatically called by Thread.start"""
    self.running = True
    logging.info("test")
    lock = Lock()
    while self.running:
      self.process.parse(logging.info)
#      with lock:
#        for (_, log) in self.syslog.logs.items():
#          log.parse(self.no_op)
          
      time.sleep(0.01)

  def no_op(self, args):
    pass

__chronicler = None

def start():
  global __chronicler
  if __chronicler:
    raise Exception("Chronicler already started")
  __chronicler = Chronicler()
  __chronicler.start()

def stop():
  global __chronicler
  if not __chronicler:
    raise Exception("Chronicler not started")
  __chronicler.stop()
  __chronicler = None

def system():
  global __chronicler
  if not __chronicler:
    raise Exception("Chronicler not started")
  return __chronicler.syslog

def add_syslog(properties):
  if not __chronicler:
    raise Exception("Chronicler not started")
  return __chronicler.syslog.add_log(properties)

def add_process(properties):
  if not __chronicler:
    raise Exception("Chronicler not started")
  if 'logs' not in properties:
    properties['logs'] = [log.dict() for _, log in __chronicler.syslog.logs.items()]
  return __chronicler.process.add_process(properties)

from chronicler.api import api

def run():
#  for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
#    signal.signal(sig, stop)
  api.run(debug=True)
