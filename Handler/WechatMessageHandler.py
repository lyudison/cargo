import tornado.wsgi
import xml.etree.ElementTree as ET

import sys
sys.path.append("Manager/")
import WechatMessageTemplate

sys.path.append("Interface/")
import DBInterface

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
            		DBInterface.add_customer(fromusername)  
            		title = "insert success!"
            		desc = "1 minute to learn CarGO!"
            		picurl = "http://img0.imgtn.bdimg.com/it/u=2465500411,44984507&fm=21&gp=0.jpg"
            		url = "http://www.baidu.com"
            		response = WechatMessageTemplate.gen_text_picture_message(fromusername, tousername, title, desc, picurl, url)
            		self.write(response)
            
    		eventkey = data.find('EventKey').text
        	if eventkey == "V1001_GOOD":
            		title = "HANDBOOK"
            		desc = "1 minute to learn CarGO!"
            		picurl = "http://img0.imgtn.bdimg.com/it/u=2465500411,44984507&fm=21&gp=0.jpg"
            		url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx97b25a5e35916ef6&redirect_uri=http%3a%2f%2f2.cargotest.sinaapp.com%2ftest&response_type=code&scope=snsapi_base&state=1#wechat_redirect"
            		response = WechatMessageTemplate.gen_text_picture_message(fromusername, tousername, title, desc, picurl, url)
            		self.write(response)

            
    	elif msgtype == "text":
        	content = data.find('Content').text
		dic = {"hello":"hello~",
       			"bye":"bye~"}
        	result = dic[content]
        	response = WechatMessageTemplate.gen_text_message(fromusername, tousername, result)
    		self.write(response)
