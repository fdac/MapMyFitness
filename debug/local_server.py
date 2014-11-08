from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import sys

class AuthorizationHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200, 'OK')
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.server.path = self.path
    
redirect_uri = 'http://localhost.mapmyapi.com:12345/callback'
parsed_redirect_uri = urlparse.urlparse(redirect_uri)

server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

httpd = HTTPServer(server_address, AuthorizationHandler)
while True:
  httpd.handle_request()
  print 'Request Received'
  sys.stdout.flush()