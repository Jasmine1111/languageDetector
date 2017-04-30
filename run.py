# _*_ coding:utf8 _*_
from gevent.wsgi import WSGIServer
from server import app
import config
#import languageDetector as LD 
from sentiment_lstm import MyDict, classify2
import sentiment_lstm as SL
#LD.setup()
SL.setup()
print("All is done!")
http_server = WSGIServer(('', config.PORT), app)
http_server.serve_forever()
