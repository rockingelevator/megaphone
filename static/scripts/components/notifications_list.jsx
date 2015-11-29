var React = require('react');
var Notification = require('./notification');

module.exports = React.createClass({
	render: function(){
		var myId = this.props.me;
		var notificationNodes = this.props.data.map(function(notification){
			return (
				<Notification key={notification.id} data={notification} userId={this.props.userId}/>
			);
		}.bind(this));
		return (
			<ul>
				{notificationNodes}
			</ul>
		);
	}
});