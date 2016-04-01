# coding=utf-8
import urllib
import urllib2
import httplib
import json
import sys
sys.setdefaultencoding('utf8')
sys.path.append("Manager/")
import ShopPhotoManager
import WechatMessageTemplate
import RecordManager

#TODO(HXM) json中文消息回复测试
def record_remind(openId):
    """remind customer of record when 30 minutes passed

    Args:
        openId:
    """
    # get access_token
    url_request_token = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                        "&appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9")
    urlfile = urllib2.urlopen(url_request_token)
    data_token = urlfile.read()
    data_token = json.loads(data_token)
    access_token = data_token["access_token"]
    # content = content.encode('utf-8')
    # data = {
    #         "touser":openId,
    #         "msgtype":"text",
    #         "text":
    #             {
    #             "content":content
    #             }
    #         }
    # data_json = json.dumps(data)

    # send remind message
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token
    # Warnning: content内容只能为中文（包括中文标点，。！）！！！
    content = "尊敬的车主，您好！您已超出预约时间，请尽快到达。以免被记为违约，影响您今后的服务体验"
    
    data_json = """{"msgtype": "text", "touser": "%s", "text": {"content": "%s"}}""" % (openId, content)
    req = urllib2.Request(url)

    # urllib2 use body.length to calculate the Content-Length(every utf8 1 bit), but actually every chinese charecter  
    content_len = len(data_json)+len(content)/3*2
    req.add_header('Content-Length', content_len)

    res = urllib2.urlopen(req, data_json)

def customer_breach_remind(openId):
    """remind customer of record breach when 1 hour passed

    Args:
        openId:
    """
    # get access_token
    url_request_token = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                        "&appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9")
    urlfile = urllib2.urlopen(url_request_token)
    data_token = urlfile.read()
    data_token = json.loads(data_token)
    access_token = data_token["access_token"]

    # send remind message
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token
    # Warnning: content内容只能为中文（包括中文标点，。！）！！！
    content = ("尊敬的车主，您好！由于您未在预约1小时内接受洗车服务，您的行为将被视为违约。"
                "您在1天内您将不能使用预约功能。（其他功能仍然能正常使用）")
    
    data_json = """{"msgtype": "text", "touser": "%s", "text": {"content": "%s"}}""" % (openId, content)
    req = urllib2.Request(url)

    # urllib2 use body.length to calculate the Content-Length(every utf8 1 bit), but actually every chinese charecter  
    content_len = len(data_json)+len(content)/3*2
    req.add_header('Content-Length', content_len)

    res = urllib2.urlopen(req, data_json)


def customer_order_remind(customerId, shopId):
    """remind customer when customer make an appointment

    Args:
        customerId:
        shopId:
    """
    # get access_token
    url_request_token = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                        "&appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9")
    urlfile = urllib2.urlopen(url_request_token)
    data_token = urlfile.read()
    data_token = json.loads(data_token)
    access_token = data_token["access_token"]

    # send remind message
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token

    shopurl = "http://2.cargotest.sinaapp.com/customershopdetail?shopId=%s" % shopId
    picurl = ShopPhotoManager.get_shop_photo_urls(shopId)[0]

    data_json = """{
    "touser":"%s",
    "msgtype":"news",
    "news":{
        "articles": [
         {
             "title":"您已成功预约洗车",
             "description":"30分内有效，点击可查看详情",
             "url":"%s",
             "picurl":"%s"
         }
         ]
    }
    }""" % (customerId, shopurl, picurl)
    req = urllib2.Request(url)

    content_len = len(data_json)+40 # when you use chinese in uft8

    res = urllib2.urlopen(req, data_json)

def customer_comment_remind(recordId):
    """remind customer when customer arrived shop

    Args:
        recordId:
    """
    # get access_token
    url_request_token = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                        "&appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9")
    urlfile = urllib2.urlopen(url_request_token)
    data_token = urlfile.read()
    data_token = json.loads(data_token)
    access_token = data_token["access_token"]

    # send remind message
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token

    record = RecordManager.get_recordAllInfo(recordId)
    commenturl = "http://2.cargotest.sinaapp.com/customercomment?recordId=%s&customer_id=%s" % (recordId, record[1])
    picurl = ShopPhotoManager.get_shop_photo_urls(record[2])[0]
    print picurl

    data_json = """{
    "touser":"%s",
    "msgtype":"news",
    "news":{
        "articles": [
         {
             "title":"您已确认到店，请在完成服务后评价",
             "description":"点击进行评价",
             "url":"%s",
             "picurl":"%s"
         }
         ]
    }
    }""" % (record[1], commenturl, picurl)
    req = urllib2.Request(url)

    content_len = len(data_json)+44 # when you use chinese in uft8

    res = urllib2.urlopen(req, data_json)