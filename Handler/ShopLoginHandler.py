import tornado.wsgi

import sys
sys.path.append("Handler/")
import ShopBaseHandler

class ShopLoginHandler(ShopBaseHandler.ShopBaseHandler):
    def get(self):
        self.write('<html><body><form action="/shoplogin" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/shopmain")
