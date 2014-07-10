var restify = require("restify");

function Daemon(details) {
  this.name = details.name;
  this.running = true;
  this.logs = [];
  this.callbacks = [];
}

Daemon.prototype.pause = function(pause) {
  if(this.running != pause) {
    throw new restify.InvalidArgumentError("Already in that state");
  }
  this.running = !pause;
  return this;
}

Daemon.daemons = []

Daemon.create = function(daemon) {
  if(Daemon.daemons[daemon.name] !== undefined) {
    throw new Error("Daemon already exists.");
  }
  Daemon.daemons[daemon.name] = new Daemon(daemon);
  return daemon;
}

Daemon.get = function(name) {
  return Daemon.daemons[name]
}

Daemon.del = function(name) {
  Daemon.daemons[name] = undefined;
}

Daemon.close = function() {
  Daemon.daemons = [];
}

module.exports = Daemon;
