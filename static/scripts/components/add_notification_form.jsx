var React = require('react');
var Select = require('./select');

module.exports = React.createClass({
    getInitialState: function(){
      return {
          message: ''
      };
    },
    handleMessageChange: function(event){
        this.setState({message: event.target.value});
    },
    createNotification: function(){
        console.log('creating notification');
    },
    render: function(){
        var types = ["Important", "Lunch", "Information", "Party"]
        return <form className={"notification-form " + this.props.isVisible}>
            <Select options={types}/>
            <textarea
                className="textinput"
                defaultValue={this.state.message}
                onChange={this.handleMessageChange}
            >
            </textarea>
            <a onClick={this.createNotification} className="btn">Create notification</a>
        </form>
    }
});