#use for wechat valid
import tornado.wsgi
import sae
import hashlib

def checkSignature(signature, timestamp, nonce):
    token = 'cargo'
    args = [token, timestamp, nonce]
    args.sort()
    mysig = hashlib.sha1(''.join(args)).hexdigest()
    return mysig == signature

class WechatValidHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if checkSignature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('Valid Failed!')