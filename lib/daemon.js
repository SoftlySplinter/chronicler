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

Daemon.daemons = []

Daemon.create = function(daemon) {
  if(Daemon.daemons === undefined) { console.log("Fuck"); }
  if(Daemon.daemons[daemon.name] !== undefined) {
    throw new Error("Daemon already exists.");
  }
  Daemon.daemons[daemon.name] = new Daemon(daemon);
  return daemon;
}

Daemon.get = function(name) {
  d = Daemon.daemons[name]
  if(d === undefined) {
    throw new Error("No daemon");
  }
  return d;
}

Daemon.pause = function(name, pause) {
  return Daemon.get(name).pause(pause);
}

Daemon.del = function(name) {
  Daemon.daemons[name] = undefined;
}

Daemon.close = function() {
  Daemon.daemons = [];
}

module.exports = Daemon;
