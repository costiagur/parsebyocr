import http.server
from os import linesep

class POST:
    def  __init__(self,server_instance):
        
        selfserv = server_instance

        content_length = int(selfserv.headers['Content-Length'])

        boundary = '--' + selfserv.headers['Content-Type'].split('=')[1] #get boundary. in headers, boundary is shorter by 2 "-" than in request body

        boundary = boundary.encode()

        #https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        postb = selfserv.rfile.read(content_length) #read entire request body. result is bytes.
        
        self.resdict = dict()

        postblist = postb.split(boundary)
       
        delimiter = (linesep + linesep).encode()

        for eachpart in postblist[1:-1]:

            contDisp = eachpart[0 : eachpart.find(delimiter)]

            contData = eachpart[eachpart.find(delimiter) + len(delimiter) : -len(linesep)]

            if contDisp.find(b'; filename=') != -1: # in case a file was loaded
                
                if contDisp.find(linesep.encode() + b'Content-Type:') != -1:
                    filename = contDisp[contDisp.find(b'; filename=') + 12 : -len(linesep) + 1 + abs(contDisp.find(linesep.encode() + b'Content-Type:'))]
                else:
                    filename = contDisp[contDisp.find(b'; filename=') + 12 : -1]
                #

                filename = filename.decode()

                paramname = contDisp[contDisp.find(b'; name=') + 8 : contDisp.find(b'; filename=') -1]
                paramname = paramname.decode()

            else:
                filename = ''
                paramname = contDisp[contDisp.find(b'; name=') + 8 : -1]
                paramname = paramname.decode()

                contData = contData.decode()
            #           

            self.resdict[paramname] = (filename,contData)
        #
    #
    
    def _FILES(self):
        resdict = dict()

        for eachkey in self.resdict.keys():
            if self.resdict[eachkey][0] !='':
                resdict[eachkey] = self.resdict[eachkey]
            #
        #

        return resdict
    #

    def _POST(self):
        resdict = dict()

        for eachkey in self.resdict.keys():
            if self.resdict[eachkey][0] == '':
                resdict[eachkey] = self.resdict[eachkey][1]
            #
        #

        return resdict
    #
#  