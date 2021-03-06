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
    'syslogtag': Group(Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]"))) + Suppress(":"),
    'programname': Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + Suppress(ints) + Suppress("]") + Suppress(":")),
    'PRI': ints,
    'syslogfacility': None,
    'syslogfacility-text': None,
    'syslogseverity': None,
    'syslogseverity-text': None,
    'timegenerated': Group(month + day + hour),
    'timereported': Group(month + day + hour),
    'TIMESTAMP': Group(month + day + hour)
  }

  def __init__(self, fmt):
    self.format = fmt
    self.pattern, self.properties = self.gen_format(fmt)

  def gen_format(self, fmt):
    """Generates a PyParsing element based on a formatting string."""
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
    """Parses a log line and splits it into its parsed elements."""
    try:
      res = {}
      parsed = self.pattern.parseString(line)
      for prop, elem in zip(self.properties, parsed):
        if prop in ["TIMESTAMP", 'timecreated', 'timereported']:
          res[prop] = strftime("%Y-%m-%d %H:%M:%S")
        elif prop == "syslogtag":
          res[prop] = {}
          res[prop]['programname'] = elem[0]
          if len(elem) > 1:
            res[prop]['programid'] = elem[1]
        else:
          res[prop] = elem
      callback(res)
    except ParseException as e:
      logging.warn("Unable to parse line: {0}".format(line))

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
      'log': self.file,
      'format': str(self.format),
      'name': self.name,
    }

  def parse(self, callback):
    with open(self.file, 'r') as log:
      log.seek(self.loc)
      for line in log:
        self.format.parse(line, callback)
      self.loc = log.tell()
