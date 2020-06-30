from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import re
import os
import random
import json
import math
from pdf2image import (convert_from_path, convert_from_bytes)

def do_ocr (img,x1,y1,x2,y2,hsa=0,vsa=0,colore=0.0,brightnesse=1.0,sharpnesse=1.0,contraste=1.0,boxblur=0):

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

    if hsa != 0 or vsa != 0:
        skew = (1,math.tan(hsa*math.pi/180),0,math.tan(vsa*math.pi/180),1,0)

        imgskew = img.transform((img.size[0],img.size[1]),Image.AFFINE,skew)
    else:
        imgskew = img
    #   
    
    imgcrop = imgskew.crop((x1*imgskew.size[0],y1*imgskew.size[1],x2*imgskew.size[0],y2*imgskew.size[1]))

    imglarge = imgcrop.resize((imgcrop.size[0]*5,imgcrop.size[1]*5))

    if colore < 0.0 or colore == 1.0:
        imgcolor = imglarge
    else:
        imgcolor = ImageEnhance.Color(imglarge).enhance(colore)
    #


    if brightnesse < 0.0 or brightnesse == 1.0:
        imgbright = imgcolor
    else:
        imgbright = ImageEnhance.Brightness(imgcolor).enhance(brightnesse)
    #


    if sharpnesse < 0.0 or sharpnesse == 1.0:
        imgsharp = imgbright
    else:
        imgsharp = ImageEnhance.Sharpness(imgbright).enhance(sharpnesse)
    #
 

    if contraste < 0.0 or contraste == 1.0:
        imgcontrast = imgsharp
    else:
        imgcontrast = ImageEnhance.Contrast(imgsharp).enhance(contraste)
    #

 
    if boxblur < 0 or boxblur == 0:
        img_blur = imgcontrast
    else:
        img_blur = imgcontrast.filter(ImageFilter.BoxBlur(boxblur))
    #    

    ocr_str = pytesseract.image_to_string(img_blur, lang='heb+eng', config='--psm 7')

    ocr_nums = re.sub(r'\D','',ocr_str)

    return (ocr_nums,img_blur)
#

def pars2files(reqtype,scanfile,x1,y1,x2,y2,hsa,vsa,colore,brightnesse,sharpnesse,contraste,boxblur,dpirate=400):

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    if x2 < x1: #if the picture was chosen backwards
        midval = x2
        x2 = x1
        x1 = midval
    #

    if y2 < y1: #if the picture was chosen backwards
        midval = y2
        y2 = y1
        y1 = midval
    #

    hsa = int(hsa)
    vsa = int(vsa)
    colore = float(colore)
    brightnesse = float(brightnesse)
    sharpnesse = float(sharpnesse)
    contraste = float(contraste)
    boxblur = int(boxblur)
    
    if reqtype=='firstrun':

        os.makedirs(name='drafts',exist_ok=True)
        os.makedirs(name='mid',exist_ok=True)

        images = convert_from_bytes(scanfile,dpi=dpirate,output_folder=".\\drafts",single_file=True)

        firstnum,firstimg = do_ocr(images[0],x1,y1,x2,y2,hsa,vsa,colore,brightnesse,sharpnesse,contraste,boxblur)

        random.seed()

        randnum = str(random.randint(1000,10000))

        firstimg.save('mid\\' + randnum + '.png') #random number needed for js to update the test image

        repdict = dict()

        repdict["firstnum"] = firstnum

        repdict["firstimg"] = '.\\mid\\' + randnum + '.png' 

        for entry in os.scandir(r'.\drafts'):
            os.unlink(entry.path)
        #

        return json.dumps(repdict)
    #
    
    elif reqtype=='totalrun':

        i=1

        os.makedirs(name='drafts',exist_ok=True)
        os.makedirs(name='result',exist_ok=True)

        images = convert_from_bytes(scanfile,dpi=dpirate,output_folder=".\\drafts")

        for img in images:

            res = do_ocr(img,x1,y1,x2,y2,hsa,vsa,colore,brightnesse,sharpnesse,contraste,boxblur)

            if res[0]=='':
                for incr in [0.01,0.02,0.04,0.05]:
                    res = do_ocr(img,x1*(1-incr),y1*(1-incr),x2*(1+incr),y2*(1+incr),hsa,vsa,colore,brightnesse,sharpnesse,contraste,boxblur)
                    if res[0] != '':
                        break                
                    #
                #
            #

            img.save('result\\' + str(i) + "_" + res[0] + '.pdf') #turn original img to pdf

            print(res[0])

            i = i + 1
        #

        for entry in os.scandir(r'.\mid'):
            os.unlink(entry.path)
        #

        for entry in os.scandir(r'.\demo'):
            os.unlink(entry.path)
        #

        for entry in os.scandir(r'.\drafts'):
            os.unlink(entry.path)
        #

        return '1'
    #
#