from PIL import Image
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import pickle
import time



class ReqHandler(BaseHTTPRequestHandler):
	def log_request(self,*args):
		pass
	def do_POST(self,*args):
		a=pickle.loads(self.rfile.read(int(self.headers["Content-Length"])))
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",0)
		self.end_headers()
		i=Image.frombuffer(*a,"raw",a[0],0,1)
		i.save(f"./data/{time.time()}.png")



with ThreadingHTTPServer(("localhost",8010),ReqHandler) as httpd:
	print("Start!")
	httpd.serve_forever()