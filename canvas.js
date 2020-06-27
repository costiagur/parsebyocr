var canv = new Object()
const imcanv = document.getElementById('imcanv');
canv.ctx = [];

canv.i=0;

canv.startx = 0;
canv.starty = 0;
canv.midx = 0;
canv.midy = 0;

canv.isdrawing = false


canv.mousedown = function(event){
    
    if (canv.isdrawing == false){

        if(canv.i>0){
            canv.ctx[canv.i-1].beginPath();
            canv.ctx[canv.i-1].clearRect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);
        }

        canv.isdrawing = true;
    
        canv.ctx[canv.i] = imcanv.getContext('2d');
        canv.ctx[canv.i].fillStyle = 'rgba(153, 255, 153, 0.4)';

        canv.startx = event.offsetX;
        canv.starty = event.offsetY;
        canv.midx = canv.startx;
        canv.midy = canv.starty;
           
        document.getElementById("startx").innerHTML = canv.startx
        document.getElementById("starty").innerHTML = canv.starty
    }
}

canv.mousemove = function(event){
    if (canv.isdrawing == true) {

        canv.ctx[canv.i].beginPath();
        canv.ctx[canv.i].clearRect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);

        canv.midx = event.offsetX;
        canv.midy = event.offsetY;

        canv.ctx[canv.i].rect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);
        canv.ctx[canv.i].fill();
        
        document.getElementById("endx").innerHTML = event.offsetX
        document.getElementById("endy").innerHTML = event.offsetY
    }
};
  
canv.mouseup = function(event) {
    if (canv.isdrawing == true) {

       
        canv.isdrawing = false;

        canv.i++;
    }
};

imcanv.onmousedown = canv.mousedown;
imcanv.onmousemove = canv.mousemove;
imcanv.onmouseup = canv.mouseup;

