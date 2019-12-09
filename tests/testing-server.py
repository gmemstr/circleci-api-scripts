import http.server
import socketserver

PORT = 7483

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"success": true}'.encode('utf-8'))
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"success": true}'.encode('utf-8'))
        return

print('Server listening on port 7483...')
httpd = socketserver.TCPServer(('', PORT), Handler)
httpd.serve_forever()
