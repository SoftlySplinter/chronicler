import json
from flask import Flask

import chronicler
from chronicler.api.system import system
from chronicler.api.process import process

api = Flask('chronicler')
api.register_blueprint(system, url_prefix = '/system')
api.register_blueprint(process, url_prefix = '/process')

@api.route('/start', methods=['POST'])
def start():
  try:
    chronicler.start()
    return ("", 200)
  except Exception as e:
    return (json.dumps({'error': str(e)}), 400)

@api.route('/stop', methods=['POST'])
def stop():
  try:
    chronicler.stop()
    return ("", 200)
  except Exception as e:
    return (json.dumps({'error': str(e)}), 400)


