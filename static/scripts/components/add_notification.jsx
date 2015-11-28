var React = require('react');
var FancyButton = require('./fancy_btn');
var NotificationForm = require('./add_notification_form');

module.exports = React.createClass({
    getInitialState: function(){
        return {
            open: false
        };
    },
    openForm: function(){
        this.setState({open: !this.state.open});
    },
    render: function(){
       return <div>
            <p className="actions">
                <FancyButton
                    whenClicked={this.openForm} value={this.state.open ? "Cancel" : "Create notification"} iconClass={this.state.open ? "icon-minus" : "icon-plus-circled"}
                />
            </p>
            <NotificationForm team={this.props.team} connection={this.props.connection} isVisible={this.state.open ? "show" : ""} />
       </div>

    }
});