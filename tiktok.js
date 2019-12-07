console.log("working :)");
//Networking
ws = new WebSocket("ws://127.0.0.1:8000");

ws.addEventListener('open', function (event) {
    ws.send(JSON.stringify({ cmdtype: "login" }));
});

ws.addEventListener('message', function (event) 
{
    console.log('Message from server ', event.data);
});

function sendText() 
{
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
var PlayerTeam = "X";

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
var IsTurn = "Yours";

var Turn = document.getElementById("PlayerTurn");
if (IsTurn == "Yours") 
{
    Turn.innerHTML = "It is your turn.";
}
else if (IsTurn == "Theirs") 
{
    Turn.innerHTML = "It is the enemy's turn.";
}
else 
{
    Turn.innerHTML = "Oh god errors.";
}

//Drawing
var canvas = document.getElementById("TicTacToe");
canvas.width = 325;
canvas.height = 325;

var ctx = canvas.getContext("2d");

var drawx = 40;
var drawy = 40;

var LineMax1 = 3;
var LineMax2 = LineMax1;
var BoardNum = 3;

function drawGrid(x, y, size) 
{

    for (var i = 0; i < 2; i++) 
    {
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
ctx.strokeStyle = "#FF0088";
for (var x = 0; x < 3; x++) 
{
    for (var y = 0; y < 3; y++) 
    {
        drawGrid(15+gridSeperation*x, 15+gridSeperation*y, 25);
    }
}

ctx.strokeStyle = "#FFFFFF";
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
