fs = require("fs");
tv4 = require("tv4");

module.exports = {
  setUp: function(callback) {
    this.schema = JSON.parse(fs.readFileSync(__dirname + "/../definitions/daemon.json", "utf8"));
    this.valid = [
      { name: "Chronicler" },
      { name: "Chronicler", interval: 1000 }
    ];
    this.invalid = [
      {},
      { interval: 1000 },
      { name: 250 },
      { n: "Chronicler" },
      { name: "Chronicler", interval: "1000" },
      { name: "Chronicler", other: "Blah" }
    ]
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
