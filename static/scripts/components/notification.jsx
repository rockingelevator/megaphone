var React = require('react');

module.exports = React.createClass({
    render: function(){
        return <li>
                 <p className="message">
                     <i className="icon-fire-station red"></i>
                     <span className="text">
                         <strong>{ this.props.type }</strong>&nbsp;&nbsp;
                         { this.props.children }
                     </span>
                 </p>
                </li>
    }
});