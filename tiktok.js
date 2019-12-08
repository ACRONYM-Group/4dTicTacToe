console.log("working :)");
var bx = 0;
var by = 0;
var sx = 0;
var sy = 0;

//Team
//Recieve Team status from server
function SetPlayerTeam(PlayerTeam) {
    var Team = document.getElementById("PlayerTeam");
    if (!PlayerTeam) {
        Team.innerHTML = "You are: X";
    } else if (PlayerTeam) {
        Team.innerHTML = "You are: O";
    } else {
        Team.innerHTML = "Oh god errors.";
    }
}

//Turn management
//Recieve turn status from server

var turn;

function SetTurnState(IsTurn) {
    var Turn = document.getElementById("PlayerTurn");
    if (IsTurn) {
        Turn.innerHTML = "It is your turn.";
    } else if (!IsTurn) {
        Turn.innerHTML = "It is the enemy's turn.";
    } else {
        Turn.innerHTML = "Oh god errors.";
    }
}

function CheckTurnState() {

}

//CheckWin
function CheckWinState() {

}

//Drawing
var canvas = document.getElementById("TicTacToe");
canvas.width = 325;
canvas.height = 325;

var ctx = canvas.getContext("2d");
var cx = 0;
var cy = 0;

var size = 25;

var drawx = 40;
var drawy = 40;

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

gridSeperation = 100;
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

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    cx = x;
    cy = y;
}

//Figuring out where you clicked
canvas.addEventListener("mousedown", function (e) {
    getCursorPosition(canvas, e);
    trackclick();
});

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

function DrawCircle(BigX, BigY, SmallX, SmallY) {
    ctx.beginPath();
    ctx.arc(27.5 + size * SmallX + gridSeperation * BigX, 27.5 + size * SmallY + gridSeperation * BigY, 9, 0, 2 * Math.PI);
    ctx.stroke();
    ws.send(JSON.stringify({
        cmdtype: "setCell",
        coords: [bx, by, sx, sy],
        val: "O"
    }));
}

function Fdrawx() {
    ctx.moveTo(bx * S2 + sx * S1 + 14, by * S2 + sy * S1 + 14);
    ctx.lineTo(bx * S2 + (sx + 1) * S1 + 14, by * S2 + (sy + 1) * S1 + 14);
    ctx.moveTo(bx * S2 + sx * S1 + 14, by * S2 + (sy + 1) * S1 + 14);
    ctx.lineTo(bx * S2 + (sx + 1) * S1 + 14, by * S2 + sy * S1 + 14);
    ctx.stroke();
    ws.send(JSON.stringify({
        cmdtype: "setCell",
        coords: [bx, by, sx, sy],
        val: "X"
    }));
}

var boole = false;
canvas.addEventListener("mousedown", function (e) {

    getCursorPosition(canvas, e);

    trackclick();
    if (bx % 1 == 0 && by % 1 == 0 && sx % 1 == 0 && sy % 1 == 0) {
        boole = !boole;
        SetPlayerTeam(boole)
        if (boole) {
            Fdrawx();
        } else {
            DrawCircle(bx, by, sx, sy);
        }
    } else {
        console.log("Cancelling draw move")
    }

});

//Networking
ws = new WebSocket("ws://127.0.0.1:8000");

ws.addEventListener("open", function (event) {
    ws.send(
        JSON.stringify({
            cmdtype: "login"
        })
    );
    ws.send(
        JSON.stringify({
            cmdtype: "setCell",
            coords: [0, 0, 0, 0],
            val: "X"
        })
    );
    ws.send(
        JSON.stringify({
            cmdtype: "getCell",
            coords: [0, 0, 0, 0]
        })
    );
    ws.send(
        JSON.stringify({
            cmdtype: "getCell",
            coords: [0, 1, 0, 0]
        })
    );
});

ws.addEventListener("message", function (event) {
    console.log("Message from server ", event.data);
});

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