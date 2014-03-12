import json
from flask import Blueprint, request

from chronicler import chronicler

system = Blueprint('system', __name__)

@system.route('/logs' methods=['GET', 'POST']
def logs():
  if request.method == 'GET':
    return (json.dumps(chronicler.system.logs), 200)
  if request.method == 'POST':
    details = request.get_json()
    try:
      chronicler.system.create_log(details)
    except Exception as e:
      return (json.dumps({'error': e}), 400)
