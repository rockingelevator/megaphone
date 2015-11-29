var React = require('react');
var ReactDOM = require('react-dom');
var NotificationsList = require('./notifications_list');
var AddNotificationWidget = require('./add_notification');
var InfiniteScroll = require('./infinite_scroll')(React, ReactDOM);
var Api = require('../utils/api');
var NotificationsStore = require('../stores/notifications_store');
var UsersStore = require('../stores/users_store');

function getTeamSlug(url){
	var parser = document.createElement('a');
	parser.href = url;
	return parser.pathname.split('/')[1];
}

module.exports = React.createClass({

	componentDidMount: function(){
		// When the connection is open, send some data to the server
		this.state.connection.onopen = function () {
		  this.state.connection.send('Ping'); // Send the message 'Ping' to the server
		}.bind(this);

		// Log errors
		this.state.connection.onerror = function (error) {
		  console.log('WebSocket Error: ');
		  console.log(error);
		};

		// Log messages from the server
		this.state.connection.onmessage = function (e) {
			var nfData = JSON.parse(e.data);
			if(nfData && nfData.id){
				var items = this.state.items;
				items.unshift(nfData);
				var meta = this.state.meta;
				meta.offset += 1;
				this.setState({
					items: items,
					meta: meta
				});
			}
		}.bind(this);

		$(window).unload(function(){
			console.log('closing connection');
			this.state.connection.close();
		}.bind(this));
	},
	getInitialState: function(){
		var parser = document.createElement('a');
		parser.href = document.URL;
		var team = parser.pathname.split('/')[1];

		return {
			meta: {
				offset: 0,
				limit: 20,
				user_id: false
			},
			items: [],
			hasMore: true,
			team: team,
			connection: new WebSocket("ws://127.0.0.1:8080/api/ws/" + team + "/notifications"),
		};
	},
	loadMore: function(){
		NotificationsStore.getNotifications(this.state.team, this.state.meta.offset, this.state.meta.limit)
			.then(function(){
				var data = NotificationsStore.notifications;
				var hasMore = this.state.items.length < data.meta.total;
				data.meta.offset += this.state.meta.limit;
				this.setState({
					meta: data.meta,
					items: this.state.items.concat(data.items),
					hasMore: hasMore
				});
			}.bind(this));
	},
	loader: function(){
		return <div>
			<p>
				<i className="icon-spin5 animate-spin">
				</i>
			</p>
		</div>
	},
	removeNotification: function(id, index){
		NotificationsStore.removeNotification(id, function(data){
			if('id' in data){
				this.state.items.splice(index, 1);
				this.forceUpdate();
			}
			else {
				console.log(data.error);
			}
		}.bind(this));
	},
	render: function(){
		return <div>
				<AddNotificationWidget
						team={this.state.team}
						connection={this.state.connection}
				/>
				<InfiniteScroll
					loadMore={this.loadMore}
					hasMore={this.state.hasMore}
					loader={this.loader()}
				>
					<NotificationsList
							data={this.state.items}
							userId={this.state.meta.user_id}
							onItemRemoved={this.removeNotification}
					/>
				</InfiniteScroll>
			</div>
	}
});