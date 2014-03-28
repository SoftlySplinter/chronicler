import json
import logging
from flask import Blueprint, request

import chronicler

callback = Blueprint('callback', __name__)

@callback.route('', methods=['GET', 'POST'])
def callbacks():
  try:
    if request.method == 'GET':
      return json.dumps(chronicler.callback().callbacks.keys())
    if request.method == 'POST':
      details = request.get_json()
      if details is None:
        raise Exception("No data")
      return json.dumps(chronicler.callback().add_callback(details).dict())
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400 


