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
    return json.dumps(process.dict())
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400

@process.route('/<string:id>', methods=['GET', 'DELETE'])
def __process(id):
  try:
    if request.method == 'GET':
      return json.dumps(chronicler.process().processes[id].dict())
    if request.method == 'DELETE':
      chronicler.process().processes.pop(id)
      return "", 200
  except KeyError as e:
    return (json.dumps({'error': 'Process {0} does not exist'.format(id)}), 404)
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400
