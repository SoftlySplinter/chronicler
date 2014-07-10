module.exports = process.env.CHRONICLER_COVERAGE
  ? require('./lib-cov/chronicler')
  : require('./lib/chronicler')

var main = function() {
  require('./').start();
}

if(require.main === module) {
  main();
}
