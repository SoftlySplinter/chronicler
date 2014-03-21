#!/bin/sh

curl http://127.0.0.1:5000/chronicler -X GET
echo '\n'
curl http://127.0.0.1:5000/chronicler -X POST
echo '\n'
curl http://127.0.0.1:5000/chronicler -X GET
echo '\n'
curl http://127.0.0.1:5000/system/logs -X GET -H "Accept:application/json"
echo '\n'
curl http://127.0.0.1:5000/system/logs/-6477767910910693092 -X GET -H "Accept:application/json"
echo '\n'
curl http://127.0.0.1:5000/system/logs -X POST --data @examples/sample.json -H "Content-Type:application/json"
echo '\n'
curl http://127.0.0.1:5000/process -X POST --data @examples/process.json -H "Content-Type: application/json"
echo '\n'
