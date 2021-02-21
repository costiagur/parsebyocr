import json
import pars2files
import firstpage

def myfunc(obj,querydict):

    #print(obj)

    if querydict['request'][1] == 'preload':
            
        if querydict['docfile0'][1] == b'': #if no file was added, stop processing
            msg = 'No file uploaded'
            
        else:
            try:
                msg = firstpage.showfirstpage(querydict['docfile0'][1],
                                    int(querydict['rollangle'][1]),
                                    int(querydict['hsa'][1]),
                                    int(querydict['vsa'][1]),
                                    400)
        
            except Exception as err:
                msg = "Error occured: " + str(err)
            #
        #
    
    elif querydict['request'][1] == 'prepare':
            
        if querydict['docfile0'][1] == b'': #if no file was added, don't delete it
            msg = 'No file uploaded'
            
        else:
            try:
                arealist = json.loads(querydict['areastr'][1])
                areadict = dict()
                doclist = []
                
                for i in range(0,len(arealist)):
                    areadict[i] = list(map(int,arealist[i].split(",")))
                #

                print(areadict)

                for i in range(0,int(querydict['docsnum'][1])):
                    doclist.append(querydict['docfile' + str(i)][1])
                #

                msg = pars2files.pars2files(querydict['reqtype'][1],
                                        doclist,
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
            
            except Exception as err:
                msg = "Error occured: " + str(err)
            #
    #
    
    return msg
#