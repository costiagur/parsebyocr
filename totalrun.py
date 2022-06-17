import zipfile
from pdf2image import convert_from_bytes
from PyPDF2 import (PdfFileReader, PdfFileWriter)
from io import BytesIO
from ocrit import ocrit
from tempfile import (TemporaryDirectory,NamedTemporaryFile)
from base64 import b64encode
from relimg import relimg
import re
import json
from os import unlink
 

def totalrun(scanfile, areastr, relstr, canvheight, canvwidth, namearr,cutpagearr, rollangle='0', brightnessrate='1.0', contrastrate='1.0',enlargerate='2',
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
    #print(areadict)

    zipbite = BytesIO()

    zipres = zipfile.ZipFile(zipbite, mode='a')

    #---------------Convert all pdf pages to images and test page to image to be the basis for relative image cuts ---------------------------------------------------------

    imgesdir = TemporaryDirectory(ignore_cleanup_errors=True)
    testimgdir = TemporaryDirectory(ignore_cleanup_errors=True)

    resimages = convert_from_bytes(scanfile,dpi=300, output_folder=imgesdir.name,grayscale=True)
 
    # -------------create list relative images files to be searched later during OCR process ----------------------------------
   
    relimgfilelist = dict()

    for key in reldict: #key is ordered number
        testimage = convert_from_bytes(scanfile, dpi=300, output_folder= testimgdir.name,first_page=int(reldict[key][4]),last_page=int(reldict[key][4]),grayscale=True) #imges from which relatives will be cut off
        reimgfile = NamedTemporaryFile(mode='w+b',delete=False)
        relimgfilelist[key] = relimg(testimage[0],reldict[key][0],reldict[key][1],reldict[key][2],reldict[key][3],canvwidth,canvheight,reimgfile)
        reimgfile.close()
    #

    scanfileio = BytesIO()
    scanfileio.write(scanfile)
    scanfileio.seek(0)

    pdfReader = PdfFileReader(scanfileio)
    print("num of pdf pages :" + str(pdfReader.numPages))
    
    pdfWriter = PdfFileWriter()
    csvlist = []

    print("len(resimages): " + str(len(resimages)))

    prevstr = 'firstpage' #in case first page will not meet conditions
    resstr = 'firstpage'

    for i in range(0,len(resimages),1): #for each page to be taken

        resdatalist = []
        resloclist = []

        for key in areadict: #for each selected area in the img

            resdata, imgfound, rellocfound = ocrit(resimages[i],
                                    areadict[key][0],
                                    areadict[key][1],
                                    areadict[key][2],
                                    areadict[key][3],
                                    reldict[key][0],
                                    reldict[key][1],
                                    relimgfilelist[key],
                                    rollangle,
                                    brightnessrate,
                                    sharpnessrate,
                                    contrastrate,
                                    boxblur,
                                    enlargerate,
                                    hsa, vsa,
                                    langset)

            print("for key: " + str(key) + " " + resdata)

            resdatalist.append(resdata) #each next cell in data row
            resloclist.append(rellocfound)
        #

        print("cutpagearr: " + str(cutpagearr))
        print("resloclist: " + str(resloclist))

        csvlist.append("\t".join(resdatalist))

        if sum(cutpagearr) <= sum([a*b for a,b in zip(cutpagearr,resloclist)]): #in case the conditions are met

            def combinestr(cond,mystr):
                return mystr if cond == 1 else ''
            #

            resstr = map(combinestr,namearr,resdatalist)
            resstr = ' '.join(resstr)
            resstr = resstr.strip()

            print("File name " + str(i) + " " + re.sub('\W+', '_', resstr) + ".pdf")
            print("Found data: " + str(resdatalist))
            print("len(resimages): " + str(len(resimages)))
            print("i: " + str(i))           


            if len(resimages) > 1 and i==0:
                pdfWriter.addPage(pdfReader.getPage(0))
                

            elif len(resimages) == 1 and i==0:
                pdfWriter.addPage(pdfReader.getPage(0))
                
                tempf = NamedTemporaryFile(mode='w+b',suffix=".pdf",delete=False)
                pdfWriter.write(tempf)
                tempf.close()
                
                zipres.write(tempf.name, arcname=re.sub('\W+', '_', resstr) + ".pdf")
                unlink(tempf.name)

            elif len(resimages) > 1 and i== len(resimages)-1:
                tempf = NamedTemporaryFile(mode='w+b',suffix=".pdf",delete=False)
                pdfWriter.write(tempf)
                tempf.close()
 
                zipres.write(tempf.name, arcname=re.sub('\W+', '_', prevstr) + ".pdf")
                unlink(tempf.name)
                
                pdfWriter = PdfFileWriter() #new pdfwriter to fill
                pdfWriter.addPage(pdfReader.getPage(i))

                tempf = NamedTemporaryFile(mode='w+b',suffix=".pdf",delete=False)
                pdfWriter.write(tempf)
                tempf.close()

                zipres.write(tempf.name, arcname=re.sub('\W+', '_', resstr) + ".pdf")
                unlink(tempf.name)
            
            elif len(resimages) > 1 and i < len(resimages)-1:
                tempf = NamedTemporaryFile(mode='w+b',suffix=".pdf",delete=False)
                pdfWriter.write(tempf)
                tempf.close()

                zipres.write(tempf.name, arcname=re.sub('\W+', '_', prevstr) + ".pdf")
                unlink(tempf.name)

                pdfWriter = PdfFileWriter() #new pdfwriter to fill
                pdfWriter.addPage(pdfReader.getPage(i))
            #

        elif i==len(resimages)-1:#last page and conditions are not met on this page
            pdfWriter.addPage(pdfReader.getPage(i))
                
            tempf = NamedTemporaryFile(mode='w+b',suffix=".pdf",delete=False)
            pdfWriter.write(tempf)
            tempf.close()
                
            zipres.write(tempf.name, arcname=re.sub('\W+', '_', prevstr) + ".pdf")
            unlink(tempf.name)

        else: #conditions are not met
            pdfWriter.addPage(pdfReader.getPage(i)) #adding to existing pdfwriter
        #
        
        prevstr = resstr
    #
    
    print(csvlist)

    csvstr = "\n".join(csvlist)

    csvstr = re.sub(r'[^0-9A-Za-zא-ת_,\newline\.\-\t\s]',"",csvstr)

    csvfile = NamedTemporaryFile(mode = "w",suffix=".xls",delete=False)

    csvfile.write(csvstr)

    csvfile.close()

    zipres.write(csvfile.name, arcname="result.xls")
    unlink(csvfile.name)

    zipres.close()
        
    zipbite.seek(0)

    res = b64encode(zipbite.read())

    zipbite.close()

    for eachkey in relimgfilelist:
        unlink(relimgfilelist[eachkey].name)
    #

    scanfileio.close()

    imgesdir.cleanup()
    testimgdir.cleanup()

    return res     
    
#