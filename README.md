# Chronicler

![](https://travis-ci.org/SoftlySplinter/chronicler.svg)&nbsp;[![Coverage Status](https://coveralls.io/repos/SoftlySplinter/chronicler/badge.png?branch=schema)](https://coveralls.io/r/SoftlySplinter/chronicler?branch=schema)

Monitor your logs.

## Table of Contents

1. [Usage](#usage)
2. [REST API](#rest-api)
  1. [Daemon Control](#daemon-control)
  2. [Monitor System Logs](#monitor-system-logs)
  3. [Log Format](#log-format)
  4. [Process Monitoring](#process-monitoring)
3. [Dependencies](#dependencies)

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
  "log": "/path/to/log",
  "format": "log format (optional, defaults to the syslog format)",
  "name": "name (optional)"
}
```

This will return:

```json
{
  "id": "log id",
  "log": "/path/to/log",
  "format": "log format",
  "name": "log name"
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
  "logs": ["ids", ...]
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
  "id": "log id",
  "log": "/path/to/log",
  "format": "log format",
  "name": "log name"
}
```

To remove a specific log:

```http
DELETE /system/log/:id HTTP/1.1
```

### Log Format

Logs can be formatted with a similar syntax to the rsyslog format.

Examples:

* RFC5424 format: `<%PRI%> %TIMESTAMP% %HOSTNAME% %syslogtag%%msg%`
* Debian format: `%TIMESTAMP% %HOSTNAME% %syslogtag% %msg%`

Formatters (surrounded with `%`):

* `msg` The message part of the log.
* `rawmsg` The raw log message.
* `HOSTNAME` The hostname of the system which produced the message.
* `syslogtag` The process name (and potentially PID)
* `programname` The process name (not including PID)
* `PRI` The priority of the message
* `syslogfacility` 
* `syslogfacility-text`
* `syslogseverity`
* `syslogseverity-text`
* `timegenerated` The time the log message was generated
* `timereported` The time the log message was reported
* `TIMESTAMP` Alias for `timereported`

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
  "name": "process name",
  "pid": "process id (optional)",
  "logs": ["log id",...] (optional)
}
```

For a PID to function correctly the log format must include that information.

Returns:

```json
{
  "name": "process name",
  "pid": "process id",
  "logs": ["log id",...]
}
```

By default the logs will be those that are registed to `/system`.

Getting all processes monitored:

```http
GET /process HTTP/1.1
Accept: application/json
```
```json
{
  "processes": ["ps name",...]
}
```

Getting a specific process:

```http
GET /process/:id HTTP/1.1
Accept: application/json
```
```
{
  "name": "process name",
  "pid": "process id",
  "logs": ["log id",...]
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

Requires Python 2.7 and Python setuptools.

All other dependencies should be installed through setuptools:

* [Flask](http://flask.pocoo.org)
* [pyparsing 2.0.1](http://pyparsing.wikispaces.com)
