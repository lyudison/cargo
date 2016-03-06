import tornado.wsgi
import sys
sys.path.append("Handler/")
import ShopBaseHandler

class ShopMainHandler(ShopBaseHandler.ShopBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/shoplogin")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
