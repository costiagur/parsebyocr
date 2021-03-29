from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import math
import tempfile
import cv2

def do_ocr (reqtype, imgobj, seekx1, seeky1, seekx2, seeky2, relx1, rely1, relx2, rely2, relimgaddress, canvwidth, canvheight, rollangle=0,
            brightnessrate=1.0, sharpnessrate=1.0, contrastrate=1.0, boxblur=0, enlargerate=2,
            hsa=0, vsa=0, langset='heb'):

    iniwidth = imgobj.size[0]
    iniheight = imgobj.size[1]

    #is both are 0, than no relative image was set. x1 and other coordinates stay as is

    if relimgaddress == '0':
        x1 = seekx1*iniwidth/canvwidth
        x2 = seekx2*iniwidth/canvwidth
        y1 = seeky1*iniheight/canvheight
        y2 = seeky2*iniheight/canvheight

        print("relative to zero (%i,%i),(%i,%i)" % (x1,y1,x2,y2))
    #
    else:  #search relative image using cv2
        picdir = tempfile.TemporaryDirectory()
        file = open(picdir.name + "\\imgobj.bmp", "w+b")
        imgobj.save(file)
        file.close()
        totcvimg = cv2.imread(picdir.name + "\\imgobj.bmp",0)        
        
        relcvimg = cv2.imread(relimgaddress,0)

        methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']
        
        methvals = list()
        methlocs = list()

        for meth in methods:
            method = eval(meth)
            matchres = cv2.matchTemplate(relcvimg,totcvimg,method)

            if meth == 'cv2.TM_SQDIFF_NORMED': #in this method best is minimum
                #print(cv2.minMaxLoc(matchres))
                methvals.append(1 - cv2.minMaxLoc(matchres)[0])
                methlocs.append(cv2.minMaxLoc(matchres)[2])
            else: #in this method maximum is best
                #print(cv2.minMaxLoc(matchres))
                methvals.append(cv2.minMaxLoc(matchres)[1]) 
                methlocs.append(cv2.minMaxLoc(matchres)[3])
            #
        #

        bestmatch = methvals.index(max(methvals)) #find the maximum matching correlation
        bestloc = methlocs[bestmatch] #best location based on the bestmatch
        
        picdir.cleanup()

        if bestmatch >0.8:
            x1 = seekx1/relx1*bestloc[0] 
            x2 = seekx2/relx1*bestloc[0]
            y1 = seeky1/rely1*bestloc[1]
            y2 = seeky2/rely1*bestloc[1] #relativity to the same upper left point

            print("relative point (%i,%i)" % (bestloc[0],bestloc[1]))
            print("relative cropping points (%i,%i),(%i,%i)" % (x1,y1,x2,y2))
        else:
            x1 = seekx1*iniwidth/canvwidth
            x2 = seekx2*iniwidth/canvwidth
            y1 = seeky1*iniheight/canvheight
            y2 = seeky2*iniheight/canvheight
        #
    #

    print("Final cropping points: (%i, %i), (%i, %i)" % (x1,y1,x2,y2))

    img = imgobj.crop((x1, y1, x2, y2))
    #img.show()
    img = ImageEnhance.Color(img).enhance(0.0) #turn black and white for OCR

    hsa = min(max(hsa,-90),90) #no less than -90, no more than 90
    vsa = min(max(vsa,-90),90)


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
      
    ocr_str = ocr_str.strip()

    ocr_str = ocr_str.replace('\n','')

    print(ocr_str)
  
    return (ocr_str, img) #returns ocr string and image (which is needed for the first run)
#