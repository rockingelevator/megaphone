var React = require('react');
var Select = require('./select');
var Button = require('./button');

module.exports = React.createClass({
    render: function(){
        var types = ["Important", "Lunch", "Information", "Party"]
        return <form className="notification-form" action="/api/demo-team/notifications/add" method="POST">
            <Select options={types}/>
            <textarea className="textinput">
            </textarea>
            <Button value="Create notification"/>
        </form>
    }
});