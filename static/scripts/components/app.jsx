var React = require('react');
var ReactDOM = require('react-dom');
var NotificationsList = require('./notifications_list');

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

ReactDOM.render(
	<NotificationsList data={notificationsData}/>,
	document.getElementById('notifications-list')
);