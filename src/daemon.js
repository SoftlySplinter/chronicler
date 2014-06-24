
function Daemon(details) {
  this.name = details.name;
  this.running = true;
  this.logs = [];
  this.callbacks = [];
}

Daemon.prototype.pause = function(pause) {
  if(pause && !this.running) {
    throw new Error("Daemon is already paused");
  }
  if(!pause && this.running) {
    throw new Error("Daemon is already running");
  }

  this.running = pause;
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
  if(this.daemons[daemon.name] === undefined) {
    throw new Error("No daemon");
  }
  return this.daemons.get(name);
}

Daemons.prototype.pause = function(name, pause) {
  return this.get(name).pause();
}

Daemons.prototype.del = function(name) {
  daemon = get(name);
  daemons[name] = undefined;
  return daemon;
}

module.exports = new Daemons();
