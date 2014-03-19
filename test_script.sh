#!/bin/sh

curl http://127.0.0.1:5000/start -X POST
curl http://127.0.0.1:5000/system/logs -X POST --data @examples/syslog.json -H "Content-Type:application/json"
curl http://127.0.0.1:5000/system/logs -X GET -H "Accept:application/json"
curl http://127.0.0.1:5000/system/logs/-6477767910910693092 -X GET -H "Accept:application/json"
sleep 10
curl http://127.0.0.1:5000/system/logs -X POST --data @examples/sample.json -H "Content-Type:application/json"
