console.log("Working :)");
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
for(i=0; i<3; i++){
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