import tornado.wsgi
from  datetime  import  *
import time
import sys
sys.path.append("Manager/")
import CommentManager
import RecordManager
import ShopInfoManager

class CustomerCommentHandler(tornado.web.RequestHandler):
    def get(self):
        customer_id = self.get_argument('customer_id')
        record_id = self.get_argument('recordId')
        is_commented = CommentManager.has_comment(record_id)
        shop_name = CommentManager.get_comment_shopname(record_id)[0]
        if customer_id == RecordManager.get_customerId(record_id):
            self.render("../static/template/CustomerComment.html",
                        shop_name=shop_name, recordId = record_id,
                        isCommented=is_commented)

    def post(self):
        record_id = self.get_argument('recordId')
        star_rating = self.get_argument('starRating')
        content = self.get_argument('comment')
        comment_time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        CommentManager.set_comment(record_id, star_rating, content, comment_time)
        shopId = RecordManager.get_shopId(recordId)
        ShopInfoManager.update_comment_starRating(shopId)
        self.write("comment success")

