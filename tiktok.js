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

var LineMax1 = 3;
var LineMax2 = LineMax1;
var BoardNum = 3;

var y = 10;
var hy = 0;
var T = 0;
var L = 0;
/*
for(l=0; l < BoardNum; l++){
for (i = 0; i < BoardNum; i++) {
for (x = 0; x < LineMax2; x++) {

    //vert line draw
    ctx.moveTo(x * 23.3 + 23.3 + T * 40 * LineMax1, L * 40 * LineMax1 );
    ctx.lineTo(x * 23.3 + 23.3 + T * 40 * LineMax1, 23.3 * LineMax1 + 23.3 + L * 40 * LineMax1);

// horizontal line draw
    ctx.moveTo(T * 40 * LineMax1, x * 23.3 + 23.3);
    ctx.lineTo(23.3 * LineMax1 + 23.3 + T * 40 * LineMax1, x * 23.3 + 23.3);
    ctx.stroke(); 
}
T++}

T = 0;
L++
}
*/
function drawGrid(x, y, size) {

    for (var i = 0; i < 2; i++) {
        ctx.moveTo(x+size*(i+1), y);
        ctx.lineTo(x+size*(i+1), y+size*3);
        ctx.stroke();

        ctx.moveTo(x, y+size*(i+1));
        ctx.lineTo(x+size*3, y+size*(i+1));
        ctx.stroke();
    }
    
}

gridSeperation = 100;
function projectTesseract(n, increment, gridSeperation, size) {
    ctx.strokeStyle = "#"+toString(n)+toString(increment)+"0000";
    console.log("#"+(n*5)+increment+"0000");
    if (size == undefined) {
        size = 25;
    }

    if (Math.floor(increment/2)-increment/2 == 0) {
        for (var x = 0; x < 3; x++) {
            y=0;
            drawGrid(15+gridSeperation*x, 15+gridSeperation*y, size);
        }
    }

    // if (Math.floor(increment/2)-increment/2 != 0) {
    //     for (var y = 0; y < 3; y++) {
    //         x=0;
    //         drawGrid(15+gridSeperation*x, 15+gridSeperation*y, size);
    //     }
    // }

    

    x=0;
    y=0;
    //drawGrid(x, y, gridSeperation, size*2);
    
    increment += 1;
    
    if (increment < n) {
        projectTesseract(n, increment, gridSeperation*3, size*3);
    }
}

projectTesseract(3, 1, 100, 25);
/*
for (var x = 0; x < 3; x++) {
    for (var y = 0; y < 3; y++) {
        drawGrid(15+gridSeperation*x, 15+gridSeperation*y, 25);
    }
}*/

