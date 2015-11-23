var React = require('react');

module.exports = React.createClass({
   render: function(){
       var options = this.props.options.map(function(option, i){
          return <option key={"typeoption" + i} value={option}>
              {option}
          </option>
       });
       return <select className="textinput">
           {options}
           </select>
   }
});