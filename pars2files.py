from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import re
import os
import random
import json
import math
import zipfile
import base64
from pdf2image import (convert_from_path, convert_from_bytes)
import PyPDF2
import io

#********************************* DO OCR *************************************************************

def do_ocr (reqtype, img, x1, y1, x2, y2, rollangle=0, hsa=0, vsa=0,
            brightnesse=1.0, sharpnesse=1.0, contraste=1.0, boxblur=0):

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
            imgrolled = img.rotate(rollangle)
        else:
            imgrolled = img
        #

        if hsa != 0 or vsa != 0:
            skew = (1, math.tan(hsa*math.pi/180), 0, math.tan(vsa*math.pi/180), 1, 0)

            imgskew = imgrolled.transform((imgrolled.size[0], imgrolled.size[1]),
                                         Image.AFFINE,
                                         skew
                                         )
        else:
            imgskew = imgrolled
        #   
        
        imgcrop = imgskew.crop((x1*imgskew.size[0], 
                                y1*imgskew.size[1],
                                x2*imgskew.size[0],
                                y2*imgskew.size[1]
                                )
                               )

        imglarge = imgcrop.resize((imgcrop.size[0]*5, imgcrop.size[1]*5))

        imgcolor = ImageEnhance.Color(imglarge).enhance(0.0) #turn black and white


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

        ocr_nums = re.sub(r'\D', '', ocr_str)

        if ocr_nums != '':
            break
        #
    #    
    return (ocr_nums, img_blur)
#

#************************ MAIN FUNCTION *********************************************************************

def pars2files(reqtype, scanfile, x1, y1, x2, y2, rollangle, hsa, vsa,
                brightnesse, sharpnesse, contraste, boxblur, dpirate=400,
                pagesin="1"):

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

    rollangle = int(rollangle)
    hsa = int(hsa)
    vsa = int(vsa)
    brightnesse = float(brightnesse)
    sharpnesse = float(sharpnesse)
    contraste = float(contraste)
    boxblur = int(boxblur)
    
    #**************************************************************

    if reqtype=='firstrun':

        os.makedirs(name='drafts',exist_ok=True)
        os.makedirs(name='mid',exist_ok=True)

        images = convert_from_bytes(scanfile,dpi=dpirate,
                                    output_folder=".\\drafts",
                                    single_file=True)

        firstnum,firstimg = do_ocr(reqtype, images[0], x1, y1, x2, y2, 
                                   rollangle, hsa, vsa,brightnesse,
                                   sharpnesse, contraste, boxblur)

        random.seed()

        randnum = str(random.randint(1000, 10000))

        firstimg.save('mid\\' + randnum + '.png')
                        #random number needed for js to update the test image

        repdict = dict()

        repdict["firstnum"] = firstnum

        repdict["firstimg"] = '.\\mid\\' + randnum + '.png' 

        for entry in os.scandir(r'.\drafts'):
            os.unlink(entry.path)
        #

        msg = json.dumps(repdict)

        return msg.encode() 
    #
    #*******************************************************************************

    elif reqtype=='totalrun':

        os.makedirs(name='drafts', exist_ok=True)
        os.makedirs(name='result', exist_ok=True)

        reqpagesl = pagesin.split(",")

        pdfReaderObj = PyPDF2.PdfFileReader(io.BytesIO(scanfile))

        numofpages = pdfReaderObj.numPages

        #imageslist = convert_from_bytes(scanfile, dpi=dpirate,
        #                                output_folder=".\\drafts")
                                        #turn pdf to list of images

        if len(reqpagesl) == 1: #if user requested each X page which is the step below

            start = 1
            i=start
            step = int(reqpagesl[0])

            pagenumlist = []

            while i<= numofpages:
                 
                pagenumlist.append(i)

                i=i+step
            #
        
        else:            
            pagenumlist = [1] #take 1 as first value anyway
            
            reqpagesl.sort()

            i = 1 if int(reqpagesl[0])==1 else 0 
                    #if first in pagenumlist is 1 than dont take it again     

            while i < len(reqpagesl):
                 
                if int(reqpagesl[i]) > numofpages: #page cannot be larger len(imageslist)
                    pagenumlist.append(numofpages)
                    break

                else: 
                    pagenumlist.append(int(reqpagesl[i])) #add requested page number to pagelist
                    i=i+1
                #
            #

            pagenumlist.sort()
        #

        print(pagenumlist)

        for pagenum in pagenumlist: #for each page to be taken

            num_in_list = pagenum-1

            pdfpage = pdfReaderObj.getPage(num_in_list) #get page

            pdfWriterObj = PyPDF2.PdfFileWriter() # 1 convert page object into pdf file to convert it to img later

            pdfWriterObj.addPage(pdfpage) # 2
            
            pdfOutputFile = open(r'.\\drafts\mid.pdf', 'wb') # 3
            
            pdfWriterObj.write(pdfOutputFile) # 4
            
            pdfOutputFile.close() # 5

            img = convert_from_path(r'.\\drafts\mid.pdf', dpi=dpirate, output_folder=".\\drafts", single_file=True) #get its image

            res = do_ocr(reqtype, img[0], x1, y1, x2, y2, rollangle, hsa, vsa,
                        brightnesse, sharpnesse, contraste, boxblur)

            pdfWriterObj = PyPDF2.PdfFileWriter()

            pdfWriterObj.addPage(pdfpage) #add pdf page to resulting pdf file. saved farther.

            if len(reqpagesl) == 1:
                till = min(num_in_list + step,numofpages)
                            #take no more than last index in imageslist
            
            else:
                if pagenum < pagenumlist[-1]: 
                            #if it is not the last value in pagenumlist
                    till = min(
                                pagenumlist[pagenumlist.index(pagenum)+1]-1,
                                numofpages
                              ) 
                            #take the next param in list but no more than last page in imageslist
                
                else:
                    till = numofpages
                #
            #

            if till-num_in_list > 1: 
                            # in case there should be several pages in resulting pdf
                i=0
                
                for i in range(num_in_list+1,till,1):
                    pdfWriterObj.addPage(pdfReaderObj.getPage(i))
                #                
            #

            pdfOutputFile = open('result\\' + str(pagenum) + "_" + res[0] + '.pdf', 'wb')
            
            pdfWriterObj.write(pdfOutputFile)
            
            pdfOutputFile.close()

            print(res[0])
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

        randnum = str(random.randint(1000, 10000))

        zipname = randnum + '.zip'

        resf = zipfile.ZipFile(file = zipname, mode='a')

        for entry in os.scandir(r'.\result'):
            if entry.name.find('.pdf') != -1:
                resf.write(entry)
            #
            os.unlink(entry.path)
        #

        resf.close()

        with open(zipname,mode='rb') as resfile:
            resread = resfile.read()
        #
        
        resf64 = base64.b64encode(resread)

        os.unlink(zipname)

        return resf64
        
    #
#