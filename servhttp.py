import http.server
import urllib
import os
import time
import onepage
import pars2files

#logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'\\log\\servhttp.log',format='%(levelname)s in %(funcName)s, %(asctime)s: %(message)s',level=logging.DEBUG)

class webserv(http.server.BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200) 
        self.send_header('Content-Type', 'text/html') 
        self.send_header('Access-Control-Allow-Origin', self.headers['Origin']) #local file sends in origin 'null' req header. therefore the compatible response header  
        self.end_headers()
    #

    def _post_prepare(self,boundary,poststr):

        resdict = dict()
        delimiter1 = boundary + '\r\nContent-Disposition: form-data; name='
        delimiter1len = len(delimiter1)
        delimiter2 = '\r\n\r\n'
        delimiter2len = len(delimiter2)

        postprefile = poststr.split('filename=')[0] #get everything till filename= string

        for i in range(0,len(postprefile),1):
            startname = postprefile.find(delimiter1,i)
            endname = postprefile.find(delimiter2,startname)
            endval = postprefile.find(delimiter1,endname)
            
            if endname > startname and startname != -1:
                resdict[postprefile[(startname+delimiter1len):(endname)].strip('\"')] = postprefile[(endname+delimiter2len):(endval-1)].strip('\r') 
                # value taken should not include \r
            #
            else:
                break
            #
        #
        
        if poststr.find('filename=',0) > -1:
            startfilename = poststr.find('filename=',0)
            endfilename = poststr.find('\r\n',startfilename+9)
            resdict['filename'] = poststr[startfilename+9:endfilename].strip('\"')
        #      

        #print(resdict)

        return resdict
    #

    def do_POST(self):

        #print ("headers: " +str(self.headers))
        
        length = int(self.headers['Content-Length'])

        boundary = self.headers['Content-Type'].split('=')[1] #get boundary

        boundary = '--'+boundary #in headers, boundary is shorter by 2 "-" than in request body

        print(length)

        postb = self.rfile.read(length) #read entire request body. result is bytes

        #print(postb)

        findbyte = postb.find(b'Content-Type',0) #find where file should start after \r\n in the request body

        findfile = postb.find(b'\r\n\r\n',findbyte) #find last \r\n\r\n that go after content-type but before the file body

        print(findfile)

        if findfile == -1:
            posstnofileb = postb #if no file was sent than the entire body should be converted to string
        else:
            posstnofileb = postb[0:(findfile)] #if file was sent than everything before the file should be converted to string. file should be left bytes.
        #
        #postnofiles = posstnofileb.decode('windows-1255')
        
        postnofiles = posstnofileb.decode() #decode from bytes to string the part of body before file

        #print(postnofiles)

        querystr = self._post_prepare(boundary,postnofiles) #remove all headers in the body. convert to dct

        if findfile == -1:
            querystr['docfile'] = b'' #if no file was sent, the docfile argument will be empty bytes str
        else:
            eof = postb[findfile:length].find(boundary.encode()) #last boundary is the end of file
            querystr['docfile'] = postb[(findfile+4):(findfile+eof-2)] #after two \r\n and till last \r\n
        #
        #print("Query: "+str(querystr))    

        if querystr['request'] == 'preload':
            if querystr['docfile'] == b'': #if no file was added, stop processing
                msg = 'No file uploaded'
                #logging.error(msg)
            
            else:
                msg = onepage.onepage(querystr['docfile'],querystr['hsa'],querystr['vsa'],querystr['dpirate'])
            #
        elif querystr['request'] == 'prepare':
            if querystr['docfile'] == b'': #if no file was added, don't delete it
                msg = 'No file uploaded'
            
            else:
                msg = pars2files.pars2files(querystr['reqtype'],querystr['docfile'],querystr['ratiox1'],querystr['ratioy1'],querystr['ratiox2'],querystr['ratioy2'],querystr['hsa'],querystr['vsa'],querystr['colore'],querystr['brightnesse'],querystr['sharpnesse'],querystr['contraste'],querystr['boxblur'],querystr['dpirate'])
            #
        #
               
        self._set_headers() #set headers of response
        
        msgb = msg.encode() #convert to bytes to be sent

        self.wfile.write(msgb) #send bytes = write to socket

        return
    #
    
    def do_GET(self):
        pass
    #
#

HOST = '127.0.0.1'
PORT = 50000

serv = http.server.HTTPServer((HOST,PORT),webserv)

serv.serve_forever()

