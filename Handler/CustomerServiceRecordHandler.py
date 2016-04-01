import tornado.wsgi
import datetime
import sys
sys.path.append("Manager/")
import RecordManager
import OAuthManager
import CommentManager
import ShopInfoManager


# TODO: (HXM) Test for date boundary
# TODO: (HXM) The length of every month in html
class CustomerServiceRecordHandler(tornado.web.RequestHandler):
    def get(self):
        customer_id = OAuthManager.get_openid_base(self)
        now_date = datetime.datetime.now().date()

        record_list = []
        # get record this month 
        this_month = datetime.datetime.now().date().month
        start_date = now_date.replace(day = 01)
        end_date = now_date.replace(month = this_month + 1,day = 01) - datetime.timedelta(days = 1)
        record_list_this_month = RecordManager.get_records_interval_customer(customer_id, str(start_date), str(end_date))
        for record in record_list_this_month:
            record.append(CommentManager.has_comment(record[0]))
        if len(record_list_this_month) > 0:
            record_list.append(record_list_this_month)

        # get record one month before
        one_month_before = this_month - 1
        if one_month_before == 0:
            one_month_before = 12
            star_date_one_month_before = now_date.replace(year = datetime.datetime.now().date().year - 1, month = one_month_before, day = 01)
            end_date_one_month_before = now_date.replace(day = 01) - datetime.timedelta(days = 1)
        else:
            star_date_one_month_before = now_date.replace(month = one_month_before, day = 01)
            end_date_one_month_before = now_date.replace(month = this_month, day = 01) - datetime.timedelta(days = 1)
        record_list_one_month_before = RecordManager.get_records_interval_customer(customer_id, str(star_date_one_month_before), str(end_date_one_month_before))
        for record in record_list_one_month_before:
            record.append(CommentManager.has_comment(record[0]))
        if len(record_list_one_month_before) > 0:
            record_list.append(record_list_one_month_before)

        # get record two month before
        two_month_before = this_month - 2
        if two_month_before <= 0:
            two_month_before = two_month_before + 12
            star_date_two_month_before = now_date.replace(year = datetime.datetime.now().date().year - 1, month = two_month_before, day = 01)
            end_date_two_month_before = now_date.replace(year = datetime.datetime.now().date().year - 1, month = one_month_before, day = 01) - datetime.timedelta(days = 1)
        else:
            star_date_two_month_before = now_date.replace(month = two_month_before, day = 01)
            end_date_two_month_before = now_date.replace(month = one_month_before, day = 01) - datetime.timedelta(days = 1)
        record_list_two_month_before = RecordManager.get_records_interval_customer(customer_id, str(star_date_two_month_before), str(end_date_two_month_before))
        for record in record_list_two_month_before:
            record.append(CommentManager.has_comment(record[0]))
        if len(record_list_two_month_before) > 0:
            record_list.append(record_list_two_month_before)

        # record_list = [record_list_this_month, record_list_one_month_before, record_list_two_month_before]

        self.render("../static/template/CustomerServiceRecord.html", customer_id=customer_id, record_list = record_list)
