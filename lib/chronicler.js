restify = require('restify');
bunyan = require('bunyan');

function Chronicler() {
  this.server = restify.createServer({
    "name": "Chronicler",
    "log": bunyan.createLogger({name: "Chronicler"})
  });
  this.daemonApi = require('./api/daemon.js');
  this.server.use(restify.bodyParser());
}


Chronicler.prototype.start = function() {
  this.daemonApi.register(this.server);
  this.server.listen(8080);
}

Chronicler.prototype.close = function() {
  this.server.close();
  this.daemonApi.close();
}

module.exports = new Chronicler();
