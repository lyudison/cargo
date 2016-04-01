import tornado.wsgi
import datetime
import sys
sys.path.append("Manager/")
import RecordManager
import WechatMessageManager

# TODO:(HXM) test WechatMessageManager!!
class RecordRefreshHandler(tornado.web.RequestHandler):
    def get(self):
        record_list = RecordManager.get_unfinished_record()
        for record in record_list:
            # Notifying the User when 30 minutes passed
            if ((datetime.datetime.now() - record[3]) > datetime.timedelta(minutes = 30) and
            (datetime.datetime.now() - record[3]) < datetime.timedelta(minutes = 31)):
                print "sending wechat message"
                WechatMessageManager.record_remind(record[1])

            # set record customer breach when 1 hour passed
            elif (datetime.datetime.now() - record[3]) > datetime.timedelta(hours = 1):
                WechatMessageManager.customer_breach_remind(record[1])
                RecordManager.record_breach(record[0])
            # else:
                # print "record refreshing..."