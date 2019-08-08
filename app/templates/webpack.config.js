const path = require('path');
const resolve = require('path').resolve;

const Webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackIncludeAssetsPlugin = require('html-webpack-include-assets-plugin');


module.exports = (env, argv) => {
  const prod = argv.mode === "production";

  return {
    devtool: !prod ? void 0 : "eval-source-map",
    entry: './src/index.jsx',
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader', 'shebang-loader']
        }
      ]
    },
    resolve: {
      extensions: ['*', '.js', '.jsx'],
    },
    plugins: [
      new Webpack.DefinePlugin({
        CESIUM_BASE_URL: JSON.stringify("/cesium")
      }),
      new CopyWebpackPlugin([
          {
            from: 'node_modules/cesium/Build/Cesium${prod ? "" : "Unminified"}',
            to: "cesium"
          } 
      ]),
      new HtmlWebpackPlugin({
        filepath: __dirname +  '/dist',
        template: 'index.html',
        scripts: ['cesium/Cesium.js']
      }),
      new HtmlWebpackIncludeAssetsPlugin({
        append: false,
        assets: ["cesium/Widgets/widgets.css", "cesium/Cesium.js"]
      })
    ],
    externals: {
      cesium: "Cesium"
    },
    output: {
      path: __dirname + '/dist',
      publicPath: '',
      filename: 'bundle.js',
    },
  };
}
