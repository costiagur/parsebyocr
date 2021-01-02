import json
import pars2files
import firstpage

def myfunc(obj,querydict):

    #print(obj)

    if querydict['request'][1] == 'preload':
            
        if querydict['docfile'][1] == b'': #if no file was added, stop processing
            msg = 'No file uploaded'
            
        else:
            msg = firstpage.showfirstpage(querydict['docfile'][1],
                                    int(querydict['rollangle'][1]),
                                    int(querydict['hsa'][1]),
                                    int(querydict['vsa'][1]),
                                    400)
        #
    
    elif querydict['request'][1] == 'prepare':
            
        if querydict['docfile'][1] == b'': #if no file was added, don't delete it
            msg = 'No file uploaded'
            
        else:
            arealist = json.loads(querydict['areastr'][1])
            areadict = dict()
            
            for i in range(0,len(arealist)):
                areadict[i] = list(map(int,arealist[i].split(",")))
            #

            print(areadict)

            msg = pars2files.pars2files(querydict['reqtype'][1],
                                    querydict['docfile'][1],
                                    areadict,
                                    querydict['canvheight'][1],
                                    querydict['canvwidth'][1],
                                    querydict['rollangle'][1],
                                    querydict['brightnessrate'][1],
                                    1.0,
                                    querydict['contrastrate'][1],
                                    querydict['boxblur'][1],
                                    2,
                                    querydict['hsa'][1],
                                    querydict['vsa'][1],
                                    400,
                                    querydict['pagesin'][1],
                                    '',
                                    querydict['lang'][1])
        #
    #
    return msg

#