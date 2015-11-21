var React = require('react');
var TypeBadge = require('./type_badge.jsx');

module.exports = React.createClass({
    render: function(){
        return <li>
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