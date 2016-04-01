#coding=utf-8
import tornado.wsgi
import tornado.web
import sys
import time
sys.path.append("Handler/")
from CustomerBaseHandler import CustomerBaseHandler
sys.path.append("Manager/")
import ShopInfoManager
import RecordManager
import BaiduMapManager
import OAuthManager
import ShopPhotoManager
import CustomerPersonInfoManager
import AutoOrderManager

class CustomerSearchListHandler(CustomerBaseHandler):
    def get(self):
        openid = OAuthManager.get_openid_base(self)
        self.set_secure_cookie("user", openid)
        self.render("../static/template/CustomerSearchListRedirect.html", openid=openid)

    def post(self):
        # print 'class CustomerSearchListHandler','self.request.arguments',self.request.arguments
        
        openid = self.get_argument('openid')    # get openid from html
        # shopId = self.get_argument('shopId')
        # try to get location from wechat
        customerId = openid
        # request for nearby shop list

        Location = None
        Location = CustomerPersonInfoManager.get_location(openid)

        # if location not get yet, browser(client) keeps requesting
        if Location==None:
            print "has no location"
            self.write("has no location")

        # search for specific shop by name
        elif 'shop_name' in self.request.arguments:
            lng = float(Location.split(',')[0])
            lat = float(Location.split(',')[1])
            shop_name = self.get_argument('shop_name')
            raw_shop_ids = ShopInfoManager.get_shop_id_by_name(shop_name)
            shop_ids = [str(i).split(',')[0][1:] for i in raw_shop_ids] # solve tuple format problem

            shops = []
            if shop_ids!=None:
                for shop_id in shop_ids:
                    '''MySQL show warning message when search by long type (for example, shop_id)
                    '''
                    shop = ShopInfoManager.get_shopAllInfo(shop_id)
                    shop_img = ShopPhotoManager.get_shop_photo_urls(shop[0])[0]
                    shop_name = shop[1]
                    star_rating = round(shop[7])*18
                    dark_star_rating = (5-round(shop[7]))*18
                    shop_phone = shop[4]
                    if shop[4] == "null":
                        shop_phone = ""
                    shop_id = shop[0]

                    bookable = False
                    auto_order = AutoOrderManager.get_order_num(shop[0])

                    if auto_order != None and auto_order > 0:
                        bookable = True

                    distance_meter = BaiduMapManager.get_distance_by_latlng(lat, lng, shop[6], shop[5])
                    # if the shop cannot get distance, not display
                    if distance_meter==-1:
                        continue
                    # convert to kilometers and keep 2 decimal number
                    distance = float(distance_meter) / 1000
                    distance = '%.2f' % distance 

                    item = [shop_name, star_rating, shop_phone, distance,
                            shop_id, shop_img, dark_star_rating, bookable]
                    shops.append(item)
            self.render("../static/template/CustomerSearchList.html", customerId=customerId, items=shops, lng=lng, lat=lat)

        # request for all nearby shops
        else:
            lng = float(Location.split(',')[0])
            lat = float(Location.split(',')[1])
            shops_tuple = ShopInfoManager.get_shop_nearby(lng, lat) # without sorting with distance
            shops_list = [list(shop_tuple) for shop_tuple in shops_tuple]

            shops = []
            for shop in shops_list:
                shop_img = ShopPhotoManager.get_shop_photo_urls(shop[0])[0]
                shop_name = shop[1]
                star_rating = round(shop[7])*18
                dark_star_rating = (5-round(shop[7]))*18
                shop_phone = shop[4]
                if shop[4] == "null":
                    shop_phone = ""
                shop_id = shop[0]

                # judge if able to order
                bookable = False
                auto_order = AutoOrderManager.get_order_num(shop[0])
                if auto_order != None and auto_order > 0:
                    bookable = True

                distance_meter = BaiduMapManager.get_distance_by_latlng(lat, lng, shop[6], shop[5])
                # if the shop cannot get distance, not display
                if distance_meter==-1:
                    continue
                # distance_meter = 0
                # convert to kilometers and keep 2 decimal number
                distance = float(distance_meter) / 1000
                distance = '%.2f' % distance 
                
                item = [shop_name, star_rating, shop_phone, distance, shop_id, shop_img, dark_star_rating, bookable]
                shops.append(item)

            # sort by distance (from nearest to farest)
            shops.sort(key=lambda x: x[3])
            self.render("../static/template/CustomerSearchList.html", customerId=customerId, items=shops, lng=lng, lat=lat)