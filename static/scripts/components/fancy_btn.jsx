var React = require('react');

module.exports = React.createClass({
    render: function(){
        return <a className="btn fancy">
                    <i className={this.props.iconClass}>
                    </i>
                    {this.props.value}
                </a>
    }
});