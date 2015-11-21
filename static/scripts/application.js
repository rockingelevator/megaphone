notificationsData = [
	{
		id: 1,
		team: 1,
		author_id: 1,
		type: 'Important',
		message: 'First notification!',
		creation_date: new Date()
	},
	{
		id: 2,
		team: 1,
		author_id: 1,
		type: 'Lunch',
		message: 'Second notification!',
		creation_date: new Date()
	}
];

var Notification = React.createClass({
    render: function(){
        return React.createElement("li", null, 
                 React.createElement("p", {className: "time"},  this.props.creationDate.strftime('%-H:%M') ), 
                 React.createElement("p", {className: "message"}, 
                     React.createElement("i", {className: "icon-fire-station red"}), 
                     React.createElement("span", {className: "text"}, 
                         React.createElement("strong", null,  this.props.type), "  ", 
                          this.props.children
                     )
                 )
                );
    }
});
var NotificationsList = React.createClass({displayName: "NotificationsList",
	render: function(){
		var notificationNodes = this.props.data.map(function(notification){
			return (
				React.createElement(Notification, {author: notification.author_id, type: notification.type, creationDate: notification.creation_date}, 
					notification.message
				)
			);
		});
		return (
			React.createElement("ul", null, 
				notificationNodes	
			)
		);
	}
});

ReactDOM.render(
	React.createElement(NotificationsList, {data: notificationsData}),
	document.getElementById('notifications-list')
);