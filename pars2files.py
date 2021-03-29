import os
import zipfile
from pdf2image import (convert_from_path, convert_from_bytes)
import PyPDF2
import io
import do_ocr
import tempfile
import json
import base64
import relimg
import re
import sys
 

def pars2files(reqtype, sourcelist, areadict, reldict, canvheight, canvwidth, 
    rollangle=0, brightnessrate=1.0, sharpnessrate=1.0, contrastrate=1.0, boxblur=0, enlargerate=2, 
    hsa=0, vsa=0, dpirate=400, pagesin="1", outdir = '', langset='heb', onlynum=False):

    canvheight = float(canvheight)
    canvwidth = float(canvwidth)
    rollangle = int(rollangle)
    brightnessrate = float(brightnessrate)
    sharpnessrate = float(sharpnessrate)
    contrastrate = float(contrastrate)
    boxblur = int(boxblur)
    enlargerate = int(enlargerate)
    dpirate = int(dpirate)
    hsa = int(hsa)
    vsa = int(vsa)

    titlestr = 'page,' #header row in resulting csv file
    key = 0
    for key in areadict: #take care of points if chosen backwards

        titlestr = titlestr + 'area' + str(key+1) + ',' #header row in resulting csv file

        midval = 0
        #print(areadict)

        if areadict[key][2] < areadict[key][0]: #if the picture was chosen backwards
            midval = areadict[key][2]
            areadict[key][2] = areadict[key][0]
            areadict[key][0] = midval
        #

        midval = 0

        if areadict[key][3] < areadict[key][1]: #if the picture was chosen backwards
            midval = areadict[key][3]
            areadict[key][3] = areadict[key][1]
            areadict[key][1] = midval
        #

        midval = 0

        if reldict[key][2] < reldict[key][0]: #if the picture was chosen backwards
            midval = reldict[key][2]
            reldict[key][2] = reldict[key][0]
            reldict[key][0] = midval
        #

        midval = 0

        if reldict[key][3] < reldict[key][1]: #if the picture was chosen backwards
            midval = reldict[key][3]
            reldict[key][3] = reldict[key][1]
            reldict[key][1] = midval
        #

    #

    titlestr = titlestr + 'link\n'

    #print(areadict)

    #*****************************************************************************

    if reqtype == 'firstrun': #first run is when user tests quality of ocr

        draftdir = tempfile.TemporaryDirectory()

        images = convert_from_bytes(sourcelist[0],dpi=dpirate,
                                    output_folder=draftdir.name,
                                    single_file=True) #converts only first page into image: single_file=True

        resultdict = dict()

        key = 0

        for key in areadict: #keys 0-4
            
            print("firstrun - areadict[key] " + str(areadict[key]))
            print("firstrun - reldict[key] " + str(reldict[key]))
            
            if reldict[key][0] == 0 and reldict[key][2] == 0:
                relimgaddress = '0'
            else:
                relimgaddress = relimg.relimg(images[0],reldict[key][0],reldict[key][1],reldict[key][2],reldict[key][3],
                                    canvwidth,canvheight,key,draftdir.name)
            #
            
            firstres, firstimg = do_ocr.do_ocr(reqtype, 
                                        images[0], 
                                        areadict[key][0],
                                        areadict[key][1],
                                        areadict[key][2],
                                        areadict[key][3],
                                        reldict[key][0],
                                        reldict[key][1],
                                        reldict[key][2],
                                        reldict[key][3],
                                        relimgaddress, 
                                        canvwidth,
                                        canvheight,
                                        rollangle, 
                                        brightnessrate,
                                        sharpnessrate,
                                        contrastrate,
                                        boxblur,
                                        enlargerate,
                                        hsa, vsa,
                                        langset)
        
            imgpath = io.BytesIO()
            firstimg.save(imgpath,'PNG')

            imgpath.seek(0)

            imgpathres = b'data:image/png;base64,' +  base64.b64encode(imgpath.read())

            if onlynum == True: #if number is requested
                firstres = re.sub(r'\D', '', firstres)
            #

            resultdict[key] = [firstres, imgpathres.decode()] #dictinary of each area, with its ocr and its image path
        #

        del images #destory images object

        draftdir.cleanup()

        return(json.dumps(resultdict))
    #
    #*******************************************************************************

    elif reqtype == 'totalrun':

        draftdir = tempfile.TemporaryDirectory()
        resdir = tempfile.TemporaryDirectory()
        #zipdir = tempfile.TemporaryDirectory()
        rescsvstr = ""
                
        rescsvstr += titlestr + "\n" # write header row into CSV file

        reslist = []
        relimglist = []

        ini_img = convert_from_bytes(sourcelist[0],dpi=dpirate,
                                    output_folder=draftdir.name,
                                    single_file=True) #converts only first page into image: single_file=True


        for key in list(reldict): #create list of addresses to images to be used later

            if reldict[key][0] == 0 and reldict[key][2] == 0:
                relimglist.insert(key,'0')
            else:
                pathrelimg = relimg.relimg(ini_img[0],reldict[key][0],reldict[key][1],reldict[key][2],reldict[key][3],
                                    canvwidth,canvheight,key,draftdir.name)

                relimglist.insert(key,pathrelimg)
            #
              
            print("relimglist " + str(key) + " - " + relimglist[key])
        #

        for docfile in sourcelist: #For each uploaded PDF file

            pagenumlist = [1] # in any case first page should be present

            i = 0

            pdfReaderObj = PyPDF2.PdfFileReader(io.BytesIO(docfile))

            numofpages = pdfReaderObj.numPages


            #create list of pages to cut at**********************************************

            if len(pagesin.split(",")) == 1: #if user requested each X page, like every page or every second page

                divisor = int(pagesin)
                #print('divisor: ' + str(divisor))

                #print('len(imageslist): ' + str(numofpages))

                for i in range(1,numofpages+1,1): 

                    #print('i: ' + str(i))   
                    
                    if i % divisor == 0 and (i+1) not in pagenumlist: #if devisable and not already in page list
                    
                        if i+1 <= numofpages:
                            pagenumlist.append(i+1) #divisable by 3, means pages 1,4,7, meaning 3+1, 6+1
                        #                                        #anyway not more that len(imagelist)
                    #
                #
            
            elif len(pagesin.split(",")) > 1: # if user requested an array of pages 
                
                pagesarr = pagesin.split(",")
                
                pagesarr = list(map(int,pagesarr)) # convert values to integers
                
                pagesarr.sort() # sort pages in ascending order     

                for i in pagesarr: #remake pagesarr, so that will include page 1 and last page be numofpages
                    
                    if i not in pagenumlist and i <= numofpages:
                        pagenumlist.append(i)

                    #
                #
            #

            #print(pagenumlist)

            #Get pages to OCR ***********************************************************

            for pagenum in pagenumlist: #for each page to be taken

                reslist.clear() #each row of CSV file is made as list to be joined later. Therefore clear it and start using.

                num_in_list = pagenum-1 #for index in list which start with 0

                pdfpage = pdfReaderObj.getPage(num_in_list) #get page

                pdfWriterObj = PyPDF2.PdfFileWriter() # 1 convert page object into pdf file to convert it to img later
                                                    # deirect ByteIO
                pdfWriterObj.addPage(pdfpage) # 2
                
                pdfOutputFile = open(draftdir.name + "\\mid.pdf", 'wb') # 3
                
                pdfWriterObj.write(pdfOutputFile) # 4
                
                pdfOutputFile.close() # 5

                img = convert_from_path(draftdir.name + "\\mid.pdf", dpi=dpirate, output_folder=draftdir.name, single_file=True) #get its image

                reslist.append(str(pagenum)) #first row in cell is page number

                for key in areadict: #for each selected area in the img

                    firstres, firstimg = do_ocr.do_ocr(reqtype,
                                    img[0],
                                    areadict[key][0],
                                    areadict[key][1],
                                    areadict[key][2],
                                    areadict[key][3],
                                    reldict[key][0],
                                    reldict[key][1],
                                    reldict[key][2],
                                    reldict[key][3],
                                    relimglist[key],
                                    canvwidth,
                                    canvheight,
                                    rollangle,
                                    brightnessrate,
                                    sharpnessrate,
                                    contrastrate,
                                    boxblur,
                                    enlargerate,
                                    hsa, vsa,
                                    langset)

                    if onlynum == True: #if number is requested
                        firstres = re.sub(r'\D', '', firstres)
                    #

                    print("totalrun -result- " + str(firstres))

                    reslist.append(str(firstres)) #each next cell in data row
                #
                
                print("initial filename: " + reslist[1])

                filename = re.sub('\W+', '_', reslist[1]) #file named by page num and second cell in each row

                print("final filename: " + filename)

                pagepath = resdir.name + '\\' + str(pagenum) + "_" + filename + '.pdf' 

                pdfWriterObj = PyPDF2.PdfFileWriter()

                pdfWriterObj.addPage(pdfpage) #add pdf page to resulting pdf file. saved farther.

                if pagenum < pagenumlist[-1]: #if it is not the last value in pagenumlist
                            
                    till = pagenumlist[pagenumlist.index(pagenum)+1]-1 #next page-1 in pagenumlist
                
                else:
                
                    till = numofpages #not to take last page - 1 but take the last page only
                #

                if till-num_in_list > 1: # in case there should be several pages in resulting pdf
                    
                    i=0
                    
                    for i in range(num_in_list+1,till,1):
                        pdfWriterObj.addPage(pdfReaderObj.getPage(i))
                    #
                #
                else:
                    pass # if each page to take that there is no appending of other images
                #

                pdfOutputFile = open(pagepath, 'wb')
                
                pdfWriterObj.write(pdfOutputFile)
                
                pdfOutputFile.close()

                reslist.append('=hyperlink("' + str(pagenum) + "_" + filename + '.pdf")')

                rescsvstr += ','.join(reslist) + '\n'

            #
        #

        with open(resdir.name + '\\result.csv',mode="w") as resultcsv: #create CSV file to store results. previous existing was removed
            resultcsv.write(rescsvstr)
        #        

        zipbite = io.BytesIO()

        zipres = zipfile.ZipFile(zipbite, mode='w')

        for entry in os.scandir(resdir.name):

            if entry.name.find('.pdf') != -1 or entry.name.find('.csv') != -1:
                
                zipres.write(entry,os.path.basename(entry.name))
            #
        #

        zipres.close()

        resdir.cleanup()

        try:
            draftdir.cleanup()
        except:
            for draftfile in os.scandir(draftdir.name):
                try:
                    os.unlink(draftfile)
                except:
                    print(sys.exc_info()[0])
                #
            #
        #
        
        zipbite.seek(0)

        res = base64.b64encode(zipbite.read())

        return(res.decode())        
    #
#