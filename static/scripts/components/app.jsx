var React = require('react');
var ReactDOM = require('react-dom');
var NotificationsList = require('./notifications_list');

notificationsData = [
	{
		id: 1,
		team: 1,
		author: {
			id: 1,
			first_name: 'Eugene',
			last_name: 'Coltraine',
			avatar: 'eugene.png'
		},
		type: 'Important',
		message: 'First notification!',
		creation_date: new Date()
	},
	{
		id: 2,
		team: 1,
		author: {
			id: 2,
			first_name: 'Helga',
			last_name: 'Simone',
			avatar: 'helga.png'
		},
		type: 'Lunch',
		message: 'Second notification!',
		creation_date: new Date()
	}
];

ReactDOM.render(
	<NotificationsList data={notificationsData}/>,
	document.getElementById('notifications-list')
);