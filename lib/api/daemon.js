var tv4 = require('tv4');
var Daemon = require("../daemon");

function DaemonApi() { }

DaemonApi.schema = require('../../definitions/daemon');

DaemonApi.prototype.register = function(server) {
  server.post("/daemon", function(req, res, next) {
    if(!req.is('json')) {
      return next(new restify.InvalidContentError("Expected JSON"));
    }
    if(!tv4.validate(req.body, DaemonApi.schema)) {
      return next(new restify.InvalidContentError("Invalid daemon definition"));
    }
  
    try {
      res.json(201, Daemon.create(req.body));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.get("/daemon/:name", function(req, res, next) {
    daemon = Daemon.get(req.params.name);
    if(daemon === undefined) {
      return next(new restify.ResourceNotFoundError(req.params.name));
    }
    res.json(daemon);
    return next();
  });
  
  server.patch("/daemon/:name", function(req, res, next) {
    daemon = Daemon.get(req.params.name);
    if(daemon === undefined) {
      return next(new restify.ResourceNotFoundError("Daemon " + req.params.name + " does not exist"));
    }

    try {
      res.json(daemon.pause(req.params.pause));
    } catch(ex) {
      return next(ex);
    }
    return next();
  });
  
  server.del("/daemon/:name", function(req, res, next) {
    try {
      if(Daemon.get(req.params.name === undefined)) {
        return next(restify.ResourceNotFoundError(req.params.name));
      }
      Daemon.del(req.params.name);
      res.send(200);
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
}

DaemonApi.prototype.close = function() {
  Daemon.close();
}

module.exports = new DaemonApi();
