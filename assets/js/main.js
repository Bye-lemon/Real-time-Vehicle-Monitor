/*
 * Main Javascript file for app.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
require('expose-loader?$!jquery');
require('font-awesome-webpack');
require('popper.js');
require('bootstrap');
require('d3');
require('expose-loader?Highcharts!highcharts');
require('highcharts/modules/map')(Highcharts);
require('highcharts/highcharts-more')(Highcharts);
require('expose-loader?Highcharts!highcharts/highstock');
require('expose-loader?io!socket.io-client');


// Your own code
require('./plugins.js');
require('./script.js');
