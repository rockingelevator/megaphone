var connection = new WebSocket("ws://127.0.0.1:8080/api/ws/demo-team/notifications");

// When the connection is open, send some data to the server
connection.onopen = function () {
  connection.send('Ping'); // Send the message 'Ping' to the server
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error: ');
  console.log(error);
};

// Log messages from the server
connection.onmessage = function (e) {
  console.log('Server: ' + e.data);
  var result = document.getElementById('result');

  //result.innerHTML = result.innerHTML + "<br>" + e.data;
};

var makeEcho = function(){
  connection.send('Echo!');
};