var React = require('react');
var ReactDOM = require('react-dom');
var NotificationsList = require('./notifications_list');
var AddNotificationWidget = require('./add_notification');
var InfiniteScroll = require('./infinite_scroll')(React, ReactDOM);
var api = require('./api');


function getTeamSlug(url){
	var parser = document.createElement('a');
	parser.href = url;
	return parser.pathname.split('/')[1];
}

var App = React.createClass({
	getInitialState: function(){
		var parser = document.createElement('a');
		parser.href = document.URL;
		var team = parser.pathname.split('/')[1];
		return {
			meta: {
				offset: 0,
				limit: 20
			},
			items: [],
			hasMore: true,
			team: team
		};
	},
	loadMore: function(){
		api.get('/:team/notifications',
			{
				team: this.state.team,
				offset: this.state.meta.offset,
				limit: this.state.meta.limit
			},
			function(data){
				var hasMore = this.state.items.length < data.meta.total;
				data.meta.offset += this.state.meta.limit;
				this.setState({
					meta: data.meta,
					items: this.state.items.concat(data.items),
					hasMore: hasMore
				});
			}.bind(this)
		);
	},
	loader: function(){
		return <div>
			<p>
				<i className="icon-spin5 animate-spin">
				</i>
			</p>
		</div>
	},
	render: function(){
		return <div>
				<AddNotificationWidget team={this.state.team}/>
				<InfiniteScroll
					loadMore={this.loadMore}
					hasMore={this.state.hasMore}
					loader={this.loader()}
				>
					<NotificationsList data={this.state.items} />
				</InfiniteScroll>
			</div>
	}
});


ReactDOM.render(
	<App />,
	document.getElementById('content')
);

