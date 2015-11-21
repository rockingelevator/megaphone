var React = require('react');

module.exports = React.createClass({
    render: function(){
        var iconClass;
        switch(this.props.type.toLowerCase()){
            case 'important':
                iconClass = "icon-fire-station red";
                break;
            case 'lunch':
                iconClass = "icon-restaurant yellow";
                break;
            case 'information':
                iconClass = "icon-megaphone-1 blue";
                break;
            case 'party':
                iconClass = "icon-glass pink";
                break;
        }
        return <i className={iconClass}>
        </i>
    }
});