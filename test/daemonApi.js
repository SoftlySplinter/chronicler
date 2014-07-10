request = require('supertest');

module.exports = {
  setUp: function(callback) {
    this.chronicler = require("../");
    this.chronicler.start();

    this.existing = {
      name: "Existing Daemon",
      post: function() {
        return {
          name: this.name
        };
      },
      get: function(running) {
        return {
          name: "Existing Daemon",
          running: running !== undefined ? running : true,
          logs: [],
          callbacks: []
        };
      }
    };

    request(this.chronicler.server)
    .post('/daemon')
    .send(this.existing.post())
    .expect(201, this.existing.post())
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
    .send( this.existing.post() )
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
    .get('/daemon/' + this.existing.name)
    .expect(200, this.existing.get()).end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testGetInvalidDaemonReturns404: function(test) {
    request(this.chronicler.server)
    .get('/daemon/undefined')
    .expect(404)
    .end(function(err, res) {
      if(err) { 
        test.ok(false, err.message); 
      }
      test.done();
    });
  },

  testPauseValidDaemonReturns200: function(test) {
    request(this.chronicler.server)
    .patch('/daemon/' + this.existing.name)
    .send({ pause: true })
    .expect(200, this.existing.get(false))
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testPausePausedDaemonReturns400: function(test) {
    request(this.chronicler.server)
    .patch('/daemon/' + this.existing.name)
    .send({ pause: false })
    .expect(400, { code: 'InvalidContent', message: 'Already running' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testPauseInvalidDaemonReturns404: function(test) {
    request(this.chronicler.server)
    .patch('/daemon/undefined')
    .send( {pause: true} )
    .expect(404, { code: 'ResourceNotFound', message: 'undefined' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testPatchDaemonWithInvalidDataReturns400: function(test) {
    request(this.chronicler.server)
    .patch('/daemon/' + this.existing.name)
    .send( { foo: 'bar' })
    .expect(400, { code: 'InvalidContent', message: 'Pause flag not set' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testDeleteValidDaemonReturns200: function(test) {
    request(this.chronicler.server)
    .del('/daemon/' + this.existing.name)
    .expect(200, {})
    .end(function(err, res) {
      if(err) { test.ok(false, err.message) }
      test.done();
    });
  },

  testDeleteInvalidDaemonReturns404: function(test) {
    request(this.chronicler.server)
    .del('/daemon/undefined')
    .expect(404, { code: "ResourceNotFound", message: "undefined" })
    .end(function(err, res) {
      if(err) { test.ok(false, err.message) }
      test.done();
    });
  },
}
