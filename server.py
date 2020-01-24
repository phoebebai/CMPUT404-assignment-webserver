#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        alist = self.data.split()
        
        if len(alist) < 2:
            return
        if alist[0].decode("utf-8") != "GET":
            cont = "<h1 align=\"center\">Error 405</h1>"
            cont = cont.encode("utf-8")
            length = len(cont)
            cont = cont.decode("utf-8")

            finalcont = "HTTP/1.x 405 Method Not Allowed\r\nContent-length:"+str(length)+"\r\nContent-Type: text/html\r\n\r\n<h1 align=\"center\">Error 405</h1>"
            self.request.sendall(bytearray(finalcont,'utf-8'))
            return

        filesrc = "www" + alist[1].decode("utf-8")
        if filesrc[-1] == "/":
            filesrc = filesrc + "index.html"
        else:
            if os.path.exists(filesrc) and not os.path.isfile(filesrc):
                finalcont = "HTTP/1.x 301 Moved Permanently\r\nContent-length: 0\r\nLocation: http://127.0.0.1:8080/deep/\r\nConnection: close\r\n\r\n"
                self.request.sendall(bytearray(finalcont,'utf-8'))
                return

        try :
            f = open(filesrc,"r")
            cont = f.read()
            cont = cont.encode("utf-8")
            length = len(cont)
            cont = cont.decode("utf-8")

            if ".css" in filesrc:
                finalcont = "HTTP/1.x 200 ok\r\nContent-length:"+str(length)+"\r\nContent-Type: text/css\r\n\r\n" + cont
            elif".html" in filesrc:
                finalcont = "HTTP/1.x 200 ok\r\nContent-length:"+str(length)+"\r\nContent-Type: text/html\r\n\r\n" + cont

            self.request.sendall(bytearray(finalcont,'utf-8'))
        
        except :

            cont = "<h1 align=\"center\">Error 404</h1>"
            cont = cont.encode("utf-8")
            length = len(cont)
            cont = cont.decode("utf-8")
            
            finalcont = "HTTP/1.x 404 Not Found\r\nContent-length:"+str(length)+"\r\nContent-Type: text/html\r\n\r\n<h1 align=\"center\">Error 404</h1>"
            self.request.sendall(bytearray(finalcont,'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; sthis will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
