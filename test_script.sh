#!/bin/sh

if [ -f examples/gen.log ]
then
  rm examples/gen.log
fi
touch examples/gen.log

curl http://127.0.0.1:5000/chronicler -X GET
echo '\n'
curl http://127.0.0.1:5000/chronicler -X POST
echo '\n'
curl http://127.0.0.1:5000/chronicler -X GET
echo '\n'
curl http://127.0.0.1:5000/system/logs -X GET -H "Accept:application/json"
echo '\n'
curl http://127.0.0.1:5000/callback -X POST --data @examples/callback.json -H "Content-Type:application/json"
echo '\n'
curl http://127.0.0.1:5000/system/logs -X POST --data @examples/gen.json -H "Content-Type:application/json"
echo '\n'
curl http://127.0.0.1:5000/process -X POST --data @examples/process.json -H "Content-Type: application/json"
echo '\n'

# Run an example program.
python chronicler/example-prog.py examples/gen.log
