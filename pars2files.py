from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import re
import os
import random
import json
from pdf2image import (convert_from_path, convert_from_bytes)

def do_ocr (img,x1,y1,x2,y2,colore=0.0,brightnesse=2.0,sharpnesse=1.0,boxblur=1):

    print('Color Ench. %s, Brightness Ench. %s, Sharpness Ench. %s, Blur radius. %s' %(colore,brightnesse,sharpnesse,boxblur))

    img_crop = img.crop((x1*img.size[0],y1*img.size[1],x2*img.size[0],y2*img.size[1]))

    img_large = img_crop.resize((img_crop.size[0]*5,img_crop.size[1]*5))

    img_color = ImageEnhance.Color(img_large).enhance(colore)

    img_bright = ImageEnhance.Brightness(img_color).enhance(brightnesse)

    img_sharp = ImageEnhance.Sharpness(img_bright).enhance(sharpnesse)

    img_blurred = img_sharp.filter(ImageFilter.BoxBlur(boxblur))

    ocr_str = pytesseract.image_to_string(img_blurred, lang='heb+eng', config='--psm 7')

    ocr_nums = re.sub(r'\D','',ocr_str)

    return (ocr_nums,img_blurred)
#

def pars2files(reqtype,scanfile,x1,y1,x2,y2,colore,brightnesse,sharpnesse,boxblur,dpirate=400):

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

    colore = float(colore)
    brightnesse = float(brightnesse)
    sharpnesse = float(sharpnesse)
    boxblur = int(boxblur)
    
    if reqtype=='firstrun':

        os.makedirs(name='drafts',exist_ok=True)
        os.makedirs(name='mid',exist_ok=True)

        images = convert_from_bytes(scanfile,dpi=dpirate,output_folder=".\\drafts",single_file=True)

        firstnum,firstimg = do_ocr(images[0],x1,y1,x2,y2,colore,brightnesse,sharpnesse,boxblur)

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

            res = do_ocr(img,x1,y1,x2,y2,colore,brightnesse,sharpnesse,boxblur)

            if res[0]=='':
                for bright in range(-10,10,5):
                    for sharp in range(-10,20,5):
                        res = do_ocr(img,x1,y1,x2,y2,colore,brightnesse+bright/5,sharpnesse+sharp/5,boxblur)
                        if res[0] != '':
                            break
                
                        #
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