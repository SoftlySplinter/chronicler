import json
import logging
from flask import Blueprint, request

import chronicler

system = Blueprint('system', __name__)

@system.route('/logs', methods=['GET', 'POST'])
def logs():
  try:
    if request.method == 'GET':
      logs = [log for log in chronicler.system().logs.keys()]
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

@system.route('/logs/<string:id>', methods=['GET', 'DELETE'])
def log(id):
  log_id = int(id)
  try:
    if request.method == 'GET':
      return json.dumps(chronicler.system().logs[log_id].dict())
    if request.method == 'DELETE':
      chronicler.system().logs.pop(log_id)
      return ("", 200)
  except KeyError as e:
    return (json.dumps({'error': 'Log {0} does not exist'.format(log_id)}), 404)
  except Exception as e:
    logging.exception(e)
    return (json.dumps({'error': str(e)}), 500)
