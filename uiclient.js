ui = new Object();

ui.host = 'http://localhost:50000';

//*********************************************************************************** */

ui.submit = function(reqtype){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    const imcanv = document.getElementById('imcanv');

    var canvheight = imcanv.height; 
    var canvwidth = imcanv.width;

    var ratiox1 = Number(document.getElementById("startx").innerHTML)/canvwidth;
    var ratiox2 = Number(document.getElementById("endx").innerHTML)/canvwidth;
    var ratioy1 = Number(document.getElementById("starty").innerHTML)/canvheight;
    var ratioy2 = Number(document.getElementById("endy").innerHTML)/canvheight;

    console.log('ratiox1: ' + ratiox1)
    console.log('ratioy1: ' + ratioy1)
    console.log('ratiox2: ' + ratiox2)
    console.log('ratioy2: ' + ratioy2)

    fdata.append("request",'prepare'); //prepare files

    fdata.append("reqtype",reqtype); //test run ot total run

    fdata.append("ratiox1",ratiox1);

    fdata.append("ratioy1",ratioy1);

    fdata.append("ratiox2",ratiox2);

    fdata.append("ratioy2",ratioy2);

    fdata.append("colore",Number(document.getElementById("colore").value)/10);

    fdata.append("brightnesse",Number(document.getElementById("brightnesse").value)/10);

    fdata.append("sharpnesse",Number(document.getElementById("sharpnesse").value)/10);

    fdata.append("boxblur",document.getElementById("boxblur").value);

    fdata.append("dpirate",document.getElementById("dpirate").value);

    fdata.append("docfile",document.getElementById("docfile").files[0]);

    xhr.open('POST',ui.host,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            
            document.getElementById("loader").style.display='none'; //close loader

            if(this.responseText.valueOf() < 1){
                ui.showmodal('Error',this.responseText);
            }
            else{
                if(reqtype == 'firstrun'){

                    let repobj = JSON.parse(this.responseText);

                    document.getElementById("firstrun_num").innerHTML=repobj.firstnum;
                    
                    let firstrun_canv = document.getElementById("firstrun_canv")
                    let ctx = firstrun_canv.getContext("2d");
                    let img = new Image();

                    img.addEventListener('load', function() {
                        ctx.clearRect(0,0,firstrun_canv.width,firstrun_canv.height) //clear existing picture

                        ctx.drawImage(img,0,0,img.naturalWidth,img.naturalHeight,0,0,firstrun_canv.width,firstrun_canv.height) 
                      }, false);
                      
                    img.src = repobj.firstimg;       
                }

                else if(reqtype=='totalrun'){
                    ui.showmodal('Files Prepared','Files Prepared');
                    window.open('.\\result\\','_blank')
                }  
            }
       }
    };

    xhr.send(fdata);     
}

//*********************************************************************************** */

ui.preload = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    const imcanvback = document.getElementById('imcanvback');
    const ctx = imcanvback.getContext("2d");
    var canvheight = imcanvback.height; 
    var canvwidth = imcanvback.width;

    fdata.append("request",'preload'); //get first page for showing

    fdata.append("dpirate",document.getElementById("dpirate").value);

    fdata.append("docfile",document.getElementById("docfile").files[0]);

    xhr.open('POST',ui.host,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            
            document.getElementById("loader").style.display='none'; //close loader

            console.log(this.responseText)

            if(this.responseText.valueOf() < 1){
                ui.showmodal('Error',this.responseText);
            }
            else {
                var img = new Image();

                img.addEventListener('load', function() {
                    ctx.drawImage(img,0,0,img.naturalWidth,img.naturalHeight,0,0,canvwidth,canvheight)
                    
                    console.log(img.src);

                    document.getElementById("firstrun_bt").disabled=false //enable buttons for further procedures
                    document.getElementById("totalrun_bt").disabled=false

                  }, false);

                img.src = '.\\demo\\demopage.png'
                
            }
        }
    };

    xhr.send(fdata);     
}

//********************************************************************************************* */

ui.showmodal = function(header,body){

    document.getElementById("modal_out").style.display='block';

    document.getElementById("header_out").innerHTML = header;

    document.getElementById("body_out").innerHTML = body;

    if(body != ''){
        setTimeout(() => {
            document.getElementById("modal_out").style.display='none';
        },3000);
    }
}
