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
    return json.dumps({'error': 'Process {0} does not exist'.format(id)}), 404
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400

@process.route('/<string:id>/logs', methods=['GET', 'POST'])
def process_logs(id):
  try:
    proc = chronicler.process().processes[id]
    if request.method == 'GET':
      return json.dumps([log for log in proc.logs])
    if request.method == 'POST':
     details = request.get_json()
     if not details:
       raise Exception("No data")
     log = proc.add_log(details)
     return json.dumps(log.dict()) 
  except KeyError as e:
    return json.dumps({'error': 'Process {0} does not exist'.format(id)}), 404
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400

@process.route("/<string:pid>/logs/<string:lid>", methods=['GET', 'DELETE'])
def process_log(pid, lid):
  log_id = int(lid)
  try:
    proc = chronicler.process().processes[pid]
    try:
      if request.method == 'GET':
        return json.dumps(proc.logs[log_id].dict())
      if request.method == 'DELETE':
        proc.logs.pop(log_id)
        return "", 200
    except KeyError as e:
      return json.dumps({'error': 'Log {0} does not exist'.format(log_id)}), 404
  except KeyError as e:
    return json.dumps({'error': 'Process {0} does not exist'.format(id)}), 404
  except Exception as e:
    logging.exception(e)
    return json.dumps({'error': str(e)}), 400
