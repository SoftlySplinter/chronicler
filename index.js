module.exports = process.env.CHRONICLER_COVERAGE
  ? require('./lib-cov/chronicler')
  : require('./lib/chronicler')
