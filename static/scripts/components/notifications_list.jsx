var React = require('react');
var Notification = require('./notification');

module.exports = React.createClass({
	onremoved: function(id, index){
		this.props.onItemRemoved(id, index);
	},
	render: function(){
		var myId = this.props.me;
		var notificationNodes = this.props.data.map(function(notification, index){
			return (
				<Notification
						//key={notification.id}
						key={index}
						index={index}
						data={notification}
						userId={this.props.userId}
						whenRemoved={this.onremoved}
				/>
			);
		}.bind(this));
		return (
			<ul>
				{notificationNodes}
			</ul>
		);
	}
});