import json
import logging

from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex, ParseException, Empty, Group
from time import strftime

ints = Word(nums)

month = Word(string.uppercase, string.lowercase, exact=3)
day   = ints
hour  = Combine(ints + ":" + ints + ":" + ints)

class LogFormat(object):
  __properties = {
    'msg': Regex(".*"),
    'rawmsg': Regex(".*"),
    'HOSTNAME': Word(alphas + nums + "_" + "-" + "."),
    'syslogtag': Group(Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")),
    'programname': Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + Suppress(ints) + Suppress("]") + Suppress(":")),
    'PRI': ints,
    'syslogfacility': None,
    'syslogfacility-text': None,
    'syslogseverity': None,
    'syslogseverity-text': None,
    'timegenerated': None,
    'timereported': None,
    'TIMESTAMP': Group(month + day + hour)
  }

  def __init__(self, fmt):
    self.format = fmt
    self.pattern, self.properties = self.gen_format(fmt)

  def gen_format(self, fmt):
    res = Empty()
    props = []
    escape = False
    prop = ""
    for char in fmt:
      if escape:
        if char == "%":
          escape = False
          res = res + self.__properties[prop]
          props.append(prop)
          prop = ""
        else:
          prop = prop + char
      else:
        if char == "%":
          escape = True
        elif char == " ":
          pass
        else:
          res = res + Suppress(char)
    return res, props

  def parse(self, line, callback):
    try:
      res = {}
      parsed = self.pattern.parseString(line)
      i = 0
      for prop in self.properties:
        if prop == "TIMESTAMP":
          res[prop] = strftime("%Y-%m-%d %H:%M:%S")
          i += 1
        else:
          res[prop] = parsed[i]
          i += 1
      callback(res)
    except ParseException as e:
      logging.warn("Unable to parse line: {0}".format(line))
      logging.exception(e)

  def __str__(self):
    return self.format
    

class Log(object):
  """Stores information about a logfile."""

  __default_format = "<%PRI%>%TIMESTAMP% %HOSTNAME% %syslogtag%%msg%"
  loc = 0

  @staticmethod
  def get_id(properties):
    """Get the ID of a log, used to place an item into a dictionary."""
    return hash(properties['log'])

  def __init__(self, properties):
    self.file = properties['log']
    
    if 'format' not in properties:
      properties['format'] = self.__default_format
    self.format = LogFormat(properties['format'])
    
    if 'name' not in properties:
      properties['name'] = properties['log']
    self.name = properties['name']

  @property
  def id(self):
    return Log.get_id({'log': self.file})

  def dict(self):
    return {
      'id': self.id,
      'file': self.file,
      'format': str(self.format),
      'name': self.name,
    }

  def parse(self, callback):
    with open(self.file, 'r') as log:
      log.seek(self.loc)
      for line in log:
        self.format.parse(line, callback)
      self.loc = log.tell()
