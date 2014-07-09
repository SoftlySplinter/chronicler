var tv4 = require('tv4');
var daemonSchema = require('../../definitions/daemon');
var daemon = require('../daemon.js');

function DaemonApi() {}

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
  
    if(!tv4.validate(req.body, daemonSchema)) {
      return next(new restify.InvalidContentError("Invalid daemon definition"));
    }
  
    try {
      res.json(201, daemon.create(req.body));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.get("/daemon/:name", function(req, res, next) {
    try {
      res.json(daemon.get(req.params.name));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.patch("/daemon/:name", function(req, res, next) {
    try {
      res.json(daemon.pause(req.params.name, req.body.pause));
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
  
  server.del("/daemon/:name", function(req, res, next) {
    try {
      daemon.del(req.params.name);
      res.send(200);
      return next();
    } catch (ex) {
      return next(new restify.InvalidContentError(ex.message));
    }
  });
}

module.exports = new DaemonApi();
