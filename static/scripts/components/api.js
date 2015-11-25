// url api helpers
var request = require('request-json');
var rootUrl = 'http://128.0.0.1:8080';
var apiPath = '/api';

function ParamException(message){
    this.message = message;
    this.name = 'ParamException';
};

ParamException.prototype = Error.prototype;

String.prototype.replaceKey=function(key, param) {
    key = ':' + key;
    return this.substr(0, this.indexOf(key)) + param + this.substr(this.indexOf(key)+key.length);
}

module.exports = {
    url: function(path, params){
        try {
            //checking if all required params are given
            var pathKeys = [];
            var query = '?';
            path.split(':').forEach(function(part){
                pathKeys.push(part.split('/')[0]);
            }) ;
            pathKeys.forEach(function(key){
                if(key != '' && !params.hasOwnProperty(key))
                    throw new ParamException('Path param ' + key + ' is required.');
            });

            for (param in params) {
                if (param.hasOwnProperty(length)) {
                    var end = param.length;
                }
                else {
                    throw new ParamException('Invalid param: ' + param);
                }
                var start = path.indexOf(':' + param);
                if (start > -1) {
                    path = path.replaceKey(param, params[param]);
                }
                else {
                    //else put param as query part
                    query += param + '=' + params[param] + '&';
                }
            }
            return (apiPath + path + query);
        }
        catch(e){
            console.log(e.message, e.name);
        }
    }
};

