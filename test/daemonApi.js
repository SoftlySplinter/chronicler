request = require('supertest');

module.exports = {
  setUp: function(callback) {
    this.chronicler = require("../");
    this.chronicler.start();

    this.existing = {
      post: {
        name: "Existing Daemon"
      },
      get: {
        name: "Existing Daemon",
        running: true,
        logs: [],
        callbacks: []
      }
    };
    request(this.chronicler.server)
    .post('/daemon')
    .send(this.existing.post)
    .expect(201, this.existing.post)
    .end(function(err, res) {
      if(err) {
        callback(err);
      }
      callback();
    });

  },
  tearDown: function(callback) {
    this.chronicler.close();
    callback();
  },
  testCreateValidDaemonReturns201: function(test) {
    testerDaemon = { name: 'tester' }
    request(this.chronicler.server)
    .post('/daemon')
    .send( testerDaemon )
    .expect(201, testerDaemon)
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testCreateInvalidDaemonReturns400: function(test) {
    request(this.chronicler.server)
    .post('/daemon')
    .send({})
    .expect(400, { code: 'InvalidContent', message: 'Invalid daemon definition' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testCreateDuplicateDaemonReturns400: function(test) {
    request(this.chronicler.server)
    .post('/daemon')
    .send( this.existing.post )
    .expect(400, { code: 'InvalidContent', message: 'Daemon already exists.' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testGetValidDaemonReturns200: function(test) {
    request(this.chronicler.server)
    .get('/daemon/' + this.existing.post.name)
    .expect(200, this.existing.get).end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  }
}
