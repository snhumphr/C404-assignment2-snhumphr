#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        status_line = data.split("\r\n")[0]
        code = status_line.split(" ")[1]
        return int(code)

    def get_headers(self, data):
        return None

    def get_body(self, data):
        body = data.split("\r\n")[-1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def build_request(self, url, host, method):
        
        crlf = "\r\n"
        http_version = "HTTP/1.1"
        space = " "
        
        request_line = method + space + url + space + http_version + crlf
        
        host_line = "Host: " + host + space + crlf
        #TODO: Check if we need a message body on the request
        
        return request_line + host_line + crlf

    def GET(self, url, args=None):
        
        #use urllib to parse the url
        parsed_url = urllib.parse.urlparse(url, "http")
        
        hostname = parsed_url.hostname
        port = parsed_url.port
        
        #build request
        #print("hostname: ", hostname)
        #print("port: ", port)
        
        request = self.build_request(url, hostname, "GET")        
        print("Request: ", request)

        self.connect(hostname, port)

        self.sendall(request)

        self.socket.shutdown(socket.SHUT_WR)

        response = self.recvall(self.socket)

        self.close()

        code = self.get_code(response)
        
        headers = self.get_headers(response)
        
        body = self.get_body(response)

        print("Code: ", code)
        print("Body: ", body)
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
