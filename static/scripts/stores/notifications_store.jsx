var Api = require('../utils/api.js');
var Reflux = require('reflux');

module.exports = Reflux.createStore({
    getNotifications: function(team, offset, limit){
        return Api.get('/:team/notifications',
			{
				team: team || '',
				offset: offset || 0,
				limit: limit || 0
			}).then(function(data){
				    this.notifications = data;
				}.bind(this));
    },
	postNotification: function(team, data){
        return Api.post('/:team/notifications', {
            team: team
        }, data).then(function(data){
            this.postNfStatus = data;
        }.bind(this));
    },
    removeNotification: function(id, callback){
        return Api.remove('/notifications/:id', {id: id}, callback)
            .then(function(data){
                this.removeStatus = data;
            }.bind(this));
    }
});