restify = require('restify');
daemonApi = require('./api/daemon.js');

server = restify.createServer({
  "name": "Chronicler"
});

server.use(restify.bodyParser());

daemonApi.register(server);

server.listen(8080);

module.exports = server;
