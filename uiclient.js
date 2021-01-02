ui = new Object();

ui.host = 'http://localhost:54293'

//*********************************************************************************** */

ui.submit = function(reqtype){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    var areaarr = [];

    const imcanv = document.getElementById('imcanv');

    var canvheight = imcanv.height; 
    var canvwidth = imcanv.width;

    areaclass = document.getElementsByClassName("area"); 

    for (let i=0; i < areaclass.length;i++){

        if (areaclass[i].dataset["area"+i] != ''){
            areaarr.push(areaclass[i].dataset["area"+i]);
        }
    }

    if(areaarr.length == 0){ // in case no area button was clicked, "click" first area button 
        ui.insertpoint(0)
        areaarr.push(document.getElementById("area0").dataset.area0)
    }

    areastr = JSON.stringify(areaarr);

    //console.log(areastr);

    fdata.append("request",'prepare'); //prepare files

    fdata.append("reqtype",reqtype); //test run ot total run

    fdata.append("areastr",areastr);

    fdata.append("canvheight",canvheight);

    fdata.append("canvwidth",canvwidth);

    //console.log("canvheight " + canvheight);
    //console.log("canvwidth " + canvwidth);

    fdata.append("rollangle",document.getElementById("rollangle").value);

    fdata.append("hsa",document.getElementById("hsa").value);

    fdata.append("vsa",document.getElementById("vsa").value);

    fdata.append("brightnessrate",Number(document.getElementById("brightnessrate").value)/10);

    fdata.append("contrastrate",Number(document.getElementById("contrastrate").value)/10);

    fdata.append("boxblur",document.getElementById("boxblur").value);

    fdata.append("lang",document.getElementById("lang").value);

    fdata.append("pagesin",document.getElementById("pagesin").value);

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
                    
                    console.log(this.responseText);

                    let repobj = JSON.parse(this.responseText);

                    for(i=0; i < Object.keys(repobj).length; i++){

                        if(repobj[i][1] != 0){
                            let canv = document.getElementById('rescanv' + i)
                            let ctx = canv.getContext("2d");
                            let img = new Image();

                            document.getElementById("ocr" + i).innerHTML = repobj[i][0];
        
                            img.addEventListener('load', function() {
                                ctx.clearRect(0,0,canv.width,canv.height) //clear existing picture
        
                                ctx.drawImage(img,0,0,img.naturalWidth,img.naturalHeight,0,0,canv.width,canv.height) 
                              }, false);
                              
                            img.src = repobj[i][1];       
                        }    
                    }
                }

                else if(reqtype=='totalrun'){
                    ui.download('result.zip',this.responseText)
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

    fdata.append("rollangle",document.getElementById("rollangle").value);

    fdata.append("hsa",document.getElementById("hsa").value);

    fdata.append("vsa",document.getElementById("vsa").value);

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
                    
                    //console.log(img.src);

                    document.getElementById("firstrun_bt").disabled=false //enable buttons for further procedures
                    document.getElementById("totalrun_bt").disabled=false

                  }, false);

                img.src = this.responseText;  
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

//********************************************************************************************* */
ui.download = function(filename, filetext){

    var a = document.createElement("a");

    document.body.appendChild(a);

    a.style = "display: none";

    a.href = 'data:application/octet-stream;base64,' + filetext;

    a.download = filename;

    a.click();

    document.body.removeChild(a);

}

//********************************************************************************************** */
ui.insertpoint = function(num){

    var rgbarr = []

    rgbarr[0] = 'rgba(51, 153, 51, 0.3)'
    rgbarr[1] = 'rgba(51, 204, 51, 0.3)'
    rgbarr[2] = 'rgba(102, 255, 51, 0.3)'
    rgbarr[3] = 'rgba(204, 255, 51, 0.3)'
    rgbarr[4] = 'rgba(204, 204, 0, 0.3)'

    var imcanvmiddle = document.getElementById('imcanvmiddle');
    var ctxmid = imcanvmiddle.getContext('2d');
    
    var pointstr = document.getElementById("pointsxy").innerHTML;
    var pointarr = pointstr.split(",");

    ctxmid.clearRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1])
    ctxmid.fillStyle = rgbarr[num];
    ctxmid.fillRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1]);

    document.getElementById("area"+num).dataset["area"+num] = pointstr;
    document.getElementById("area"+num).style.color = rgbarr[num].slice(0,-4) + '1)';
}