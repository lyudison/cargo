import tornado.wsgi
import sys
sys.path.append("Manager/")
import ShopInfoManager
import OAuthManager

class WashCarHandler(tornado.web.RequestHandler):
    def get(self):
        openid = OAuthManager.get_openid_base(self)
        a = ShopInfoManager.get_shopAllInfo(1)
        shopId = ShopInfoManager.get_shopName(1)
        shopName = a[1]
        ownerName = a[2]
        address = a[3]
        shopPhone = a[4]
        longitude = a[5]
        latitude = a[6]
        starRating = a[7]
        desc = a[8]
        
        self.render("../static/template/CustomerShopList.html", openid=openid, shopName=shopName, starRating=starRating, address=address, shopPhone=shopPhone, desc=desc)
