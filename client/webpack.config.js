const path = require('path');
const resolve = require('path').resolve;

const Webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackTagsPlugin = require('html-webpack-tags-plugin');


module.exports = (env, argv) => {
  //const prod = argv.mode === "production";
  const prod = false;

  return {
    devtool: !prod ? void 0 : "eval-source-map",
    entry: './src/index.jsx',
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader', 'shebang-loader']
        },
        {
          test: /\.css$/,
          exclude: /node_modules/,
          use: ['style-loader', 'css-loader']
        },
      ]
    },
    resolve: {
      extensions: ['*', '.js', '.jsx'],
    },
    plugins: [
      new Webpack.DefinePlugin({
        CESIUM_BASE_URL: JSON.stringify("cesium")
      }),
      /*      new CopyWebpackPlugin([
          {
            from: 'node_modules/cesium/Build/Cesium${prod ? "" : "Unminified"}',
            to: "cesium"
          } 
      ]),*/

      // Copy over Cesium resources to static folder
      new CopyWebpackPlugin([
          {
            from: 'node_modules/cesium/Build/CesiumUnminified',
            to: "cesium"
          } 
      ]),

      // Copy over jquery to static folder
      new CopyWebpackPlugin([
        {
          from: 'src/res/jquery-1.9.0.js',
          to: 'res'
        }
      ]),

      // Copy over React plugin resources to static folder
      new CopyWebpackPlugin([
        {
          from: 'node_modules/react-grid-layout/css/styles.css',
          to: 'res/react-grid-layout/css'
        }
      ]),
      new CopyWebpackPlugin([
        {
          from: 'node_modules/react-resizable/css/styles.css',
          to: 'res/react-resizable/css'
        }
      ]),

      // Sum all react files into one index.html file
      new HtmlWebpackPlugin({
        filepath: __dirname +  './../static',
        template: 'index.html',
      }),

      // Specifically link to styles and js files that aren't copied by
      // copy-webpack?
      new HtmlWebpackTagsPlugin({
        tags: ['cesium/Widgets/widgets.css', 'cesium/Cesium.js', 'res/jquery-1.9.0.js', 'res/react-grid-layout/css/styles.css', 'res/react-resizable/css/styles.css'],
        append: false
      })
    ],
    externals: {
      cesium: "Cesium",
      bufferutil: "BufferUtil"
    },
    output: {
      path: __dirname + './../server/cashmaps/static',
      publicPath: '',
      filename: 'bundle.js',
    },
  };
}
