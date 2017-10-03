import BaseHTTPServer
import json
import time

class WebMUDRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # Eventually be picky about the endpoint, but right now accept any request.
        # (This is because eventually the mud can serve the client HTML/CSS/JS too!)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = []
        response.append(self._console_out("Ok @ {}".format(time.time())))
        response.append(self._console_in_flash(200, [["#F00", "#0F0", "#00F"][int(time.time())%3], "#FFF"]))
        self.wfile.write(json.dumps(response))

    def _console_out(self, msg):
        result = {}
        result['time'] = time.time()
        result['type'] = 'console-out'
        result['data'] = {'msg': msg}
        return result

    def _console_in_flash(self, speed, seq):
        result = {}
        result['time'] = time.time()
        result['type'] = 'console-in-flash'
        result['data'] = {"speed": speed, "seq": seq}
        return result


def start_mud():
    server_address = ('', 7777)
    httpd = BaseHTTPServer.HTTPServer(server_address, WebMUDRequestHandler)
    # Use httpd.handle_request() to handle one request 
    # This allows checks in-between, like for shutdown.
    while True: # "True" makes this equivalent to httpd.serve_forever()
        httpd.handle_request()

if __name__ == '__main__':
    start_mud()

