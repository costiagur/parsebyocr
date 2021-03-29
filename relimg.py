from PIL import Image

#this function saves initial relative image to be searched using CV2.

def relimg (imgobj,relx1,rely1,relx2,rely2,canvwidth,canvheight, keynum, tempdir):

    iniwidth = imgobj.size[0]
    iniheight = imgobj.size[1]

    relimg = imgobj.crop((relx1*iniwidth/canvwidth, rely1*iniheight/canvheight, relx2*iniwidth/canvwidth, rely2*iniheight/canvheight))
    file = open(tempdir + "\\relimg" + str(keynum) + ".bmp", "w+b")
    relimg.save(file)
    file.close()

    return (tempdir + "\\relimg" + str(keynum) + ".bmp")
#