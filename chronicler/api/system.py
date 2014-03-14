import json
import logging
from flask import Blueprint, request

import chronicler

system = Blueprint('system', __name__)

@system.route('/logs', methods=['GET', 'POST'])
def logs():
  try:
    if request.method == 'GET':
      return (json.dumps(chronicler.system().logs), 200)
    if request.method == 'POST':
      details = request.get_json()
      print details
      chronicler.add_syslog(details)
  except Exception as e:
      logging.exception(e)
      return (json.dumps({'error': str(e)}), 400)
