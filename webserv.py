import http.server
import post
from sys import exit


class Handler(http.server.BaseHTTPRequestHandler):
    def setcodeword(self, codestr):
        self.CODESTR = codestr
        self.REPLIYED = 0
        
    #

    def setnewport(self,newPORT,querystr):
        self.newPORT = newPORT
        self.querystr = querystr
    #

    def customfunc(self,funcobj):
        self.funcobj = funcobj
    #

    def processing(self,queryobj):
        
        postlist = queryobj._POST()

        if('request' in postlist.keys()):
            if postlist['request'] == 'close':
                exit()
            #
            elif postlist['request'] == self.CODESTR:
                Handler.REPLIYED = 1 #this class is never initiated. therefore using here self doesn't update the value of self.REPLIYED in the setcodeword() and isrepliyed(). instead using specifically the name of the class

                returnstr = '{"port":' + str(self.newPORT) + ', "args":' + self.querystr + '}'

                return returnstr.encode()
        #

        return Handler.funcobj(queryobj)
    #

    def set_headers(self):
        self.send_response(200) 
        self.send_header('Content-Type', 'text/html')
        
        self.send_header('Access-Control-Allow-Origin', 
                        self.headers['Origin']
                        ) #local file sends origin header 'null'. 
        
        self.send_header('Vary','Origin')
        self.end_headers()
    #

    def do_POST(self):

        if self.client_address[0] != '127.0.0.1': #check that request comes from local computer
            return
        #

        queryobj = post.POST(self)

        replymsg = self.processing(queryobj) #,self.custmethod)

        self.set_headers() #set headers of response
        
        self.wfile.write(replymsg) #send bytes = write to socket

        return
    #

    def isrepliyed(self): #replyes that we the codeword was recieved and answered (repliyed) and we can change the port to new one.
        return self.REPLIYED 

    #
#

class HttpServer(http.server.HTTPServer):
    def __init__(self,address_tuple,useHandler,codestr,newPORT,funcobj,querystr):
        
        self.address_tuple = address_tuple
        self.useHandler = useHandler

        super().__init__(self.address_tuple,self.useHandler)
        
        useHandler.setcodeword(useHandler,codestr)
        useHandler.setnewport(useHandler,newPORT,querystr)
        useHandler.customfunc(useHandler,funcobj)
    #

    def run_once(self):      
        self.handle_request()
        return self.useHandler.isrepliyed(self.useHandler) #Handler class is never initiated. no __init__(). therefore, need to provide class to self. 
    #
    
    def close(self):
        self.server_close()
    #

    def run_continuously(self):
        self.serve_forever()
    #
#