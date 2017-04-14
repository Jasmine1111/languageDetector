# _*_ coding:utf8 _*_
from gevent.wsgi import WSGIServer
from server import app
import config
import languageDetector as LD 

LD.setup()
http_server = WSGIServer(('', config.PORT), app)
http_server.serve_forever()
