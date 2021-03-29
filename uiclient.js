ui = new Object();

ui.host = 'http://localhost:50113'

//********************************************************************************** */
window.addEventListener('beforeunload',function(event){ //when closing browser, close python
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request",'close'); //prepare files

    xhr.open('POST',ui.host, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);
        }
    };
    
    xhr.send(fdata);
    
})

//*********************************************************************************** */

ui.submit = function(reqtype){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    var areaarr = [];
    var relarr = [];

    const imcanv = document.getElementById('imcanv');

    var canvheight = imcanv.height; 
    var canvwidth = imcanv.width;

    var loadedfiles = document.getElementById("docfile").files

    areaclass = document.getElementsByClassName("area");
    relclass = document.getElementsByClassName("rel"); 

    for (let i=0; i < areaclass.length;i++){

        if (areaclass[i].dataset["area"+i] != ''){
            areaarr.push(areaclass[i].dataset["area"+i]);

            if(relclass[i].dataset["rel"+i] != ''){ //if areai exists, than check reli
                relarr.push(relclass[i].dataset["rel"+i]);
            }
            else{
                relarr.push('0,0,0,0') // in case relarea button was not clicked, insert 0,0,0,0. thus in any case relarea will be present 
            }
        }
    }

    if(areaarr.length == 0){ // in case no area button was clicked, "click" first area button 
        ui.insertpoint(0)
        areaarr.push(document.getElementById("area0").dataset.area0)
    }

    areastr = JSON.stringify(areaarr);
    relstr = JSON.stringify(relarr)

    console.log("areastr: "+ areastr);
    console.log("relstr: "+ relstr);

    fdata.append("request",'prepare'); //prepare files

    fdata.append("reqtype",reqtype); //test run ot total run

    fdata.append("areastr",areastr);
    
    fdata.append("relstr",relstr);

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

    //fdata.append("reshow",(document.getElementById("reshow").checked==true?1:0));

    fdata.append("docsnum", loadedfiles.length);

    for(let j=0; j < loadedfiles.length; j++){

        fdata.append("docfile" + j, loadedfiles[j]);
    }

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
                    
                    //console.log(this.responseText);

                    if(!this.responseText.startsWith("{")){
                        ui.showmodal("Error",this.responseText);
                        return;
                    }

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
    var loadedfiles = document.getElementById("docfile").files

    fdata.append("request",'preload'); //get first page for showing

    fdata.append("rollangle",document.getElementById("rollangle").value);

    fdata.append("hsa",document.getElementById("hsa").value);

    fdata.append("vsa",document.getElementById("vsa").value);

    console.log("loaddedfiles.length: " + loadedfiles.length);

    fdata.append("docfile0", loadedfiles[0]);
    
    xhr.open('POST',ui.host,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            
            document.getElementById("loader").style.display='none'; //close loader

            //console.log(this.responseText)

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
ui.insertpoint = function(num,type){

    var rgbarr = new Array(2);
    rgbarr[0] = new Array(3);
    rgbarr[1] = new Array(3);

    rgbarr[0][0] = 'rgba(51, 153, 51, 0.3)';
    rgbarr[0][1] = 'rgba(51, 204, 51, 0.3)';
    rgbarr[0][2] = 'rgba(102, 255, 51, 0.3)';

    rgbarr[1][0] = 'rgba(204, 0, 0, 0.3)';
    rgbarr[1][1] = 'rgba(230, 0, 0, 0.3)';
    rgbarr[1][2] = 'rgba(255, 0, 0, 0.3)';

    var imcanvmiddle = document.getElementById('imcanvmiddle');
    var ctxmid = imcanvmiddle.getContext('2d');
    
    var pointstr = document.getElementById("pointsxy").innerHTML;
    var pointarr = pointstr.split(",");

    ctxmid.clearRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1])
    ctxmid.fillStyle = rgbarr[type][num];
    ctxmid.fillRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1]);

    if(type==0){ //in case of area setting
        document.getElementById("area"+num).dataset["area"+num] = pointstr;
        document.getElementById("area"+num).style.color = rgbarr[type][num].slice(0,-4) + '1)';
    }
    else if(type==1){ //in case of relative point setting
        document.getElementById("rel"+num).dataset["rel"+num] = pointstr;
        document.getElementById("rel"+num).style.color = rgbarr[type][num].slice(0,-4) + '1)';
    }
}