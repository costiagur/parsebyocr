from pdf2image import convert_from_bytes
from io import BytesIO
from ocrit import ocrit
from tempfile import (TemporaryDirectory, NamedTemporaryFile)
import json
from base64 import b64encode
from relimg import relimg
from os import unlink

def testrun(scanfile, areastr, relstr, canvheight, canvwidth, rollangle='0', brightnessrate='1.0', contrastrate='1.0', enlargerate='2', 
    hsa='0', vsa='0', langset='heb'):

    canvheight = float(canvheight)
    canvwidth = float(canvwidth)
    rollangle = int(rollangle)
    brightnessrate = float(brightnessrate)
    sharpnessrate = 1.0
    contrastrate = float(contrastrate)
    boxblur = 0
    enlargerate = int(enlargerate)
    hsa = int(hsa)
    vsa = int(vsa)

    areadict = json.loads(areastr)
    reldict = json.loads(relstr)

    draftdir = TemporaryDirectory(ignore_cleanup_errors=True)

    resultdict = dict()

    for key in areadict: #keys 0-4
        relimgfile = NamedTemporaryFile(mode='w+b', delete=False)
        images = convert_from_bytes(scanfile, dpi=300, output_folder= draftdir.name,first_page=int(areadict[key][4]),last_page=int(areadict[key][4]),grayscale=True)

        print("firstrun - areadict[" + key + "] " + str(areadict[key]))
        print("firstrun - reldict[" + key + "] " + str(reldict[key]))
            
        relimgf = relimg(images[0],reldict[key][0],reldict[key][1],reldict[key][2],reldict[key][3],
                                    canvwidth,canvheight,relimgfile)

        relimgfile.close()
            
        testres, testimg, rellocfound = ocrit(images[0], 
                                        areadict[key][0],
                                        areadict[key][1],
                                        areadict[key][2],
                                        areadict[key][3],
                                        reldict[key][0],
                                        reldict[key][1],
                                        relimgf, 
                                        rollangle, 
                                        brightnessrate,
                                        sharpnessrate,
                                        contrastrate,
                                        boxblur,
                                        enlargerate,
                                        hsa, vsa,
                                        langset)
        
        unlink(relimgfile.name)
        
        imgpath = BytesIO()

        testimg.save(imgpath,'JPEG')

        imgpath.seek(0)

        imgpathres = b'data:image/jpeg;base64,' +  b64encode(imgpath.read())

        resultdict[key] = [testres, imgpathres.decode()] #dictinary of each area, with its ocr and its image path

        imgpath.close()
    #

    del images #destory images object

    draftdir.cleanup()

    return(json.dumps(resultdict).encode('UTF-8'))