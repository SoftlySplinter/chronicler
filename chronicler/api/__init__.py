import json
from flask import Flask

import chronicler
from chronicler.api.system import system
from chronicler.api.process import process
from chronicler.api.callback import callback

api = Flask('chronicler')
api.register_blueprint(system, url_prefix = '/system')
api.register_blueprint(process, url_prefix = '/process')
api.register_blueprint(callback, url_prefix = '/callback')

@api.route('/chronicler', methods=['POST'])
def start():
  try:
    return json.dumps(chronicler.start())
  except Exception as e:
    return json.dumps({'error': str(e)}), 400

@api.route('/chronicler', methods=['DELETE'])
def stop():
  try:
    return json.dumps(chronicler.stop())
  except Exception as e:
    return json.dumps({'error': str(e)}), 400

@api.route('/chronicler', methods=['GET'])
def status():
  try:
    return json.dumps(chronicler.status())
  except Exception as e:
    return json.dumps({'error': str(e)}), 400
