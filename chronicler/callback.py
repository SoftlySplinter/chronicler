import statsd
import logging

client = statsd.StatsClient("localhost", 8125)

def statsd_callback(res):
  assert 'PRI' in res
  assert 'syslogtag' in res

  sev = res['PRI']['severity']
  name = res['syslogtag']['programname']

  logging.debug('inc(chronicler.{0}.{1}'.format(name, sev))
  client.incr('chronicler.{0}.{1}'.format(name, sev))
