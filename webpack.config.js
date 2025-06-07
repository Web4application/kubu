const path = require('path');

module.exports = {
mode: 'production',
entry: './src/index.js',
output: {
filename: 'bundle.js',
path: path.resolve(__dirname, 'dist'),
},
module: {
rules: [
{
test: /\.js$/,
exclude: /node_modules/,
use: {
loader: 'babel-loader',
},
},
],
},
optimization: {
minimize: true,
},
};

module.exports = {
mode: 'production',
entry: './src/index.js',
output: {
filename: 'bundle.js',
path: path.resolve(__dirname, 'dist'),
},
module: {
rules: [
{
test: /\.js$/,
exclude: /node_modules/,
use: {
loader: 'babel-loader',
options: {
presets: ['@babel/preset-env'],
},
},
},
],
},
optimization: {
minimize: true,
minimizer: [new TerserPlugin()],
},
};
