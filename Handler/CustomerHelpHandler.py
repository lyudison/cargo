import tornado.wsgi

class CustomerHelpHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../static/template/CustomerHelp.html")
