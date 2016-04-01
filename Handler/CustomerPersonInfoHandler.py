# coding=utf-8
import tornado.wsgi
import sys
sys.path.append("Handler/")
from CustomerBaseHandler import CustomerBaseHandler
sys.path.append("Manager/")
import OAuthManager
import CustomerPersonInfoManager

class CustomerPersonInfoHandler(CustomerBaseHandler):
    def get(self):
    	open_id = OAuthManager.get_openid_base(self)
        self.set_secure_cookie("user", open_id)
        customer_info = CustomerPersonInfoManager.get_customer_all_info(open_id)
        if customer_info==None:
            customer_info = [open_id, '', '', '', '', '', '', '', '']
        else:
            if customer_info[5]==None:
                plate_num = ""
                plate_province = "粤"
                plate_city = "A"
            else:
                plate_number = customer_info[5]
                plate_province = plate_number[0]
                plate_city = plate_number[1]
                plate_num = ""
                for i in range(2, len(plate_number)):
                    plate_num = plate_num + str(plate_number[i])
            customer_info = [customer_info[0], customer_info[1], customer_info[2],
                    customer_info[3], customer_info[4], plate_province, plate_city, plate_num]
            print customer_info[2]
        self.render("../static/template/CustomerPersonInfo.html", customer_info=customer_info)

    def post(self):
        # get open id from cookie
        open_id = tornado.escape.xhtml_escape(self.current_user)

        customer_name = ''
        if 'customerName' in self.request.arguments:
            customer_name = self.get_argument('customerName')
        gender = 0 # default male
        if 'sex' in self.request.arguments:
            gender = self.get_argument('sex')
        customer_phone = ''
        if 'customerPhone' in self.request.arguments:
            customer_phone = self.get_argument('customerPhone')
        car_type = "0" # not used yet

        # get plate number
        for i in ('plateProvince', 'plateCity', 'plateNum'):
            if i not in self.request.arguments:
                print ('class CustomerPersonInfoHandler post():\n'
                        'ERROR: Unexisted or Incomplete plate number')
                self.write("请输入车牌号")
                return

        plate_province = self.get_argument('plateProvince')
        plate_city = self.get_argument('plateCity')
        plate_num = self.get_argument('plateNum')
        plate_number = plate_province+plate_city+str(plate_num)

        CustomerPersonInfoManager.set_customer_info(open_id,
            customer_name, gender, customer_phone, car_type, plate_number)

        customer_info = [open_id, customer_name, gender, customer_phone,
                    car_type, plate_province, plate_city, plate_num]
        self.render("../static/template/CustomerPersonInfo.html", customer_info=customer_info)