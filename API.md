# Daemon

Creation of a daemon is done through a POST.

```http
POST /daemon HTTP/1.1
```
```json
{
  "name": "chronicler",
}
```
```http
HTTP/1.1 200 OK
```
```json
{
  "name": "chronicler",
  "running": true,
  "logs": [],
  "callbacks": []
}
```

Viewing the status of a daemon is done through a GET

```http
GET /daemon/chronicler

HTTP/1.1 200 OK

{
  "name": "chronicler",
  "running": true,
  "logs": [],
  "callbacks": []
}
```

To pause a daemon, PATCH is used

```http
PATCH /daemon/chronicler HTTP/1.1

{
  "pause": true
}

HTTP/1.1 200 OK

{
  "name": "chronicler",
  "running": false,
  "logs": [],
  "callbacks": []
}
```

To stop and remove a daemon, DELETE is used

```http
DELETE /daemon/chronicler HTTP/1.1

HTTP/1.1 200 OK  
```


# Log Files

Daemons watch all log files added to them. This is done using standard CRUD
commands.

```http
POST /daemon/chronicler/log HTTP/1.1

{
  "file": "/var/syslog",
  "format": "<%PRI%> %TIMESTAMP% %HOSTNAME% %syslogtag%%msg%"
}

HTTP/1.1 200 OK

{
  "id": 1
}
```

```http
GET /daemon/chronicler/log HTTP/1.1

HTTP/1.1 200 OK

[
  {
    "id": 1
  }
]
```

```http
GET /daemon/chronicler/log/1 HTTP/1.1

HTTP/1.1 200 OK

{
  "id": 1,
  "file": "/var/syslog",
  "format": "<%PRI%> %TIMESTAMP% %HOSTNAME% %syslogtag%%msg%"
}
```

```http
DELETE /daemon/chronicler/log/1 HTTP/1.1

HTTP/1.1 200 OK
```

# Callbacks

Callbacks are a way to get alerts from log entries. There are several callbacks
on offer:

* General monitoring
* Process monitoring
* Level monitoring
* Fine monitoring

## General monitoring

General monitoring alerts on every new log entry regardless of process or log
level.

```http
POST /daemon/chronicler/callback

{
  "type": "general",
  "callback": {
    "type": statsd"
    "details": {
      "host": "statsd.example.com",
      "port": 8125 
    }
  }
}

HTTP/1.1 200 OK

{
  "id": 1,
  "type": "general",
  "callback": {
    "type": "statsd",
    "details": {
      "host": "statsd.example.com",
      "port": 8125
      "tag": "chronicler.%syslogtag%.%syslogseverity-text%"
    }
  }
}
```

```http
GET /daemon/chronicler/callback HTTP/1.1

HTTP/1.1 200 OK
[
  {
    "id": 1,
    "type": "general"
  }
]
```

```http
GET /daemon/chronicler/callback/1 HTTP/1.1

HTTP/1.1 200 OK

{
  "id": 1,
  "type": "general",
  "callback": {
    "type": "statsd",
    "details": {
      "host": "statsd.example.com",
      "port": 8125
      "tag": "chronicler.%syslogtag%.%syslogseverity-text%"
    }
  }
}
```

```http
PATCH /daemon/chronicler/callback/1 HTTP/1.1

{
  "update": "callback",
  "details": {
    "type": statsd",
    "details": {
      "host": "statsd.example.com",
      "port": 8125,
      "tag": "chronicler.syslog.%progname%.%syslogseverity-text%"
    }
  }
}

HTTP/1.1 200 OK
```

```http
DELETE /daemon/chronicler/callback/1

HTTP/1.1 200 OK
```

