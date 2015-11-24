var React = require('react');
var ReactDOM = require('react-dom');
var NotificationsList = require('./notifications_list');
var AddNotificationWidget = require('./add_notification');
var request = require('request-json');
var rootUrl = "http://127.0.0.1:8080";

function getTeamSlug(url){
	var parser = document.createElement('a');
	parser.href = url;
	return parser.pathname.split('/')[1];
};

var App = React.createClass({
	getInitialState: function(){
		return {
			meta: {},
			items: []
		};
	},
	componentDidMount: function(){
		var client = request.createClient(rootUrl);
		var team = getTeamSlug(document.URL);
		var nfApiUrl = '/api/' + team + '/notifications';
		client.get(nfApiUrl, function(err, res, data){
			if(!err){
				this.setState({meta: data.meta, items: data.items})
			}
		}.bind(this));
	},
	render: function(){
		return <div>
				<AddNotificationWidget />
				<NotificationsList data={this.state.items} />
			</div>
	}
});


ReactDOM.render(
	<App />,
	document.getElementById('content')
);

