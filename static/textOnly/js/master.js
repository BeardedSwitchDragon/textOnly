

import util
$('.alert').alert()

var alphabetlist = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
var c = document.getElementById("canvas");
var ctx = c.getContext("2d");
var width = 100;
var height = 100;

function draw(event) {
    var mouseX = event.clientX;
    var mousey = event.clientY;
    ctx.fillRect(mousex - (width / 2), mousey - (height / 2), width, height);
}
