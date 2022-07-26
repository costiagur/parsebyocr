from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import math
from io import BytesIO
import cv2
import numpy
import common

def ocrit (imgobj, seekx1, seeky1, seekx2, seeky2, relx1, rely1, relimgfile, rollangle=0,
            brightnessrate=1.0, sharpnessrate=1.0, contrastrate=1.0, boxblur=0, enlargerate=2, hsa=0, vsa=0, langset='heb'):

    try:
        seekx1 = float(seekx1)
        seeky1 = float(seeky1)
        seekx2 = float(seekx2)
        seeky2 = float(seeky2)
        relx1 = float(relx1)
        rely1 = float(rely1)

        rellocfound = 0

        picfile = BytesIO()
        imgobj.save(picfile,"JPEG")
        picfile.seek(0)

        totcvimg = cv2.imdecode(numpy.frombuffer(picfile.read(),numpy.uint8),0)               
            #cv2.imshow('ImageWindow', totcvimg)
            #cv2.waitKey()

        picfile.close()

        #imgtest = Image.open(relimgfile.name)

        with open(relimgfile.name,"rb") as fp:
            relcvimg = cv2.imdecode(numpy.frombuffer(fp.read(),numpy.uint8),0)
                #cv2.imshow('ImageWindow', relcvimg)
                #cv2.waitKey()
        #

        methods = [1,5] #cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED
            
        methvals = list()
        methlocs = list()

        for meth in methods:
            matchres = cv2.matchTemplate(relcvimg,totcvimg,meth)
            #print("Match matrix meth " + str(meth) + ": " + str(matchres))
            print("Match minmaxlol meth " + str(meth) + ": " + str(cv2.minMaxLoc(matchres)))


            if meth == 1: #in this method best is minimum
                methvals.append(1 - cv2.minMaxLoc(matchres)[0])
                methlocs.append(cv2.minMaxLoc(matchres)[2])

            else: #in this method maximum is best
                methvals.append(cv2.minMaxLoc(matchres)[1]) 
                methlocs.append(cv2.minMaxLoc(matchres)[3])
            #
        #

        bestmatch = methvals.index(max(methvals)) #find the maximum matching correlation

        bestloc = methlocs[bestmatch] #best location based on the bestmatch

        if max(methvals) >0.95:
            x1 = seekx1/relx1*bestloc[0] 
            x2 = seekx2/relx1*bestloc[0]
            y1 = seeky1/rely1*bestloc[1]
            y2 = seeky2/rely1*bestloc[1] #relativity to the same upper left point
            rellocfound = 1
            print("relative point (%i,%i)" % (bestloc[0],bestloc[1]))
            print("relative cropping points (%i,%i),(%i,%i)" % (x1,y1,x2,y2))
        else:
            return ('', b'',0)
        #
        

        print("Final cropping points: (%i, %i), (%i, %i)" % (x1,y1,x2,y2))

        img = imgobj.crop((x1, y1, x2, y2))
        #img.show()
        img = ImageEnhance.Color(img).enhance(0.0) #turn black and white for OCR

        hsa = min(max(hsa,-90),90) #no less than -90, no more than 90
        vsa = min(max(vsa,-90),90)


        if rollangle != 0:
            img = img.rotate(rollangle)
        #

        if hsa != 0 or vsa != 0:
            skew = (1, math.tan(hsa*math.pi/180), 0, math.tan(vsa*math.pi/180), 1, 0)
            img = img.transform((img.size[0], img.size[1]), Image.AFFINE, skew)
        #   
                
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
        
        ocr_str = ocr_str.strip()

        ocr_str = ocr_str.replace('\n','')

        print(ocr_str)
    
        return (ocr_str, img, rellocfound) #returns ocr string and image (which is needed for the first run)
    #
    except Exception as e:
        common.errormsg("Ocrit",e)
        return b'Error ' + str(e).encode('UTF-8')
    #
#