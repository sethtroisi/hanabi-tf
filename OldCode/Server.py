import Game

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import urllib.parse
import subprocess

class Website:
    def getSimpleForm(self):
        return '''
<form action="submit" method="post">
  Game key:<br>
  <input type="text" name="gamekey" value="Game12"><br>
  Player key:<br>
  <input type="text" name="playerkey" value="Player1"><br><br>
  <input type="submit" value="Submit">
<form>
'''


class HanabiServer(BaseHTTPRequestHandler):
    def _set_headers(self, contentType=None):
        self.send_response(200)
        if contentType:
            self.send_header('Content-type', contentType)
        self.end_headers()

    def getRequestPath(self):
        parsedPath = urllib.parse.urlparse(self.path)
        return parsedPath.path

    def getData(self):
        length = int(self.headers.get('content-length', 0))
        if length > 0:
            return self.rfile.read(length)
        return b''

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        path = self.getRequestPath()
        print ("cmd: {} path: {}".format(self.command, path))

        if path == "/getForm":
            contentType = "text/html"
            response = Website().getSimpleForm()
        elif path == "/getGame":
            contnetType = "application/json"
            data = {turn:5, score:10}
            response = json.dumps(data)
        else:
            contentType = "application/json"
            data = ["Hello", {"complex":"data"}, 1, 2, "World"]
            response = json.dumps(data)
        
        self._set_headers(contentType)
        self.wfile.write(response.encode("utf-8"))

    def do_POST(self):
        self._set_headers()
        path = self.getRequestPath()
        data = self.getData()
        print ("cmd: {} path: {} data: {}".format(
            self.command, path, data))
        response = 'Hello World'
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=HanabiServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
