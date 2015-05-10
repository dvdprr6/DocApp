import tornado.ioloop
import tornado.web

class BaseRequestHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

application = tornado.web.Application([
	(r"/", BaseRequestHandler )
])

def main():
	'''INIT SERVER'''
	main_loop = tornado.ioloop.IOLoop.instance()
	application.listen(8888)
	main_loop.start()

if __name__ == "__main__":
	main()