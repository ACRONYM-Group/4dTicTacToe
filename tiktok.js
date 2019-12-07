console.log("Working :)");
webSocket = new WebSocket("wss://www.scienceandpizza.com:8000", "protocolOne");

exampleSocket.onopen = function (event) {
    exampleSocket.send("Here's some text that the server is urgently awaiting!");
};

exampleSocket.onmessage = function (event) {
    console.log(event.data);
}

function sendText() {
    // Construct a msg object containing the data the server needs to process the message from the chat client.
    var msg = {
        type: "message",
        text: document.getElementById("text").value,
        id: clientID,
        date: Date.now()
    };

    // Send the msg object as a JSON-formatted string.
    exampleSocket.send(JSON.stringify(msg));

    // Blank the text input element, ready to receive the next line of text from the user.
    document.getElementById("text").value = "";
}

var c = document.getElementById("TicTacToe");
c.width = window.innerWidth*.95;
c.height = window.innerHeight*.95;

var ctx = c.getContext("2d");
var drawx = 40;
var drawy = 40;
var Lmax = 8;

var y=10;
var hy = 0;
var T = 0;
var gridnum = 9;
for(i=0; i<gridnum; i++){
for (x=0; x<Lmax; x++) {
    //vert line draw
    ctx.moveTo(x*23.3+23.3+T*40*Lmax, y);
    ctx.lineTo(x*23.3+23.3+T*40*Lmax, y+23.3*Lmax+23.3);
// horizontal line draw
    ctx.moveTo(hy+T*40*Lmax, x*23.3+33.3);
    ctx.lineTo(hy+23.3*Lmax+23.3+T*40*Lmax, x*23.3+33.3);
    ctx.stroke(); 
}
T++
}
