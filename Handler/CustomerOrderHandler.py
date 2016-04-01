import tornado.wsgi
import sys
import datetime
sys.path.append("Handler/")
import CustomerBaseHandler
sys.path.append("Manager/")
import ShopInfoManager
import RecordManager
import AutoOrderManager
import BaiduMapManager
import WechatMessageManager
import AutoOrderManager
import CustomerPersonInfoManager

class CustomerOrderHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../static/template/CustomerPlateNumError.html")

    def post(self):
        # add record when customer make an appointment
        customerId = self.get_argument('customerId')
        shopId_order = self.get_argument('shopId_order')

        plate_number = CustomerPersonInfoManager.get_plateNumber(customerId)

        auto_order_num = AutoOrderManager.get_order_num(shopId_order)
        
        if plate_number == None:
            self.write("unset plate number")
        elif RecordManager.is_customer_breach(customerId):
            self.write("customer breach")
        elif RecordManager.has_customer_unfinished_record(customerId):
            self.write("has unfinished record")
        elif auto_order_num <= 0:
            self.write("has no auto order")
        else:
            auto_order_num = AutoOrderManager.get_order_num(shopId_order)
            auto_order_num = int(auto_order_num) - 1
            AutoOrderManager.set_order_num(shopId_order, auto_order_num)

            if auto_order_num >= 0:
                shopId_order = self.get_argument('shopId_order')
                record_time = str(datetime.datetime.now()).split('.')[0]
                # get customer location
                Location = CustomerPersonInfoManager.get_location(customerId)

                ori_lng = float(Location.split(',')[0])
                ori_lat = float(Location.split(',')[1])

                # calculate journeyTime
                des_lng = ShopInfoManager.get_longitude(shopId_order)
                des_lat = ShopInfoManager.get_latitude(shopId_order)
                duration = BaiduMapManager.get_duration_by_latlng(ori_lat, ori_lng, des_lat, des_lng)
                arrive_time = datetime.datetime.now() + datetime.timedelta(seconds = duration)
                journey_time = str(arrive_time).split('.')[0]

                RecordManager.add_record(customerId, shopId_order, record_time, journey_time)
                WechatMessageManager.customer_order_remind(customerId, shopId_order)
            else:
                AutoOrderManager.set_order_num(shopId_order, 0)
                self.write("has no auto order")
