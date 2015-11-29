var React = require('react');
var TypeBadge = require('./type_badge.jsx');
var moment = require('moment');

module.exports = React.createClass({
    removeNotification: function(){
      this.props.whenRemoved(this.props.data.id, this.props.index);
    },
    render: function(){
        var time = moment(this.props.data.creation_date).calendar();
        var ava = "/static/img/avas/" + this.props.data.author.avatar;
        return <li>
                    <p className="time">
                        {time}
                    </p>
                    <p className="message">
                        <TypeBadge type={this.props.data.type}/>
                        <span className="text">
                            <strong>{ this.props.data.type }</strong>&nbsp;&nbsp;
                            { this.props.data.message }
                        </span>
                    </p>
                    <a className="ava">
                       <img src={ava}/>
                    </a>
                    <a
                        className={"ava remove " + (this.props.userId == this.props.data.author.id ? "show" : "")}
                        onClick={this.removeNotification}
                    >
                        <i className="icon-minus-circled">
                        </i>
                    </a>
                </li>
    }
});