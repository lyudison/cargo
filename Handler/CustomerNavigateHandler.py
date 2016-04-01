import tornado.wsgi
import sys
sys.path.append("Manager/")
import ShopInfoManager

class CustomerNavigateHandler(tornado.web.RequestHandler):
    def get(self):
        shopId = self.get_argument('shopId')
        # shopId = 3
        shop = ShopInfoManager.get_shopAllInfo(shopId)
        lng = shop[5]
        lat = shop[6]
        name = shop[1]
        self.render("../static/template/CustomerNavigator.html",
                    lng=lng, lat=lat, name=name)
        # self.render("../static/template/CustomerNavigatorCommon.html", lat=lat, lng=lng, name = name)
