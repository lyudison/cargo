# coding=utf-8
import tornado.wsgi

import sys
sys.path.append("Handler/")
import ShopBaseHandler
sys.path.append("Manager/")
import ShopInfoManager

class ShopLoginHandler(ShopBaseHandler.ShopBaseHandler):
    
    def get(self):
        '''
        self.write('<html><body><form action="/shoplogin" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
        '''
        self.render("../static/template/ShopLogin.html")

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        isLogin = ShopInfoManager.check_login(username, password)

        # self.write("username:"+username+" password:"+password)
        if isLogin:
            self.set_current_user(username)
            self.write("login_succeed")
        else:
            # self.redirect("/login")
            self.write("login_fail")
        # self.finish()
