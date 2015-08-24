# coding=utf-8
import logging
import os.path
import uuid
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.web
import tornado.websocket
from setting import TORNADO_SETTINGS

define("port", default=8999, help="run on the given port", type=int)

def send_message(message):
	for handler in ChatSocketHandler.socket_handlers:
		try:
			handler.write_message(message)
		except:
			logging.error('Error sending message', exc_info=True)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		if self.get_secure_cookie('nickname'):
			self.render('index.html', counts=(len(ChatSocketHandler.socket_handlers)+1))
		else:
			self.render('login.html')

	def post(self):
		nickname = self.get_argument('nickname')
		if nickname:
			self.set_secure_cookie('nickname', nickname)
			self.render('index.html', counts=(len(ChatSocketHandler.socket_handlers)+1))


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
	socket_handlers = set()

	def check_origin(self, origin):
		return True

	def open(self):
		ChatSocketHandler.socket_handlers.add(self)
		nickname = self.get_secure_cookie('nickname')
		send_message('<span class="welcome">%s加入聊天室.</span>' % nickname)

	def on_close(self):
		ChatSocketHandler.socket_handlers.remove(self)
		nickname = self.get_secure_cookie('nickname')
		send_message('<span class="welcome">%s离开了.</span>' % nickname)

	def on_message(self, message):
		message = '<span class="name">%s</span>: %s' % (self.get_secure_cookie('nickname'), message.encode('utf8'))
		send_message(message)


class ChatUserCountHandler(tornado.web.RequestHandler):
	def get(self, *args, **kwargs):
		self.write('%s' % len(ChatSocketHandler.socket_handlers))
		self.finish()


TORNADO_ROUTES = [('/', MainHandler),  # ('/new-msg/', ChatHandler),
                  ('/new-msg/socket', ChatSocketHandler),
	('/user-count', ChatUserCountHandler)]


class Application(tornado.web.Application):
	def __init__(self):
		handlers = TORNADO_ROUTES
		settings = TORNADO_SETTINGS
		tornado.web.Application.__init__(self, handlers, **settings)


def main():
	tornado.options.parse_command_line()
	application = Application()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.bind(options.port)
	http_server.start()
	tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
	main()