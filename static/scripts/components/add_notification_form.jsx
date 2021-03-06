var React = require('react');
var Select = require('./select');
var Api = require('../utils/api');
var NotificationsStore = require('../stores/notifications_store.jsx');

module.exports = React.createClass({
    getInitialState: function(){
      return {
          type: 'Important',
          message: ''
      };
    },
    handleMessageChange: function(event){
        this.setState({message: event.target.value});
    },
    createNotification: function(){
        var nf = {
            type: this.state.type,
            message: this.state.message
        };
        this.props.connection.send(JSON.stringify(nf));
        this.setState({message: ''});
        this.props.onPost();
    },
    handleTypeChanged: function(event){
      this.setState({type: event.target.value});
    },
    render: function(){
        var types = ["Important", "Lunch", "Information", "Party"];
        return <form className={"notification-form " + this.props.isVisible}>
            <Select whenChanged={this.handleTypeChanged} options={types}/>
            <textarea
                className="textinput"
                value={this.state.message}
                onChange={this.handleMessageChange}
            >
            </textarea>
            <a onClick={this.createNotification} className="btn">Create notification</a>
        </form>
    }
});