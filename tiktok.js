console.log("working :)");
ws = new WebSocket("ws://127.0.0.1:8000");

var loginToken = 0;

//Drawing
var bx = 0;
var by = 0;
var sx = 0;
var sy = 0;

var canvas = document.getElementById("TicTacToe");
canvas.width = 325;
canvas.height = 325;

var ctx = canvas.getContext("2d");
var cx = 0;
var cy = 0;

var size = 25;

var drawx = 40;
var drawy = 40;

var gridSeperation = 100;
var LineMax1 = 3;

var LineMax2 = LineMax1;
var BoardNum = 3;

function drawGrid(x, y, size) {
    for (var i = 0; i < 2; i++) {
        ctx.beginPath();
        ctx.moveTo(x + size * (i + 1), y);
        ctx.lineTo(x + size * (i + 1), y + size * 3);
        ctx.stroke();

        ctx.moveTo(x, y + size * (i + 1));
        ctx.lineTo(x + size * 3, y + size * (i + 1));
        ctx.stroke();
    }
}

ctx.strokeStyle = "#FF0088";
for (var x = 0; x < 3; x++) {
    for (var y = 0; y < 3; y++) {
        drawGrid(15 + gridSeperation * x, 15 + gridSeperation * y, size);
    }
}

ctx.strokeStyle = "#FFFFFF";
drawGrid(x, y, gridSeperation, size * 2);
var S2 = 100;
var S1 = 25;

//Tracking clicking
function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    cx = x;
    cy = y;
}

function trackclick() {
    for (bx = 0; bx < 3;) {
        if (cx < S2 * (bx + 1)) {
            bx += 1;
            bx *= 10;
        }
        bx++;
    }

    for (by = 0; by < 3;) {
        if (cy < S2 * (by + 1)) {
            by += 1;
            by *= 10;
        }
        by++;
    }

    if (bx == 11) {} else if (bx == 21) {
        cx -= 100;
    } else if (bx == 31) {
        cx -= 200;
    }

    if (by == 11) {} else if (by == 21) {
        cy -= 100;
    } else if (by == 31) {
        cy -= 200;
    }
    for (sx = 0; sx < 3;) {
        if (cx < S1 * (sx + 1) + 12) {
            sx += 1;
            sx *= 10;
        }
        sx++;
    }
    for (sy = 0; sy < 3;) {
        if (cy < S1 * (sy + 1) + 12) {
            sy += 1;
            sy *= 10;
        }
        sy++;
    }

    sx = (sx - 1) / 10 - 1;
    sy = (sy - 1) / 10 - 1;
    bx = (bx - 1) / 10 - 1;
    by = (by - 1) / 10 - 1;

    console.log("BX:" + bx + " BY:" + by + " SX:" + sx + " SY:" + sy);
}

//Drawing every circle or square
function DrawCircle(BigX, BigY, SmallX, SmallY) {
    ctx.beginPath();
    ctx.arc(27.5 + size * SmallX + gridSeperation * BigX, 27.5 + size * SmallY + gridSeperation * BigY, 9, 0, 2 * Math.PI);
    ctx.stroke();
}

function Fdrawx(BigX, BigY, SmallX, SmallY) {
    console.log(BigX)
    console.log(BigY)
    console.log(SmallX)
    console.log(SmallY)
    ctx.beginPath();
    ctx.moveTo(BigX * S2 + SmallX * S1 + 14, BigY * S2 + SmallY * S1 + 14);
    ctx.lineTo(BigX * S2 + (SmallX + 1) * S1 + 14, BigY * S2 + (SmallY + 1) * S1 + 14);
    ctx.moveTo(BigX * S2 + SmallX * S1 + 14, BigY * S2 + (SmallY + 1) * S1 + 14);
    ctx.lineTo(BigX * S2 + (SmallX + 1) * S1 + 14, BigY * S2 + SmallY * S1 + 14);
    ctx.stroke();
}

//On every click \/
canvas.addEventListener("mousedown", function (e) {

    getCursorPosition(canvas, e);

    trackclick();

    if (bx % 1 == 0 && by % 1 == 0 && sx % 1 == 0 && sy % 1 == 0) {
        console.log(loginToken);
        ws.send(JSON.stringify({
            cmdtype: "setCell",
            coords: [bx, by, sx, sy],
            val: PlayerTeamInternal,
            token: loginToken
        }));
    } else {
        console.log("Cancelling draw move")
    }

});

