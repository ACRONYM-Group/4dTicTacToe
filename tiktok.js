console.log("working :)");
//Networking
ws = new WebSocket("ws://127.0.0.1:8000");
ws.onOpen = function (event) {
    console.log("Working :)");
    webSocket.send(json.stringify({cmdtype:"login"}));
};

setTimeout(function() {ws.send("Here's some text that the server is urgently awaiting!");}, 1000)


ws.onmessage = function (event) {
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
    ws.send(JSON.stringify(msg));

    // Blank the text input element, ready to receive the next line of text from the user.
    document.getElementById("text").value = "";
}

//Team
//Recieve Team status from server
var PlayerTeam

var Team = document.getElementById("PlayerTeam");
if(PlayerTeam == "X")
{
    Team.innerHTML = "You are: X";
}
else if(PlayerTeam == "O")
{
    Team.innerHTML = "You are: O";
}
else
{
    Team.innerHTML = "Oh god errors.";
}

//Turn management
//Recieve turn status from server
var IsTurn

var Turn = document.getElementById("PlayerTurn");
if (IsTurn == "Yours") {
    Turn.innerHTML = "It is your turn.";
}
else if (IsTurn == "Theirs") {
    Turn.innerHTML = "It is the enemy's turn.";
}
else {
    Turn.innerHTML = "Oh god errors.";
}

//Drawing
var canvas = document.getElementById("TicTacToe");
canvas.width = window.innerWidth*.30;
canvas.height = window.innerHeight*.35;

var ctx = canvas.getContext("2d");

var drawx = 40;
var drawy = 40;

var LineMax1 = 3;
var LineMax2 = LineMax1;
var BoardNum = 3;

var y = 10;
var hy = 0;
var T = 0;
<<<<<<< HEAD
for(i=0; i<3; i++){
for (x=0; x<2; x++) {
    ctx.moveTo(x*23.3+23.3+T*80, y);
    ctx.lineTo(x*23.3+23.3+T*80, y+70);
//jordan is a normal sized bitch
//does ian even do anything?
    ctx.moveTo(hy+T*80, x*23.3+33.3);
    ctx.lineTo(hy+70+T*80, x*23.3+33.3);
    ctx.stroke(); 
}
T++
}
=======
var L = 0;
function drawGrid(x, y, size) {

    for (var i = 0; i < 2; i++) {
        ctx.beginPath();
        ctx.moveTo(x+size*(i+1), y);
        ctx.lineTo(x+size*(i+1), y+size*3);
        ctx.stroke();

        ctx.moveTo(x, y+size*(i+1));
        ctx.lineTo(x+size*3, y+size*(i+1));
        ctx.stroke();
    }
    
}

gridSeperation = 100;
ctx.strokeStyle = "#FF0000";
for (var x = 0; x < 3; x++) {
    for (var y = 0; y < 3; y++) {
        drawGrid(15+gridSeperation*x, 15+gridSeperation*y, 25);
    }
}

ctx.strokeStyle = "#0000FF";
drawGrid(x, y, gridSeperation, 50);



/*var MousePosX = 0;
var MousePosY = 0;
function GetMousePos(event) {
    if(!(event.clientX && event.clientY == "undefined"))
    {
        MousePosX = event.clientX;
        MousePosY = event.clientY;
        console.log("X: " + MousePosX);
        console.log("Y: " + MousePosX);
    }

document.addEventListener("click", GetMousePos);

GetMousePos();*/
>>>>>>> dddf3c1ae8159e0b5e69d227c0c6e38bfef072c4
