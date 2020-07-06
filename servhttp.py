import http.server
import onepage
import pars2files

class webserv(http.server.BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200) 
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', self.headers['Origin']) #local file sends origin header 'null'. 
        self.send_header('Vary','Origin')
        self.end_headers()
    #


    def _post_parse(self,boundary,postb):

        resdict = dict()
        delimiter1 = (boundary + '\r\nContent-Disposition: form-data; name=').encode()
        delimiter1len = len(delimiter1)        
        
        delimiter2 = b'\r\n\r\n'
        delimiter2len = len(delimiter2)

        filename_start_delm = ('; filename=').encode()
        filename_start_delmlen = len(filename_start_delm)

        filename_end_delm = ('Content-Type:').encode()

        boundary = boundary.encode()

        totalcount = postb.count(boundary)

        boundlist = [1,]

        startpoint = 1

        for i in range(1,totalcount,1):
            where = postb.find(boundary,startpoint)
            boundlist.append(where)
            startpoint = where + len(boundary)
            i=i
        # 

        #print(boundlist)

        for start_headers in boundlist[0:-1]:

            end_headers = postb.find(delimiter2,start_headers) #find the end of input header data
            
            filename_start = postb.find(filename_start_delm,start_headers,end_headers) #end of name

            filename_end = postb.find(filename_end_delm,start_headers,end_headers) #end of filename

            #print("start_headers: %s end_headers %s filename_start %s filename_end %s" % (start_headers,end_headers,filename_start,filename_end))

            if start_headers == boundlist[len(boundlist)-2]:# in case of last input
                endval = boundlist[len(boundlist)-1]
            else:
                endval = boundlist[boundlist.index(start_headers)+1]
            #

            if filename_start != -1: # in case a file was not loaded to that inputbox, there is no filename
                
                filename = postb[(filename_start+filename_start_delmlen):(filename_end-3)] #without last "\r\n
                filename = filename.decode().strip('\"')

                name = postb[(start_headers+delimiter1len):filename_start]
                name = name.decode().strip('\"')  
            
            else:
                filename = ''

                name = postb[(start_headers+delimiter1len):end_headers]
                name = name.decode().strip('\"')
            #           
                  
            value = postb[(end_headers+delimiter2len):(endval-2)] #without \r at the end
                
            if filename == '':
                value = value.decode()
            else:
                pass
            #

            #print("start_headers %s name %s filename %s value %s" % (start_headers,name,filename,value))

            resdict[name] = (filename,value)
        #

        return resdict
    #

    def do_POST(self): #Important: POST string inputs first, files last
        
        length = int(self.headers['Content-Length'])

        boundary = self.headers['Content-Type'].split('=')[1] #get boundary

        boundary = '--'+boundary #in headers, boundary is shorter by 2 "-" than in request body

        postb = self.rfile.read(length) #read entire request body. result is bytes.

        querystr = self._post_parse(boundary,postb)


        #----------------- Insert Your Code Here in case of POST request --------------------------------------   

        if querystr['request'][1] == 'preload':
            if querystr['docfile'][1] == b'': #if no file was added, stop processing
                msg = 'No file uploaded'
                msgb = msg.encode() #convert to bytes to be sent
            else:
                msg = onepage.onepage(querystr['docfile'][1],querystr['rollangle'][1],querystr['hsa'][1],querystr['vsa'][1],querystr['dpirate'][1])
                msgb = msg.encode() #convert to bytes to be sent
            #
        elif querystr['request'][1] == 'prepare':
            if querystr['docfile'][1] == b'': #if no file was added, don't delete it
                msg = 'No file uploaded'
                msgb = msg.encode() #convert to bytes to be sent
            else:
                msgb = pars2files.pars2files(querystr['reqtype'][1],querystr['docfile'][1],querystr['ratiox1'][1],querystr['ratioy1'][1],querystr['ratiox2'][1],querystr['ratioy2'][1],querystr['rollangle'][1],querystr['hsa'][1],querystr['vsa'][1],querystr['colore'][1],querystr['brightnesse'][1],querystr['sharpnesse'][1],querystr['contraste'][1],querystr['boxblur'][1],querystr['dpirate'][1])
            #
        #

        #-------------------------------------------------------------------------------------------------------
               
        self._set_headers() #set headers of response
        
        self.wfile.write(msgb) #send bytes = write to socket

        return
    #
#


HOST = '127.0.0.1'
PORT = 50000

serv = http.server.HTTPServer((HOST,PORT),webserv)

serv.serve_forever()