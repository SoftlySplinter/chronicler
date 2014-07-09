function Daemon(details) {
  this.name = details.name;
  this.running = true;
  this.logs = [];
  this.callbacks = [];
}

Daemon.prototype.pause = function(pause) {
  if(this.running != pause) {
    throw new Error("Already in that state");
  }
  this.running = !pause;
  return this;
}

function Daemons() {
  this.daemons = [];
}

Daemons.prototype.create = function(daemon) {
  if(this.daemons[daemon.name] !== undefined) {
    throw new Error("Daemon already exists.");
  }
  this.daemons[daemon.name] = new Daemon(daemon);
  return daemon;
}

Daemons.prototype.get = function(name) {
  d = this.daemons[name]
  if(d === undefined) {
    throw new Error("No daemon");
  }
  return d;
}

Daemons.prototype.pause = function(name, pause) {
  return this.get(name).pause(pause);
}

Daemons.prototype.del = function(name) {
  this.daemons[name] = undefined;
}

module.exports = new Daemons();
