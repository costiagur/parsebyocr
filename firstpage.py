from PIL import Image
from pdf2image import convert_from_bytes
import math
import tempfile
import base64
from io import BytesIO

def showfirstpage(scanfile, rollangle=0, hsa=0, vsa=0, dpirate=400): #mage image of the first page to display it in JS

    demofile = BytesIO()
    draftdir = tempfile.TemporaryDirectory()
    
    images = convert_from_bytes(scanfile, dpi=dpirate, 
                                output_folder= draftdir.name, single_file=True)

    if hsa > 90:
        hsa = 90
    elif hsa < -90:
        hsa = -90
    #
    if vsa > 90:
        vsa = 90
    elif vsa < -90:
        vsa = -90
    #

    imgnew = images[0]

    if rollangle != 0:
        imgnew = imgnew.rotate(rollangle)
    #

    if hsa != 0 or vsa != 0:
        skew = (1, math.tan(hsa*math.pi/180), 0, math.tan(vsa*math.pi/180), 1, 0)
        
        imgnew = imgnew.transform((imgnew.size[0], imgnew.size[1]),
                                  Image.AFFINE, 
                                  skew)
    # 

    imgnew.save(demofile, format = "PNG")
    
    demofile.seek(0)
    
    resimg = base64.b64encode(demofile.read())

    resimg = b'data:image/png;base64,' + resimg

    draftdir.cleanup()

    return resimg.decode()  
#