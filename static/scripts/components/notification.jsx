var React = require('react');
var TypeBadge = require('./type_badge.jsx');
var moment = require('moment');

module.exports = React.createClass({
    render: function(){
        var time = moment(this.props.data.creation_date).calendar();
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
                </li>
    }
});