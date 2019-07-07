module.exports = {
  env: {
    browser: true,
    es6: true
  },
  parserOptions: {
    parser: 'babel-eslint',
    ecmaVersion: 2015,
    sourceType: 'module'
  },
  extends: [
    'plugin:vue/essential',
    'airbnb-base'
  ],
  plugins: [
    'vue'
  ],
  settings: {
    'import/resolver': {
      webpack: {
        config: 'webpack.config.js'
      }
    }
  },
  rules: {
    semi: [
      'error',
      'never'
    ],
    'comma-dangle': [
      'error',
      'never'
    ],
    'space-before-function-paren': [
      'error',
      'always'
    ],
    'import/extensions': [
      'error',
      'always',
      {
        js: 'never',
        vue: 'never'
      }
    ]
  }
}
