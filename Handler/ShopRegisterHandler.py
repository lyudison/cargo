import tornado.wsgi
import sys
sys.path.append("Manager/")
import ShopInfoManager
import ShopPhotoManager

class ShopRegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../static/template/ShopRegister.html")

    def post(self):

        # self.write(str(self.request.arguments))
        # return

        username = self.get_argument('username')
        if ShopInfoManager.has_account(username):
            self.write("Username Existed!")
            return

        password = self.get_argument('password')
        shopname = self.get_argument('shopname')
        address = self.get_argument('address')
        shopphone = self.get_argument('shopphone')
        ownername = self.get_argument('ownername')
        ownerphone = self.get_argument('ownerphone')
        description = "default description"
        # TODO: need to get location of shop
        longitude = latitude = 1.0

        # register and get corresponding shop id
        shop_id = ShopInfoManager.add_shop(shopname, ownername, address, ownerphone, longitude,
            latitude, description, username, password)

        # self.write("shop id: "+str(shop_id))
        # return 

        # save certificates by shop id
        business_certificate = transport_certificate = other_certificate = None
        if 'business_certificate' in self.request.files:
            business_certificate = self.request.files['business_certificate'][0]['body']
        if 'transport_certificate' in self.request.files:
            transport_certificate = self.request.files['transport_certificate'][0]['body']
        if 'other_certificate' in self.request.files:
            other_certificate = self.request.files['other_certificate'][0]['body']
        ShopPhotoManager.add_shop_certificates(shop_id,
            business_certificate,transport_certificate,other_certificate)

        self.write("Register succeeded!")
        # self.redirect("/shopmain")