var React = require('react');
var FancyButton = require('./fancy_btn');
var NotificationForm = require('./add_notification_form');

module.exports = React.createClass({
   render: function(){
       return <div>
            <p className="actions">
                <FancyButton value="Create Notification" iconClass="icon-plus-circled"/>
            </p>
            <NotificationForm />
       </div>

   }
});