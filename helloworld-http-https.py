#!/usr/bin/env python3

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import platform
import time
import _thread as thread
import ssl

def webserver(node, http, ip, httpport, httpsport, sslcert, sslkey):

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("[HTTP] Hello World! I am %s serving on ip %s port %s\n" % (node, ip, httpport), "utf-8"))

    class SimpleHTTPSRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("[HTTPS] Hello World! I am %s serving on ip %s port %s\n" % (node, ip, httpsport), "utf-8"))
    
    if http:
        httpd = HTTPServer((ip, httpport), SimpleHTTPRequestHandler)
    else: # https
        httpd = HTTPServer((ip, httpsport), SimpleHTTPSRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=sslkey, certfile=sslcert, server_side=True)

    httpd.serve_forever()
    httpd.server_close()

def spawn(node, ip, httpport, httpsport, sslcert, sslkey):
    VERBOSE = "True"
    thread.start_new_thread(webserver, (node, True, ip, int(httpport), int(httpsport), sslcert, sslkey))
    thread.start_new_thread(webserver, (node, False, ip, int(httpport), int(httpsport), sslcert, sslkey))

    while 1:
        time.sleep(10)

def is_accessible(path, mode='r'):
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True


def main():
    node = platform.node()
    try:
        ip = os.environ['LISTEN_IP']
    except:
        ip = "0.0.0.0"
    try:
        httpport = os.environ['HTTP_PORT']
    except:
        httpport = 8080
    try:
        httpsport = os.environ['HTTPS_PORT']
    except:
        httpsport = 8443
    try:
        sslcert = os.environ['SSL_CERT_PATH']
    except:
        sslcert = '/etc/ssl/server.cert'
    try:
        sslkey = os.environ['SSL_KEY_PATH']
    except:
        sslkey = '/etc/ssl/server.key'
    if not (is_accessible(sslcert) and is_accessible(sslcert)):
        sys.stderr.write("Error with certificate files. Exiting.\n")
        return 1
    try:
        spawn(node, ip, int(httpport), int(httpsport), sslcert, sslkey)
    except KeyboardInterrupt:
        sys.stderr.write("Keybord Interrupt\n")
        return 1

if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
