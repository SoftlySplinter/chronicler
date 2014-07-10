var tv4 = require('tv4');
var Daemon = require("../daemon");

function DaemonApi() { }

DaemonApi.schema = require('../../definitions/daemon');

DaemonApi.prototype.register = function(server) {
  server.get("/", function(req, res, next) {
    res.json({
      "Chronicler": "0.0.0"
    });
    return next();
  });
  
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
    try {
      res.json(Daemon.get(req.params.name));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.patch("/daemon/:name", function(req, res, next) {
    try {
      res.json(Daemon.pause(req.params.name, req.body.pause));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.del("/daemon/:name", function(req, res, next) {
    try {
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
