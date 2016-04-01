import tornado.wsgi
import sys
sys.path.append('Interface/')
import KVDBInterface

class ShopBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        client_cookie_username = self.get_secure_cookie("user")
        if client_cookie_username==None:
            return None
        server_session_username = "user"+str(client_cookie_username)
        print 'class ShopBaseHandler get_current_user() client_cookie_username: %s, server_session_username: %s' % (client_cookie_username, server_session_username)
        return KVDBInterface.get(server_session_username)
    def set_current_user(self, username):
        server_session_username = "user"+str(username)
        KVDBInterface.set(server_session_username,username)
        self.set_secure_cookie("user",username)
    def clear_current_user(self):
        client_cookie_username = self.get_secure_cookie("user")
        server_session_username = "user"+str(client_cookie_username)
        KVDBInterface.delete(server_session_username)
        self.clear_cookie("user")
        print 'class ShopBaseHandler clear_current_user() server_session_username: %s' % server_session_username