#coding=utf-8
import tornado.wsgi
import tornado.web
import sys
import time
import datetime
sys.path.append("Handler/")
import CustomerBaseHandler
sys.path.append("Manager/")
import ShopInfoManager
import RecordManager
import CommentManager
import OAuthManager
import AutoOrderManager
import BaiduMapManager
import ShopPhotoManager
import FavorManager
import CustomerPersonInfoManager

def sort_shop(shopIdlist):
    """sort shop in shoplist, elect best eight shop

    Args:
        shopIdlist:{shopId:rank}

    Returns:
        top_eight: top eight shop
    """
    shopIdlist.sort(key=lambda d:d[11])

    top_eight = []
    for i in range(0, min(len(shopIdlist), 8)):
        shop = shopIdlist[i]
        top_eight.append(shop)

    return top_eight

# FIXME:(HXM) Shouldn't get account, password of shop
def shop_rank(longitude, latitude):
    """ranking the shop nearby

    Args:
        longitude: customer longitude
        latitude: customer latitude

    Returns:
        shoplist[0][0]:shopId of best shop
        shoplist[0][1]:shopName of best shop
        ...
        shoplist[7][10]:password of eighth shop
    """
    # get shop nearby
    shoplist_tuple = ShopInfoManager.get_shop_nearby(longitude, latitude)
    shoplist = [list(rec) for rec in shoplist_tuple]

    # get shop available (auto_order > 0) in shop nearby
    shop_available = []
    for shop in shoplist:
        auto_order_num = AutoOrderManager.get_order_num(shop[0])
        # print auto_order_num
        if auto_order_num != None and int(auto_order_num) > 0:
            shop_available.append(shop)

    # get shop rank in shop avilable
    shop_ranking = []
    for shop in shop_available:
        # calculate duration
        ori_lng = str(longitude)
        ori_lat = str(latitude)
        des_lng = ShopInfoManager.get_longitude(shop[0])
        des_lat = ShopInfoManager.get_latitude(shop[0])
        # print 'class CustomerShopListHandler shop_rank shop name',shop[1]
        distance_meter = BaiduMapManager.get_distance_by_latlng(ori_lat, ori_lng, des_lat, des_lng)
        if distance_meter==-1:
            continue
        distance = float(distance_meter) / 1000
        distance = '%.2f' % distance
        shop.append(distance)
        # calculate busy
        auto_order_num = int(AutoOrderManager.get_order_num(shop[0]))    #FIXME:(HXM)是否有可能随时变为0或None
        coming_car = int(RecordManager.get_unfinished_record_num(shop[0]))
        busy = coming_car / (auto_order_num + coming_car)
        # get starRating
        starRating = ShopInfoManager.get_starRating(shop[0])
        # print "duration:" + str(duration)

        # calculate rank using busy, duration, starRating
        rank = 1 * busy + 2 * starRating + 1 * float(distance)
        shop.append(rank)
        shop_ranking.append(shop)

    # get top eight shop
    top_eight = sort_shop(shop_ranking)

    result = top_eight
    return result

# TODO: 搜索算法 && shop rank test && ...
class CustomerShopListHandler(CustomerBaseHandler.CustomerBaseHandler):
    def get(self):
        openid = OAuthManager.get_openid_base(self)
        self.set_secure_cookie("user", openid)
        plateNumber = CustomerPersonInfoManager.get_plateNumber(openid)

        # jump to redirect page to get customer location
        # redirect request customer location which is get from wechat every second
        # KVDB will be banned if use while loop to get location
        # tonado.ioloop can not used, time.sleep() will block the thread and tornado is single-threaded       
        self.render("../static/template/CustomerShopListRedirect.html", openid = openid)

    def post(self):
        # print self.request.arguments
        if 'openid' in self.request.arguments:
            openid = self.get_argument('openid')    # get openid from html
            # shopId = self.get_argument('shopId')
            # try to get location from wechat
            customerId = openid
            Location = None
            Location = CustomerPersonInfoManager.get_location(openid)

            if Location == None:
                self.write("has no location")
            else:
                # print 'class CustomerShopListHandler post() location',Location
                longitude = float(Location.split(',')[0])
                latitude = float(Location.split(',')[1])
                shoplist = shop_rank(longitude, latitude)
                # data binding of CustomerShopList.html
                items = []
                for shop in shoplist:
                    shopImg = ShopPhotoManager.get_shop_photo_urls(shop[0])[0]
                    shopId = shop[0]
                    shopName = shop[1]
                    starRating = round(shop[7])*18
                    darkStarRating = (5-round(shop[7]))*18
                    shopPhone = shop[4]
                    distance = shop[11]
                    item = [shopImg, shopName, starRating, shopPhone,
                        shopId, distance, darkStarRating]
                    items.append(item)

                self.render("../static/template/CustomerShopList.html", customerId=customerId, items=items)