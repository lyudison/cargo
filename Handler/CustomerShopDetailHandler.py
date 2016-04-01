# coding=utf-8
import tornado.wsgi
import datetime
import sys
sys.path.append("Handler/")
import CustomerBaseHandler
sys.path.append("Manager/")
import ShopInfoManager
import ShopPhotoManager
import CommentManager
import RecordManager
import BaiduMapManager
import FavorManager
import AutoOrderManager

class CustomerShopDetailHandler(CustomerBaseHandler.CustomerBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/customershoplist")
            return
        customerId = self.current_user
        shopId = self.get_argument('shopId')

        shop_photo_urls = ShopPhotoManager.get_shop_photo_urls(shopId)
        shop = ShopInfoManager.get_shopAllInfo(shopId)
        shopId = shop[0]
        shop_name = shop[1]
        address = shop[3]
        shop_phone = shop[4]
        if shop[4] == None or shop[4] == "null":
            shop_phone = ""
        star_rating = round(shop[7])*18
        dark_star_rating = (5-round(shop[7]))*18
        desc = shop[8]
        if desc==None or desc=='N':
            desc = "暂无描述"
        
        bookable = False
        auto_order = AutoOrderManager.get_order_num(shopId)
        if auto_order != None and auto_order > 0:
            bookable = True

        comments = CommentManager.get_shopcomment(shopId)
        for comment in comments:
            if comment[4]==None:
                comment[4] = "匿名"

        isFavor = FavorManager.is_favored(customerId, shopId)

        self.render("../static/template/CustomerShopDetail.html", customerId = customerId,
            shopId=shopId, shopName=shop_name, lightStar=star_rating, darkStar=dark_star_rating,
            address=address, shopPhone=shop_phone, description=desc, comments = comments,
            shopPhotoUrls=shop_photo_urls, isFavor=isFavor, bookable=bookable)

    # TODO: (HXM) add record & shop favor
    def post(self):
        # add/delete favor shop of customer
        if 'shopId_favor' in self.request.arguments:
            shopId_favor = self.get_argument('shopId_favor')
            customerId = self.get_argument('customerId')
            isFavor = self.get_argument('isFavor')
            if isFavor == "True":
                FavorManager.add_favor(customerId, shopId_favor)
            else:
                FavorManager.delete_favor(customerId, shopId_favor)
