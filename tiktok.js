console.log("Working :)");
var c = document.getElementById("TicTacToe");
c.width = window.innerWidth*.95;
c.height = window.innerHeight*.95;

var ctx = c.getContext("2d");
var drawx = 40;
var drawy = 40;


var y=10;
var hy = 0;
var T = 0;
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