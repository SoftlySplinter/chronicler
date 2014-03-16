import json
import logging
from flask import Blueprint, request

import chronicler

system = Blueprint('system', __name__)

@system.route('/logs', methods=['GET', 'POST'])
def logs():
  try:
    if request.method == 'GET':
      logs = [log.dict() for (_, log) in chronicler.system().logs.iteritems()]
      return (json.dumps(logs), 200)
    if request.method == 'POST':
      details = request.get_json()
      print details
      if not details:
        raise Exception("No data")
      log = chronicler.add_syslog(details)
      return (json.dumps(log.dict()), 200)
  except Exception as e:
      logging.exception(e)
      return (json.dumps({'error': str(e)}), 400)

@system.route('/logs/<id>', methods=['GET', 'DELETE'])
def log(id):
  try:
    log = chronicler.system().logs[int(id)]
    if request.method == 'GET':
      return json.dumps(log.dict())
  except Exception as e:
    logging.exception(e)
    return (json.dumps({'error': str(e)}), 400)
