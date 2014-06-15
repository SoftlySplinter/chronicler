# Daemon

Creation of a daemon is done through a POST.

```http
POST /daemon HTTP/1.1

{
  'name': 'chronicler',
}

HTTP/1.1 200 OK

{
  'name': 'chronicler',
  'running': true,
  'logs': [],
  'callbacks': []
}
```

Viewing the status of a daemon is done through a GET

```http
GET /daemon/chronicler

HTTP/1.1 200 OK

{
  'name': 'chronicler',
  'running': true,
  'logs': [],
  'callbacks': []
}
```

To pause a daemon, PATCH is used

```http
PATCH /daemon/chronicler HTTP/1.1

{
  'pause': true
}

HTTP/1.1 200 OK

{
  'name': 'chronicler',
  'running': false,
  'logs': [],
  'callbacks': []
}
```

To stop and remove a daemon, DELETE is used

```http
DELETE /daemon/chronicler HTTP/1.1

HTTP/1.1 200 OK  
```
