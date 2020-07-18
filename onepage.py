from PIL import Image
from pdf2image import convert_from_bytes
import os
import math
import random

def onepage(scanfile, rollangle=0, hsa=0, vsa=0, dpirate=400):

    os.makedirs(name='demo', exist_ok=True)
    os.makedirs(name='drafts', exist_ok=True)
    
    images = convert_from_bytes(scanfile, dpi=dpirate, 
                                output_folder=".\\drafts", single_file=True)

    hsa = int(hsa)
    vsa = int(vsa)
    rollangle = int(rollangle)

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
                                  skew
                                  )
    # 

    random.seed()

    randnum = str(random.randint(1000,10000))

    imgnew.save('demo\\' + randnum + '.png')

    print('demo\\' + randnum + '.png')

    for entry in os.scandir(r'.\drafts'):
        os.unlink(entry.path)
    #    

    return randnum  
#