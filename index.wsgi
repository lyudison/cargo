# coding=utf-8
import tornado.wsgi
import sae
import sys
sys.path.append("Handler/")

from CustomerNavigateHandler import CustomerNavigateHandler
from CustomerCommentHandler import CustomerCommentHandler
from CustomerFavorHandler import CustomerFavorHandler
from CustomerPersonInfoHandler import CustomerPersonInfoHandler
from CustomerServiceRecordHandler import CustomerServiceRecordHandler
from CustomerShopDetailHandler import CustomerShopDetailHandler
from CustomerShopListHandler import CustomerShopListHandler
from CustomerSearchListHandler import CustomerSearchListHandler
from CustomerMapHandler import CustomerMapHandler
from CustomerOrderHandler import CustomerOrderHandler
from CustomerHelpHandler import CustomerHelpHandler

from ShopHelpHandler import ShopHelpHandler
from ShopLoginHandler import ShopLoginHandler
from ShopMainHandler import ShopMainHandler
from ShopRegisterHandler import ShopRegisterHandler
from ShopInfoHandler import ShopInfoHandler

from WechatMessageHandler import WechatMessageHandler

from RecordRefreshHandler import RecordRefreshHandler
# from WechatValidHandler import WechatValidHandler

settings = dict(
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    login_url="/shoplogin",
    # "xsrf_cookies":True
    # debug=True,
)

app = tornado.wsgi.WSGIApplication([
    #customer
    (r"/customernavigate", CustomerNavigateHandler),
    (r"/customercomment", CustomerCommentHandler),
    (r"/customerfavor", CustomerFavorHandler),
    (r"/customerpersoninfo", CustomerPersonInfoHandler),
    (r"/customerservicerecord", CustomerServiceRecordHandler),
    (r"/customershopdetail", CustomerShopDetailHandler),
    (r"/customershoplist", CustomerShopListHandler),
    (r"/customersearchlist", CustomerSearchListHandler),
    (r"/customermap", CustomerMapHandler),
    (r"/customerorder", CustomerOrderHandler),
    (r"/customerhelp", CustomerHelpHandler),
    #shop
	(r"/shophelp", ShopHelpHandler),
	(r"/shoplogin", ShopLoginHandler),
    (r"/shopmain", ShopMainHandler),
    (r"/shopregister", ShopRegisterHandler),
    (r"/shopinfo", ShopInfoHandler),
    #wechat
    (r"/wechat", WechatMessageHandler),
    #record refresh
    (r"/recordrefresh", RecordRefreshHandler)
    # (r"/wechat", WechatValidHandler)    # use for verify wechat 
], **settings)

application = sae.create_wsgi_app(app)
