var React = require('react');
var Select = require('./select');
var api = require('./api');

module.exports = React.createClass({
    componentDidMount: function(){

    },
    getInitialState: function(){
      return {
          type: '',
          message: ''
      };
    },
    handleMessageChange: function(event){
        this.setState({message: event.target.value});
    },
    createNotification: function(){
        api.post('/:team/notifications', {
            team: this.props.team
        },{
            type: this.state.type,
            message: this.state.message
        }, function(data){
            console.log('Post succeed: ', data);
        });
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
                defaultValue={this.state.message}
                onChange={this.handleMessageChange}
            >
            </textarea>
            <a onClick={this.createNotification} className="btn">Create notification</a>
        </form>
    }
});