import json
from flask import Flask

from chronicler import chronicler
from chronicler.api.system import system
from chronicler.api.process import process

api = Flask('chronicler')

@api.route('/start', methods=['POST'])
def start():
  try:
    chronicler.start()
    return ("", 200)
  except Exception as e:
    return (json.dumps({'error': e}), 400)

@api.route('/stop', methods=['POST'])
def stop():
  try:
    chronicler.stop()
    return ("", 200)
  except Exception as e:
    return (json.dumps({'error': e}), 400)


