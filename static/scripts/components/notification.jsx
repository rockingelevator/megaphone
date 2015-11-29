var React = require('react');
var TypeBadge = require('./type_badge.jsx');
var moment = require('moment');

module.exports = React.createClass({
    componentWillMount: function(){

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
                    <a className={"ava remove " + (this.props.userId == this.props.data.author.id ? "show" : "")}>
                        <i className="icon-minus-circled">
                        </i>
                    </a>
                </li>
    }
});