var React = require('react');

module.exports = React.createClass({
   render: function(){
       return <a onClick={this.props.whenClicked} className="btn">
           {this.props.value}
       </a>
   }
});