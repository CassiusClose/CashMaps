const resolve = require('path').resolve;

const config = {
  entry: './src/index.jsx',
  module: {
    rules [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    path: resolve('../static'),
    publicPath: resolve('../static'),
    fliename: 'bundle.js'
  }
};

module.exports = config;
