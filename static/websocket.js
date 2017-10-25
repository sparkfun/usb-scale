console.log('hello');


var myWebsocket = new io.connect('http://localhost:5000');
myWebsocket.on('connect', function(evt) {console.log("Connection open ... ");});
myWebsocket.on('message', function(evt) {
    console.log(evt);
    });
myWebsocket.on('close', function(evt) {alert("Connection Closed");});