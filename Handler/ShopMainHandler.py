#coding=utf-8
import tornado.wsgi
import json
import sys
sys.path.append("Handler/")
import ShopBaseHandler
sys.path.append("Manager/")
import RecordManager
import ShopInfoManager
import AutoOrderManager
import CommentManager
import WechatMessageManager

# some error responses
AUTO_ORDER_NUMBER_SET_SUCCEEDED = "AUTO_ORDER_NUMBER_SET_SUCCEEDED"
SET_RECORD_FINISH_SUCCEEDED = "SET RECORD FINISH SUCCEEDED"
LOGOUT_SUCCEEDED = "LOG OUT SUCCEEDED"
ERROR_POST_REQUEST = "ERROR POST REQUEST"

class ShopMainHandler(ShopBaseHandler.ShopBaseHandler):

    @tornado.web.authenticated
    def get(self):
        # print 'class ShopMainHandler get() self.current_user: %s' % self.current_user

        # get shop id
        username = tornado.escape.xhtml_escape(self.current_user)
        shop_id = ShopInfoManager.get_shopId_by_account(username)
        shop_info = ShopInfoManager.get_shopAllInfo(shop_id)
        shop_name = shop_info[1]
        comments = CommentManager.get_shop_comment(shop_id)

        # request for auto order number
        auto_order_num = AutoOrderManager.get_order_num(shop_id)

        if auto_order_num==None:
            auto_order_num = 0

        self.render("../static/template/ShopMain.html",auto_order=auto_order_num, shop_name=shop_name, comments=comments)
    
    @tornado.web.authenticated
    def post(self):
        """process with specific operation by arguments
        """
        # print 'class ShopMainHandler post() self.current_user: %s' % self.current_user

        # get shop id
        username = tornado.escape.xhtml_escape(self.current_user)
        shop_id = ShopInfoManager.get_shopId_by_account(username)
        
        # if request for records
        if 'record_id' in self.request.arguments:
            record_id = long(self.get_argument('record_id'))

            # if request for all unfinished records
            if record_id==-1:
                records = RecordManager.get_unfinished_records_by_shopid(shop_id)

                # sort as reverse order by record id
                records.sort(key=lambda x: x[0], reverse=True)

                # convert to json
                dict_records = convert_records_array_to_dict(records)
                json_records = json.dumps(dict_records)
                self.write(json_records)
                return
            # else request for latest unfinished records
            else:
                records = RecordManager.get_unfinished_records_after(shop_id, record_id)
                records.sort(key=lambda x: x[0], reverse=True)
                dict_records = convert_records_array_to_dict(records)
                json_records = json.dumps(dict_records)

                self.write(json_records)
                return

        # if request for records in interval time
        elif 'start_time' and 'end_time' in self.request.arguments:
            start_time = self.get_argument('start_time')
            end_time = self.get_argument('end_time')

            records = RecordManager.get_records_interval(shop_id, start_time, end_time)
            json_records = json.dumps(convert_records_array_to_dict(records))

            self.write(json_records)
            return

        # if a record has finished, save it
        elif 'finish_record_id' in self.request.arguments:
            finish_record_id = self.get_argument('finish_record_id')
            WechatMessageManager.customer_comment_remind(finish_record_id)
            RecordManager.set_finish(finish_record_id)
            self.write(SET_RECORD_FINISH_SUCCEEDED)
            return

        # set auto order number
        elif 'auto_order_num' in self.request.arguments:
            set_order_num = self.get_argument('auto_order_num')
            AutoOrderManager.set_order_num(shop_id, set_order_num)
            self.write(AUTO_ORDER_NUMBER_SET_SUCCEEDED)
            return

        # request for comment by record id
        elif 'comment_record_id' in self.request.arguments:
            comment_record_id = self.get_argument('comment_record_id')
            comment = CommentManager.get_comment_content('comment_record_id')
            if comment==None:
                comment = "尚未评价"
            self.write(comment)
            return

        # request to log out
        elif 'logout' in self.request.arguments:
            self.clear_current_user()
            print 'class ShopMainHandler post() log out!'
            self.write(LOGOUT_SUCCEEDED)
            return

        self.write(ERROR_POST_REQUEST)

def convert_records_array_to_dict(my_records):
    """
    format of records:
        my_record = my_records[0]
        record_id = my_record[0]
        plate_number = my_record[1]
        customer_name = my_record[2]
        customer_phone = my_record[3]
        reserve_time = my_record[4]
        eva_time = my_record[5]

    Rtn:
        dict_records = [
            {
                record_id:,
                car_number:,
                customer:,
                phone:,
                eva_time:,
                reserve_time:
            }
        ]
    """
    dict_records = []
    for my_record in my_records:
        dict_record = {
            'record_id':my_record[0],
            'car_number':my_record[1],
            'customer':my_record[2],
            'phone':my_record[3],
            'reserve_time':str(my_record[4])
        }
        if len(my_record)==6:
            dict_record['eva_time'] = str(my_record[5])
        dict_records.append(dict_record)
    return dict_records

# unused
def convert_comment_arr_to_dict(comment):
    """
    format of comment:
        customer_name = comment[0]
        customer_phone = comment[1]
        plate_number = comment[2]
        content = comment[3]
    Rtn:
        comment = {
            customer_name:,
            customer_phone:,
            plate_number:,
            content:
        }
    """
    pass