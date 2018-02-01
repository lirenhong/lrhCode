import tornado.ioloop
import tornado.web
from tornado import gen
from tornado import httpclient

class MainHandler(tornado.web.RequestHandler):
    import pdb;pdb.set_trace()
    @gen.coroutine
    def get(self):
        import pdb;pdb.set_trace()
        http_client = httpclient.AsyncHTTPClient()
        result = yield http_client.fetch("http://www.baidu.com")
        self.write(result.body)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    import pdb;pdb.set_trace()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
