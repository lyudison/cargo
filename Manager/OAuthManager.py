import tornado.wsgi
import urllib2
import json

# # not used yet. use when Wechat OAuth2.0 Scope is snsapi_userinfo
# class OAuthHandler(tornado.web.RequestHandler):
#     def get(self):
#         code = self.get_argument("code")
#         url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9&code=%s&grant_type=authorization_code" % code
#         urlfile = urllib2.urlopen(url)
#         data = urlfile.read()

#         data_string = json.loads(data)
#         access_token = data_string["access_token"]
#         open_id = data_string["openid"]
#         url2 = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (access_token, open_id)
#         urlfile2 = urllib2.urlopen(url2)
#         html = urlfile2.read()

#         self.write(html)

#     def post(self):
#         self.write("Hello world!")


def get_openid_base(self):
    '''get the openid of customer using Wechat OAuth2.0 snsapi_base method

    Args:
        self:

    Returns:
        openid:
    '''
    code = self.get_argument("code")

    url = ("https://api.weixin.qq.com/sns/oauth2/access_token?"
            "appid=wx97b25a5e35916ef6&secret=eff7f6509ec87516cb0c442aec7dd7e9&code=%s"
            "&grant_type=authorization_code") % code
    urlfile = urllib2.urlopen(url)

    data = urlfile.read()
    data_string = json.loads(data)
    access_token = data_string["access_token"]
    open_id = data_string["openid"]
    return open_id
