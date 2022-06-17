import base64
import json
from PyPDF2 import PdfFileMerger
from io import BytesIO
from firstpage import firstpage
from testrun import testrun
from totalrun import totalrun
from tempfile import NamedTemporaryFile
from os import unlink

def myfunc(queryobj):

    postdict = queryobj._POST()
    filesdict = queryobj._FILES()
    replymsg = b'Running'
    print("POST = " + str(postdict) + "\n")
    #print("FILES = " + str(filesdict) + "\n")

    def mergepdfs(filedictionary): 
        merger = PdfFileMerger()
        midpdflist = []
        for filename in filedictionary:
            midpdf = NamedTemporaryFile(mode="w+b",delete=False)
            midpdf.write(filedictionary[filename][1])
            midpdf.close()
            midpdflist.append(midpdf.name)
        #
        for eachio in midpdflist:
            merger.append(eachio)
        #
        mergedfile = BytesIO()
        merger.write(mergedfile)
        merger.close()    
        mergedfile.seek(0)

        for eachio in midpdflist:
            unlink(eachio)
        #
        return mergedfile


    #----------------- Preload - show image of a page in pdf file -------------------------------------------------

    if postdict['request'] == 'preload':
        if len(filesdict) == 1:
            replymsg = firstpage(filesdict['pdffiles_0'][1],postdict['rollangle'],postdict['hsa'],postdict['vsa'],postdict['testpagenum_in'])
        else:
            mergedfile = mergepdfs(filesdict)
            replymsg = firstpage(mergedfile.read(),postdict['rollangle'],postdict['hsa'],postdict['vsa'],postdict['testpagenum_in'])
            mergedfile.close()
        #
    #
        

    # ------------ Test Run - first run to test results -------------------------------------------------------------
    elif postdict['request'] == 'testrun':
        if len(filesdict) == 1:
            replymsg = testrun(filesdict['pdffiles_0'][1],postdict['areastr'],postdict['relstr'],postdict['canvheight'],postdict['canvwidth'],postdict['rollangle'],postdict['brightnessrate'], postdict['contrastrate'],postdict['enlragerate'], postdict['hsa'],postdict['vsa'],postdict['lang']) 
        else:
            mergedfile = mergepdfs(filesdict)
            replymsg = testrun(mergedfile.read(),postdict['areastr'],postdict['relstr'],postdict['canvheight'],postdict['canvwidth'],postdict['rollangle'],postdict['brightnessrate'], postdict['contrastrate'],postdict['enlragerate'], postdict['hsa'],postdict['vsa'],postdict['lang'])
            mergedfile.close()
        #
    #
    
    # ------------ Total Run - first run to test results -------------------------------------------------------------
    elif postdict['request'] == 'totalrun':

        namearr = json.loads(postdict['namearr'])
        cutpagearr = json.loads(postdict['cutpagearr'])

        if len(filesdict) == 1:
            replymsg = totalrun(filesdict['pdffiles_0'][1],postdict['areastr'],postdict['relstr'],postdict['canvheight'],postdict['canvwidth'],namearr,cutpagearr,postdict['rollangle'],postdict['brightnessrate'], postdict['contrastrate'],postdict['enlragerate'], postdict['hsa'],postdict['vsa'],postdict['lang'])
        else:
            mergedfile = mergepdfs(filesdict)
            replymsg = totalrun(mergedfile.read(),postdict['areastr'],postdict['relstr'],postdict['canvheight'],postdict['canvwidth'],namearr,cutpagearr,postdict['rollangle'],postdict['brightnessrate'], postdict['contrastrate'],postdict['enlragerate'], postdict['hsa'],postdict['vsa'],postdict['lang'])
            mergedfile.close()
        #
    #

    # reply message should be encoded to be sent back to browser ----------------------------------------------
    # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
    # json is encoded to be sent to browser.

    #file64enc = base64.b64encode(filesdict['doc1'][1])
    #file64dec = file64enc.decode()

    #replymsg = json.dumps([filesdict['doc1'][0],file64dec]).encode('UTF-8')

    return replymsg
#