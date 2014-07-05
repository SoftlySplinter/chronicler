request = require('supertest');

module.exports = {
  setUp: function(callback) {
    this.chronicler = require("../chronicler.js");
    this.chronicler.listen(8080);
    callback();
  },
  tearDown: function(callback) {
    this.chronicler.close();
    callback();
  },
  testCreateValidDaemonReturns201: function(test) {
    testerDaemon = { name: 'tester' }
    request(this.chronicler)
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
    request(this.chronicler)
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
    testerDaemon = { name: 'duplicateTester' }
    request(this.chronicler)
    .post('/daemon')
    .send( testerDaemon )
    .expect(201, testerDaemon)
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
    });
    request(this.chronicler)
    .post('/daemon')
    .send( testerDaemon )
    .expect(400, { code: 'InvalidContent', message: 'Daemon already exists.' })
    .end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  },

  testGetValidDaemonReturns200: function(test) {
    request(this.chronicler).get('/daemon/tester')
    .expect(200, { 
      name: 'tester', 
      running: true, 
      logs: [], 
      callbacks: [] 
    }).end(function(err, res) {
      if(err) {
        test.ok(false, err.message);
      }
      test.done();
    });
  }
}
