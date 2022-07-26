ui = new Object();

ui.port = 50000

//********************************************************************************** */
window.addEventListener('beforeunload',function(event){ //when closing browser, close python
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request",'close'); //prepare files

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);
        }
    };
    
    xhr.send(fdata);
    
})
//********************************************************************************** */
window.addEventListener('load',function(event){
    ui.onloadfunc()
})
//******************************************************************************************** */

ui.onloadfunc = function(){

    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request",'invoicebyocr'); //parol

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);

            res = JSON.parse(xhr.responseText);

            ui.port = res.port;

            if(res.args != null){

                for(key of Object.keys(res.args)){

                    if (document.getElementById(key)){ //if such id doesn't exists, than object will return null which is false
            
                        document.getElementById(key).value = res.args[key];
                    }
                }           
            }
        }
    };
    
    xhr.send(fdata);
}

//*********************************************************************************** */
ui.submit = function(reqtype){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    const imcanv = document.getElementById('imcanv');

    var canvheight = imcanv.height; 
    var canvwidth = imcanv.width;

    var loadedfiles = document.getElementById("pdffiles_in").files

    var areaarr = {};
    var relarr = {};
    var namearr = [];
    var cutpagearr = [];
    var j=0;

    for (let i=0; i < 5 ;i++){ //assuming 5 fields. enlarge if added more

        let areadata = document.getElementById(`area${i}`).dataset["area"]
        let reldata = document.getElementById(`rel${i}`).dataset["rel"]

        if (areadata != ''){
            midarr = areadata.split(",")
            if (midarr[0]*1 > midarr[2]*1){
                let midval = midarr[0]
                midarr[0] = midarr[2]
                midarr[2] = midval
            }
            if (midarr[1]*1 > midarr[3]*1){
                let midval = midarr[1]
                midarr[1] = midarr[3]
                midarr[3] = midval
            }

            areaarr[j] = midarr;

            if(reldata != ''){ //if areai exists, than check reli
                midarr = reldata.split(",")
                if (midarr[0]*1 > midarr[2]*1){
                    let midval = midarr[0]
                    midarr[0] = midarr[2]
                    midarr[2] = midval
                }
                if (midarr[1]*1 > midarr[3]*1){
                    let midval = midarr[1]
                    midarr[1] = midarr[3]
                    midarr[3] = midval
                }
                                        
                relarr[j] = midarr;
            }
            else{
                alert(`Relative area was not set for ${i}th choise`); // in case relarea button was not clicked, insert 0,0,0,0. thus in any case relarea will be present 
                return;
            }
        
            if (document.getElementById(`nameby_${i}`).checked == true){
                namearr[j] = 1;
            }
            else{
                namearr[j] = 0;
            }

            if(document.getElementById(`selectpage_${i}`).checked == true){
                cutpagearr[j] = 1;
            }
            else{
                cutpagearr[j] = 0;
            }
            j++;
        }
    }

    if(areaarr.length == 0){ // in case no area button was clicked, "click" first area button 
        alert('Error: No fields were chosen')
        return
    }
    
    var areastr = JSON.stringify(areaarr);
    var relstr = JSON.stringify(relarr);
    var namestr = JSON.stringify(namearr);
    var cutpagestr = JSON.stringify(cutpagearr);

    console.log("areastr: "+ areastr);
    console.log("relstr: "+ relstr);
    console.log("namestr: "+ namestr);
    console.log("cutpagestr: "+ cutpagestr);

    fdata.append("request",reqtype); //test run ot total run

    //fdata.append("testpagenum_in",document.getElementById("testpagenum_in").value);

    fdata.append("areastr",areastr);
    
    fdata.append("relstr",relstr);

    fdata.append("canvheight",canvheight);

    fdata.append("canvwidth",canvwidth);

    fdata.append("rollangle",document.getElementById("rollangle").value);

    fdata.append("hsa",document.getElementById("hsa").value);

    fdata.append("vsa",document.getElementById("vsa").value);

    fdata.append("brightnessrate",Number(document.getElementById("brightnessrate").value)/10);

    fdata.append("contrastrate",Number(document.getElementById("contrastrate").value)/10);

    fdata.append("enlragerate",document.getElementById("enlragerate").value);

    fdata.append("lang",document.getElementById("lang").value);

    for(let i=0; i < loadedfiles.length; i++){
        fdata.append("pdffiles_"+ i, loadedfiles[i]);
    }

    fdata.append('namearr',namestr)
    fdata.append('cutpagearr',cutpagestr)   

    xhr.open('POST',"http://localhost:"+ui.port,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            
            document.getElementById("loader").style.display='none'; //close loader

            if(this.responseText.valueOf() < 1){
                alert('Error: ' + this.responseText);
                return;
            }
            else{
                if(reqtype == 'testrun'){
                    
                    //console.log(this.responseText);

                    if(!this.responseText.startsWith("{")){
                        alert("Error: " + this.responseText);
                        return;
                    }

                    let repobj = JSON.parse(this.responseText);

                    console.log(this.responseText)

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
    var loadedfiles = document.getElementById("pdffiles_in").files

    fdata.append("request",'preload');

    fdata.append("testpagenum_in",document.getElementById("testpagenum_in").value);

    fdata.append("rollangle",document.getElementById("rollangle").value);

    fdata.append("hsa",document.getElementById("hsa").value);

    fdata.append("vsa",document.getElementById("vsa").value);
    
    for(let i=0; i<loadedfiles.length; i++){
        fdata.append("pdffiles_" + i, loadedfiles[i]);    
    }
    
    xhr.open('POST',"http://localhost:"+ui.port,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            
            document.getElementById("loader").style.display='none'; //close loader

            //console.log(this.responseText)

            if(this.responseText.valueOf() < 1){
                alert('Error: ' + this.responseText);
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

//********************************************************************************************** */
ui.insertpoint = function(num,type){

    var rgbarr = new Array(2);

    rgbarr[0] = new Array(3);
    rgbarr[1] = new Array(3);

    rgbarr[0][0] = 'rgba(51, 153, 51, 0.3)';
    rgbarr[0][1] = 'rgba(51, 204, 51, 0.3)';
    rgbarr[0][2] = 'rgba(102, 255, 51, 0.3)';
    rgbarr[0][3] = 'rgba(153, 255, 51, 0.3)';
    rgbarr[0][4] = 'rgba(204, 255, 51, 0.3)';

    rgbarr[1][0] = 'rgba(204, 0, 0, 0.3)';
    rgbarr[1][1] = 'rgba(230, 0, 0, 0.3)';
    rgbarr[1][2] = 'rgba(250, 75, 0, 0.3)';
    rgbarr[1][3] = 'rgba(250, 112, 0, 0.3)';
    rgbarr[1][4] = 'rgba(250, 154, 0, 0.3)';

    var imcanvmiddle = document.getElementById('imcanvmiddle');
    var ctxmid = imcanvmiddle.getContext('2d');
    
    var pointstr = document.getElementById("pointsxy").innerHTML;
    var pointarr = pointstr.split(",");

    ctxmid.clearRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1])
    ctxmid.fillStyle = rgbarr[type][num];
    ctxmid.fillRect(pointarr[0], pointarr[1], pointarr[2]-pointarr[0], pointarr[3]-pointarr[1]);

    if(type==0){ //in case of area setting
        document.getElementById("area"+num).dataset["area"] = pointstr;
        document.getElementById("area"+num).style.color = rgbarr[type][num].slice(0,-4) + '1)';
    }
    else if(type==1){ //in case of relative point setting
        document.getElementById("rel"+num).dataset["rel"] = pointstr;
        document.getElementById("rel"+num).style.color = rgbarr[type][num].slice(0,-4) + '1)';
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


