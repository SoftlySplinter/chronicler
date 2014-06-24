restify = require('restify');
tv4 = require('tv4');
daemonSchema = require(__dirname + '/definitions/daemon');
daemon = require('./src/daemon.js');

server = restify.createServer({
  "name": "Chronicler"
});

server.use(restify.bodyParser());

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
  res.json(201, daemon.create(req.body));
  return next();
});

server.listen(8080);
