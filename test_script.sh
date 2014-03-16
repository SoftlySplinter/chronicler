#!/bin/sh

curl http://127.0.0.1:5000/start -X POST
curl http://127.0.0.1:5000/system/logs -X POST --data @syslog.json -H "Content-Type:application/json"
curl http://127.0.0.1:5000/system/logs -X GET -H "Accept:application/json"
curl http://127.0.0.1:5000/system/logs -X POST --data @syslog.json -H "Content-Type:application/json"
curl http://127.0.0.1:5000/system/logs -X GET -H "Accept:application/json"
curl http://127.0.0.1:5000/stop -X POST
