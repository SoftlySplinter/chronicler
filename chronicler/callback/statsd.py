from __future__ import absolute_import

from statsd import StatsClient
import logging

from chronicler.callback import Callback

class StatsdCallback(Callback):
  def __init__(self, data):
    host = data['host']
    port = int(data['port'])
    self.name = "statsd.{0}:{1}".format(host, port)
    self.client = StatsClient(host, port)

  @property
  def id(self):
    return self.name

  def callback(self, tag, data):
    assert 'PRI' in data
    assert 'syslogtag' in data

    sev = data['PRI']['severitytext']
    name = data['syslogtag']['programname']
    self.client.incr('chronicler.{0}.{1}.{2}'.format(tag, name, sev))

def create(data):
  return StatsdCallback(data)
