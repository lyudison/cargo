#coding=utf-8
import tornado.wsgi
import sys
sys.path.append("Handler/")
import ShopBaseHandler
sys.path.append("Manager/")
import ShopPhotoManager
import ShopInfoManager

class ShopInfoHandler(ShopBaseHandler.ShopBaseHandler):

    @tornado.web.authenticated
    def get(self):
        # print 'class ShopInfoHandler get() self.current_user: %s' % self.current_user

        # get shop info and image's urls
        username = tornado.escape.xhtml_escape(self.current_user)
        shop_id = ShopInfoManager.get_shopId_by_account(username)
        shop_info = ShopInfoManager.get_shopAllInfo(shop_id)

        # shop info for display
        shop = [
            shop_info[1],
            shop_info[3],
            shop_info[4],
            shop_info[8]
        ]

        # shop images for display
        imgUrls = ShopPhotoManager.get_shop_photo_urls(shop_id)

        # 3 images are required for front end to display (though stupid)
        while len(imgUrls)<3:
            imgUrls.append('http://cargotest-cargo.stor.sinaapp.com/test.jpg')

        # owner info for display
        owner_info = [
            shop_info[2],
            shop_info[4]
        ]

        self.render("../static/template/ShopInformation.html", shop=shop,
            imgUrls=imgUrls, owner_info=owner_info, username=username)

    @tornado.web.authenticated
    def post(self):
        # get shop id
        username = tornado.escape.xhtml_escape(self.current_user)
        shop_id = ShopInfoManager.get_shopId_by_account(username)
        shop_info = ShopInfoManager.get_shopAllInfo(shop_id)

        # set shop phone
        if 'shop_phone' in self.request.arguments:
            shop_phone = self.get_argument('shop_phone')
            ShopInfoManager.set_shopPhone(shop_id, shop_phone)

        # set shop description 
        elif 'description' in self.request.arguments:
            description = self.get_argument('description')
            ShopInfoManager.set_description(shop_id, description)

        # upload image
        elif 'replace_index' in self.request.arguments:
            if 'shop_image' in self.request.files:
                replace_index = self.get_argument('replace_index')
                shop_image = self.request.files['shop_image'][0]['body']
                print 'class ShopInfoHandler post() replace_index',replace_index
                if replace_index=='t':
                    ShopPhotoManager.add_shop_photo(shop_id, shop_image)
                else:
                    ShopPhotoManager.set_shop_photo(shop_id, replace_index, shop_image)

        # set password
        elif 'old_password' and 'new_password' in self.request.arguments:
            old_password = self.get_argument('old_password')
            new_password = self.get_argument('new_password')
            real_password = shop_info[10]
            if real_password!=old_password:
                self.write("wrong old password")
                return
            ShopInfoManager.set_password(shop_id, new_password)

        # set owner phone
        elif 'owner_phone' in self.request.arguments:
            owner_phone = self.get_argument('owner_phone')
            ShopInfoManager.set_shopPhone(shop_id, owner_phone)

        self.redirect("/shopinfo") 