#coding=utf-8
import tornado.wsgi
import xml.etree.ElementTree as ET

import sys
sys.path.append("Manager/")
import WechatMessageTemplate
import AutoOrderManager
import CustomerPersonInfoManager

class WechatMessageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text

        if msgtype == 'event':
            event = data.find('Event').text
            if event == "subscribe":
                title = "欢迎使用车GO~"
                desc = "点击了解车GO!"
                picurl = "http://cargotest-cargo.stor.sinaapp.com/cargo%20logo%20black.png"
                url = "http://2.cargotest.sinaapp.com/customerhelp"
                response = WechatMessageTemplate.gen_text_picture_message(fromusername, tousername, title, desc, picurl, url)
                self.write(response)

            elif event == "LOCATION":
                location = data.find('Longitude').text + ',' + data.find('Latitude').text
                CustomerPersonInfoManager.set_location(fromusername, location)

            elif event == "CLICK":
                eventkey = data.find('EventKey').text
                # eventkey = "V1002_GOOD"
                if eventkey == "CUSTOMER_SERVICE":
                    text = "尊敬的车主，您好！\r\n有什么我们可以帮到您的？\r\n如果您有任何疑问，或是需要进行投诉，您可以直接回复本条消息，我们会尽快联系您进行处理。"
                    response = WechatMessageTemplate.gen_text_message(fromusername, tousername, text)
                    self.write(response)

        elif msgtype == "text":
            content = data.find('Content').text
            dic = {"hello":"你好！",
                "bye":"bye~"}
            result = dic[content]
            response = WechatMessageTemplate.gen_text_message(fromusername, tousername, result)
            self.write(response)
