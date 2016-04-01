import tornado.wsgi
import sys
sys.path.append("Manager/")
import ShopInfoManager
import FavorManager
import OAuthManager
import ShopPhotoManager
import BaiduMapManager
import AutoOrderManager

class CustomerFavorHandler(tornado.web.RequestHandler):
    def get(self):
        customer_id = OAuthManager.get_openid_base(self)

        # get favor shop by customerId
        shopId_list = FavorManager.get_shopId_list(customer_id)
        
        items = []
        for shop in shopId_list:
            shopId = shop[0]
            shop_img = ShopPhotoManager.get_shop_photo_urls(shopId)[0]
            shop_info = ShopInfoManager.get_shopAllInfo(shopId)
            shop_name = shop_info[1]
            star_rating = round(shop_info[7])*18
            dark_star_rating = (5-round(shop_info[7]))*18
            shop_phone = shop_info[4]
            if shop_info[4] == "null":
                shopPhone = ""

            bookable = False
            auto_order = AutoOrderManager.get_order_num(shopId)
            if auto_order != None and auto_order > 0:
                bookable = True


            item = [shop_img, shop_name, star_rating, shop_phone, shopId, dark_star_rating, bookable]
            items.append(item)

        self.render("../static/template/CustomerFavor.html",customerId=customer_id, items=items)
