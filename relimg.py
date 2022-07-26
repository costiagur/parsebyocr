from PIL import Image
import common

#this function saves initial relative image to be searched using CV2.

def relimg (imgobj,relx1,rely1,relx2,rely2,canvwidth,canvheight, relimgfile): #keynum, relimgfile):

    try:
        iniwidth = imgobj.size[0]
        iniheight = imgobj.size[1]

        relx1 = float(relx1)
        rely1 = float(rely1)
        relx2 = float(relx2)
        rely2 = float(rely2)

        relimgres = imgobj.crop((relx1*iniwidth/canvwidth, rely1*iniheight/canvheight, relx2*iniwidth/canvwidth, rely2*iniheight/canvheight))
        
        #relimgres.show()
        relimgres.save(relimgfile.name,"JPEG")
        relimgfile.close()
        

        return relimgfile
    #

    except Exception as e:
        common.errormsg("Relimg",e)
        return b'Error ' + str(e).encode('UTF-8')
    #    
#