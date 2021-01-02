from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import re
import math

def do_ocr (reqtype, imgobj, x1, y1, x2, y2, canvwidth, canvheight, rollangle=0,
            brightnessrate=1.0, sharpnessrate=1.0, contrastrate=1.0, boxblur=0, enlargerate=2,
            hsa=0, vsa=0, langset='heb',onlynum=False):

    img = ImageEnhance.Color(imgobj).enhance(0.0) #turn black and white for OCR

    iniwidth = img.size[0]
    iniheight = img.size[1]

    increaselist = []

    if reqtype == 'firstrun':
        increaselist.append(0) #for the first run no increase for better ocr
    else:                      #for total run try to get better ocr
        increaselist.append(0)
        increaselist.append(0.01)
        increaselist.append(0.02)
        increaselist.append(0.03)
        increaselist.append(0.04)
    #

    for incr in increaselist: #increases of cropped image to catch the number

        x1 = x1*(1-incr)
        y1 = y1*(1-incr)
        x2 = x2*(1+incr)
        y2 = y2*(1+incr)

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

        if rollangle != 0:
            img = img.rotate(rollangle)
        else:
            pass
        #

        if hsa != 0 or vsa != 0:
            skew = (1, math.tan(hsa*math.pi/180), 0, math.tan(vsa*math.pi/180), 1, 0)

            img = img.transform((img.size[0], img.size[1]), Image.AFFINE, skew)
        else:
            pass
        #   

        #print("intial points: (%f, %f), (%f, %f)" % (x1,y1,x2,y2))

        img = img.crop((x1*iniwidth/canvwidth, y1*iniheight/canvheight, x2*iniwidth/canvwidth, y2*iniheight/canvheight))
        
        #img.show()
        #print("width: %i, height: %i" % (img.size[0], img.size[1]))

        img = img.resize((img.size[0]*enlargerate, img.size[1]*enlargerate))

        if brightnessrate < 0.0 or brightnessrate == 1.0:
            pass
        else:
            img = ImageEnhance.Brightness(img).enhance(brightnessrate)
        #

        if sharpnessrate < 0.0 or sharpnessrate == 1.0:
            pass
        else:
            img = ImageEnhance.Sharpness(img).enhance(sharpnessrate)
        #
    
        if contrastrate < 0.0 or contrastrate == 1.0:
            pass
        else:
            img = ImageEnhance.Contrast(img).enhance(contrastrate)
        #

        if boxblur < 0 or boxblur == 0:
            pass
        else:
            img = img.filter(ImageFilter.BoxBlur(boxblur))
        #    

        addlang = ''

        if langset != '' and langset.find('+',0,1) == -1: #prevent state of +'' or ++'...'
            addlang = '+' + langset
        
        elif langset != '':
            addlang = langset
        #

        ocr_str = pytesseract.image_to_string(img, lang='eng'+addlang, config='--psm 7')

        if onlynum == False: #if string is requested
            ocr_res = re.sub('[^a-zA-Z0-9א-ת_ -/,.]', '', ocr_str)
            ocr_res = re.sub('[/]', '-', ocr_res)
            ocr_res = re.sub('[,]', ' ', ocr_res)

        elif onlynum == True: #if number is requested
            ocr_res = re.sub(r'\D', '', ocr_str)
        #
        
        print(ocr_res)

        if ocr_res != '':
            break
        #
    #    
    return (ocr_res, img) #returns ocr string and image (which is needed for the first run)
#