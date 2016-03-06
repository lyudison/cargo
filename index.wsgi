# coding=utf-8
import tornado.wsgi
import sae
import sys
sys.path.append("Handler/")
import WechatMessageHandler
import CustomerShopListHandler
import ShopLoginHandler
import ShopMainHandler
import WechatValidHandler

settings = {

}

app = tornado.wsgi.WSGIApplication([
    (r"/wechat", WechatMessageHandler.WechatMessageHandler),
    (r"/test", CustomerShopListHandler.WashCarHandler),
	(r"/shopmain", ShopMainHandler.ShopMainHandler),
	(r"/shoplogin", ShopLoginHandler.ShopLoginHandler),
    #(r"/wechat", WechatValidHandler)    # use for verify wechat 
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")

application = sae.create_wsgi_app(app)

#Wechat ACCESS_TOKEN gKw_tLDvucl85w-yPs7E0rlt-S6a7fZbtTodeA0bVU1wTtkaUSiNsUZLo3iZRrKe_J00OG8qSW5ucjRE_mijlg
# {
#     "button":[
#     {
#         "type": "click", 
#         "name": "一键洗车", 
#         "key": "QUICKWASHING"
#     }, 
#     {
#         "type": "view", 
#         "name": "导航", 
#         "url": "http://1.baidumapapitest.sinaapp.com/"
#     }, 
#     {
#         "name": "我的车GO", 
#         "sub_button": [
#         {
#             "type": "click", 
#             "name": "使用说明", 
#             "key": "HANDBOOK"
#         }, 
#         {
#             "type": "view", 
#             "name": "收藏车店", 
#             "url": "http://www.baidu.com/"
#         }]
#     }]
# }
