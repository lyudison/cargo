import tornado.wsgi

class CustomerBaseHandler(tornado.web.RequestHandler):
    # use for cookie
    def get_current_user(self):
        return self.get_secure_cookie("user")
