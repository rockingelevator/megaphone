var React = require('react');
var Notification = require('./notification');

module.exports = React.createClass({
	render: function(){
		var notificationNodes = this.props.data.map(function(notification){
			return (
				<Notification key={notification.id} author={notification.author_id} type={notification.type} creationDate={notification.creation_date}>
					{notification.message}
				</Notification>
			);
		});
		return (
			<ul>
				{notificationNodes}	
			</ul>
		);
	}
});