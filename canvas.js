var canv = new Object()
const imcanv = document.getElementById('imcanv');
canv.ctx = [];

canv.i=0;

canv.startx = 0;
canv.starty = 0;
canv.midx = 0;
canv.midy = 0;

canv.isdrawing = false


canv.mousedown = function(event){ //set first point of drawing
    
    if (canv.isdrawing == false){

        if(canv.i>0){
            canv.ctx[canv.i-1].beginPath(); 
            canv.ctx[canv.i-1].clearRect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);
            //delete previous drawing
        }

        canv.isdrawing = true;
    
        canv.ctx[canv.i] = imcanv.getContext('2d');
        canv.ctx[canv.i].fillStyle = 'rgba(153, 255, 153, 0.4)';

        canv.startx = event.offsetX;
        canv.starty = event.offsetY;
        canv.midx = canv.startx;
        canv.midy = canv.starty;
    }
}

canv.mousemove = function(event){ //while drawing. set last point of drawing
    if (canv.isdrawing == true) {

        canv.ctx[canv.i].beginPath();
        canv.ctx[canv.i].clearRect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);

        canv.midx = event.offsetX;
        canv.midy = event.offsetY;

        canv.ctx[canv.i].rect(canv.startx, canv.starty, canv.midx-canv.startx, canv.midy-canv.starty);
        canv.ctx[canv.i].fill();
        
        document.getElementById("pointsxy").innerHTML = canv.startx + "," + canv.starty + "," + event.offsetX + "," + event.offsetY;
    }
};
  
canv.mouseup = function(event) { //when stopped drawing
    if (canv.isdrawing == true) {

       
        canv.isdrawing = false;

        canv.i++;
    }
};

imcanv.onmousedown = canv.mousedown;
imcanv.onmousemove = canv.mousemove;
imcanv.onmouseup = canv.mouseup;

