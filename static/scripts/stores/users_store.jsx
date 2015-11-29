var Api = require('../utils/api.js');
var Reflux = require('reflux');

module.exports = Reflux.createStore({
   me: function(){
       return Api.get('/me').then(function(data){
           this.my = data;
       }.bind(this));
   }
});