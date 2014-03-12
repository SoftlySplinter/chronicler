# Chronicler

Monitor your logs.

## Usage

Chronicler is run as a Linux daemon which provides a REST API for monitoring log
activity and reporting usage using [statsd](https://github.com/etsy/statsd/).

The chronicler script (`bin/chronicler`) acts like a system process.

## REST API

The REST API is as follows:

### Daemon Control

Monitoring can be controlled through the following endpoints:

```http
POST /start HTTP/1.1
```

```http
POST /stop HTTP/1.1
```

### Monitor System Logs

To add a system log to monitor:

```http
POST /system/log HTTP/1.1
Content-Type: application/json
Accept: application/json
```
```json
{
  'log': '/path/to/log',
  'format': 'log format (optional, defaults to the syslog format)',
  'name': 'name (optional)'
}
```

This will return:

```json
{
  'id': 'log id',
  'log': '/path/to/log',
  'format': 'log format',
  'name': 'log name'
}
```

To get all the system logs monitored:

```http
GET /system/log/ HTTP/1.1
Accept: application/json
```

Returns:

```json
{
  'logs': ['ids', ...]
}
```

To get a specific log monitored:

```http
GET /system/log/:id HTTP/1.1
Accept: application/json
```

Returns:

```json
{
  'id': 'log id',
  'log': '/path/to/log',
  'format': 'log format',
  'name': 'log name'
}
```

To remove a specific log:

```http
DELETE /system/log/:id HTTP/1.1
```


### Process Monitoring

Specific processes can also be monitored through the following endpoints.

Adding a new process.

```http
POST /process HTTP/1.1
Content-Type: application/json
Accept: application/json
```
```json
{
  'name': 'process name',
  'pid': 'process id (optional)',
  'logs': ['log id',...] (optional)
}
```

For a PID to function correctly the log format must include that information.

Returns:

```json
{
  'name': 'process name',
  'pid': 'process id',
  'logs': ['log id',...]
}
```

By default the logs will be those that are in `/system`.

Getting all processes monitored:

```http
GET /process HTTP/1.1
Accept: application/json
```
```json
{
  'processes': ['ps name',...]
}
```

Getting a specific process:

```http
GET /process/:id HTTP/1.1
Accept: application/json
```
```
{
  'name': 'process name',
  'pid': 'process id',
  'logs': ['log id',...]
}
```

Adding a log specific to a process:

```http
POST /process/:id/log HTTP/1.1
Content-Type: application/json
Accept: application/json
```

This takes and receives the same information as creating a system log.

...

Removing a process from monitoring

```http
DELETE /process/:id HTTP/1.1
```

## Dependencies

...
