#coding=utf-8
import tornado.wsgi
import sys
import json
sys.path.append("Manager/")
import ShopInfoManager

class CustomerMapHandler(tornado.web.RequestHandler):
    def get(self):
        # self.render("../static/template/CustomerMapRedirect.html")

        # get location
        if 'lng' and 'lat' in self.request.arguments:
            lng = self.get_argument('lng')
            lat = self.get_argument('lat')
            # request for nearby shop list
            shops_tuple = ShopInfoManager.get_shop_nearby(lng, lat)
            shops_list = [list(shop_tuple) for shop_tuple in shops_tuple]
            self.render("../static/template/CustomerMap.html", lat=lat, lng=lng, shops_list=shops_list)
            return
        self.write("cannot get location information")

    # unused
    def post(self):
        if 'lng' and 'lat' in self.request.arguments:
            lng = self.get_argument('lng')
            lat = self.get_argument('lat')
            shops_tuple = ShopInfoManager.get_shop_nearby(lng, lat)
            shops_list = [list(shop_tuple) for shop_tuple in shops_tuple]
            # print 'shops_list', shops_list
            self.render("../static/template/CustomerMap.html", lat=lat, lng=lng, shops_list=shops_list)

# unused
def convert_shops_list_to_dict(shops_list):
    '''
    Rtn:
        shops_dict = [
            {
                shop_id:,
                shop_name:,
                lat:,
                lng:
            }
        ]
    '''
    shops_dict = []
    for shop in shops_list:
        dict_shop = {
            'shop_id':shop[0],
            'shop_name':shop[1],
            'lat':shop[6],
            'lng':shop[5]
        }
        shops_dict.append(dict_shop)
    return shops_dict