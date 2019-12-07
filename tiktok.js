console.log("Working :)");
webSocket = new WebSocket("wss://www.scienceandpizza.com:8000", "protocolOne");

WebSocket.onopen = function (event) {
    WebSocket.send("Here's some text that the server is urgently awaiting!");
};

WebSocket.onmessage = function (event) {
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
    WebSocket.send(JSON.stringify(msg));

    // Blank the text input element, ready to receive the next line of text from the user.
    document.getElementById("text").value = "";
}

var canvas = document.getElementById("TicTacToe");
canvas.width = window.innerWidth*.95;
canvas.height = window.innerHeight*.95;

var ctx = canvas.getContext("2d");

var drawx = 40;
var drawy = 40;

var LineMax = 3;
var BoardNum = 3;

var y = 10;
var hy = 0;
var T = 0;

for (i = 0; i < BoardNum; i++) {
for (x = 0; x < LineMax; x++) {

    //vert line draw
    ctx.moveTo(x * 23.3 + 23.3 + T * 40 * LineMax, y);
    ctx.lineTo(x * 23.3 + 23.3 + T * 40 * LineMax, y + 23.3 * LineMax + 23.3);

// horizontal line draw
    ctx.moveTo(hy + T * 40 * LineMax, x * 23.3 + 33.3);
    ctx.lineTo(hy + 23.3 * LineMax + 23.3 + T * 40 * LineMax, x * 23.3 + 33.3);
    ctx.stroke(); 
}
T++
}
