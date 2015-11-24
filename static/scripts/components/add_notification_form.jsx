var React = require('react');
var Select = require('./select');
var Button = require('./button');

module.exports = React.createClass({
    createNotification: function(){
        console.log('creating notification');
    },
    render: function(){
        var types = ["Important", "Lunch", "Information", "Party"]
        return <form className={"notification-form " + this.props.isVisible}>
            <Select options={types}/>
            <textarea className="textinput">
            </textarea>
            <Button whenClicked={this.createNotification} value="Create notification"/>
        </form>
    }
});