var PlayerTeamInternal = "";

//Team
//Recieve Team status from server at start of communication
function SetPlayerTeamText(PlayerTeam) {
    var TeamText = document.getElementById("PlayerTeam");
    PlayerTeamInternal = PlayerTeam;

    if (PlayerTeam == "X") {
        TeamText.innerHTML = "You are: X";
    } else if (PlayerTeam == "O") {
        TeamText.innerHTML = "You are: O";
    } else {
        TeamText.innerHTML = "Errors.";
    }
}

//Turn management
//Recieve turn status from server
function SetTurnState(Turn, Team) {
    const TurnState = document.getElementById("PlayerTurn");
    console.log(Turn.turn);
    console.log(Turn, Team);
    console.log(PlayerTeamInternal);

    if (Turn == Team) {
        TurnState.innerHTML = "It is your turn.";
    } else if ((Team == "X" && Turn.turn == "X") || (PlayerTeamInternal == "X" && Turn.turn == "X") || (PlayerTeamInternal == "X" && Turn == "X")) {
        TurnState.innerHTML = "It is your turn.";
    } else if ((Team == "O" && Turn.turn == "O") || (PlayerTeamInternal == "O" && Turn.turn == "O") || (PlayerTeamInternal == "O" && Turn == "O")) {
        TurnState.innerHTML = "It is your turn.";
    } else if (!(Turn == Team)) {
        TurnState.innerHTML = "It is the enemy's turn.";
    }
}

//Victory set
//Recieve victory condition from server
function SetWinState(Who) {
    const TurnState = document.getElementById("PlayerTurn");
    if (Who == PlayerTeamInternal) {
        TurnState.innerHTML = "Victory! You have won!";
    } else if (Who == "Tie") {
        TurnState.innerHTML = "Tie! No one won!";
    } else {
        TurnState.innerHTML = "Defeat! You have lost!";
    }
}

//Networking
ws.addEventListener("open", function (event) {
    ws.send(
        JSON.stringify({
            cmdtype: "login"
        })
    );
});

ws.addEventListener("message", function (event) {
    console.log("Message from server ", event.data);
    var msg = JSON.parse(event.data);
    console.log(msg);

    switch (msg["cmdtype"]) {
        //On Login/Websocket connection to server:
        case "loginResponse":
            loginToken = msg["token"];

            //Get team and send it to SetPlayerTeamText
            SetPlayerTeamText(msg["team"]);

            //Get turn and team and send it to SetTurnState
            SetTurnState(msg["turn"], msg["team"]);

            break;
        case "stateChange":

            SetTurnState(msg["turn"], msg["team"]);
            console.log(msg["turn"], msg["team"]);

            if (msg["val"] == "X") {
                Fdrawx(msg["coords"][0], msg["coords"][1], msg["coords"][2], msg["coords"][3])
            } else if (msg["val"] == "O") {
                DrawCircle(msg["coords"][0], msg["coords"][1], msg["coords"][2], msg["coords"][3])
            } else {
                console.log("borked");
            }
            console.log(msg["coords"]);
            console.log(msg["val"]);
            break;

        case "victoryEvent":
            SetWinState(msg["winner"])
            break;
    }
});

/*function sendText() {
    // Construct a msg object containing the data the server needs to process the message from the chat client.
    var msg = {
        type: "message",
        text: document.getElementById("text").value,
        id: clientID,
        date: Date.now()
    };

    // Send the msg object as a JSON-formatted string.
    ws.send(JSON.stringify(msg));
    switch (msg.type) {
        case "team":

            break;
        case "board changes":
            text = "<b>User <em>" + msg.name + "</em> signed in at " + timeStr + "</b><br>";
            break;
        case "win":
            text = "(" + timeStr + ") <b>" + msg.name + "</b>: " + msg.text + "<br>";
            break;
    }

    // Blank the text input element, ready to receive the next line of text from the user.
    document.getElementById("text").value = "";
}*/