import webserv
import webbrowser
from socketserver import ThreadingMixIn
import threading
import os
import backholder
import http.server
import myfunc
import random 

HOST = '127.0.0.1'
PORT = random.randint(50000,60000)

currentfolder =  os.path.dirname(os.path.realpath(__file__))

with open(currentfolder + "/uiclient.js", "r") as jsfile:
    existingjs = jsfile.readlines() #read all lines from uiclient,js file
#
with open(currentfolder + "/uiclient.js", "w") as jsfile: #insert ui.host in JS file with random PORT num
    for jsline in existingjs:
        if jsline.find("ui.host = 'http://localhost") != -1: #file existing ui.host line and replace it
            jsfile.write("ui.host = 'http://localhost:%i'\n" %(PORT))
        #
        else:
            jsfile.write(jsline) #all other lines write what was there
        #
    #
#

htmlfilepath = "file://" + currentfolder + "/index.html"

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass
#

webbrowser.open(htmlfilepath,1,True) #open html file of the UI

webserv.webserv.custmethod = myfunc.myfunc #provide my custom function to POST of webserver

serv = ThreadedHTTPServer((HOST,PORT),webserv.webserv) #threading HTTPserver

server_thread = threading.Thread(target=serv.serve_forever) #preparing thread because tkinter can't run in the same thread with httpserver
server_thread.start()

backholder.holderrun("Parse by OCR") #Run Tkinter to hold the server in the background

serv.shutdown()