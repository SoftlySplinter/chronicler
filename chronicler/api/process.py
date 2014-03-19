import json
import logging

from flask import Blueprint, request

import chronicler

process = Blueprint('process', __name__)

@process.route('', methods=['POST'])
def processes():
  try:
    details = request.get_json()
    if not details:
      raise Exception("No data")
    process = chronicler.add_process(details)
    return json.dumps(process.to_dict())
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400
