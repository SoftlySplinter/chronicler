import time
import logging
from threading import Thread

from chronicler.system import SyslogChronicler 

logging.getLogger().setLevel(0)

class Chronicler(Thread):
  """The main threaded class which handles log watching."""
  lastrun = time.time()
  syslog = SyslogChronicler()

  def stop(self):
    """Stops watching"""
    self.running = False

  def run(self):
    """Loop until stop is called. Automatically called by Thread.start"""
    self.running = True
    logging.info("test")
    while self.running:
      for (_, log) in self.syslog.logs.iteritems():
        log.parse(logging.info)
      time.sleep(0.01)

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

from chronicler.api import api

def run():
#  for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
#    signal.signal(sig, stop)
  api.run(debug=True)
