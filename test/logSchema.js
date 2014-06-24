fs = require("fs");
tv4 = require("tv4");

module.exports = {
  setUp: function(callback) {
    this.schema = JSON.parse(fs.readFileSync(__dirname + "/../definitions/log.json", "utf8"));
    this.valid = [
      { file: "/var/syslog" },
      { file: "/var/syslog", interval: 1000 }
    ];
    this.invalid = [
      {},
      { file: 100 },
      { file: "/var/syslog", interval: "1000" },
      { file: "/var/syslog", interval: -1 },
      { file: "/var/syslog", name: "System Log" },
      { file: "/var/syslog", interval: 1000, name: "System Log" }
    ];
    callback();
  },
  testValidDaemon: function(test) {
    test.expect(this.valid.length);
    this.valid.forEach(function(item) {
      test.ok(tv4.validate(item, this.schema));
    }, this);
    test.done();
  },
  testInvalidDaemon: function(test) {
    test.expect(this.invalid.length);
    this.invalid.forEach(function(item) {
      test.ok(!tv4.validate(item, this.schema), JSON.stringify(item) + " is not valid");
    }, this);
    test.done();
  }
}
