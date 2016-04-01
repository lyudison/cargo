import sys
sys.path.append("Interface/")
import StorageInterface

def get_shop_photo_urls(shop_id):
    """get urls of shop photo

    Args:
        shop_id:

    Returns:
        urls: [photo_url, photo_url, ...]
              if storage has no shop photo, shop photo is setted default.
    """
    urls = StorageInterface.get_urls('shops',"photos/"+str(shop_id))
    if urls == []:
        return ['http://cargotest-cargo.stor.sinaapp.com/test.jpg']
    return urls

def add_shop_photo(shop_id, image_data):
    """add shop image

    Args:
        shop_id: shop id
        image_data: image raw data, must be jpg

    Returns:
        True if add successfully, otherwise False
    """
    max_index = StorageInterface.get_max_file_index('shops','photos/'+str(shop_id))
    # can only save 3 photos
    if max_index==2:
        return False

    filename = "%s.jpg" % str(max_index+1)
    folder_path = "photos/%s" % str(shop_id)
    StorageInterface.add_object('shops', folder_path, filename, image_data)
    return True

def set_shop_photo(shop_id, replace_photo_index, image_data):
    """set shop photo (seemly).

    Delete the specific photo, and add a new photo with another name, which will
    cause the dissorted images order.

    Args:
        shop_id: shop id 
        replace_photo_index: name of photo intended to be replace(delete)
        image_data: image raw data
    """
    bucket_name = 'shops'
    folder_path = "photos/%s" % str(shop_id)

    # get the max photo index
    max_index = StorageInterface.get_max_file_index('shops','photos/'+str(shop_id))

    # delete the photo
    delete_photo_name = "%s.jpg" % replace_photo_index
    StorageInterface.delete_object(bucket_name, folder_path, delete_photo_name)

    # add new photo with name str(max_index+1).jpg
    add_max_index = max_index + 1
    if max_index==replace_photo_index:
        add_max_index = max_index + 1
    add_photo_name = "%s.jpg" % str(add_max_index)
    StorageInterface.add_object(bucket_name, folder_path, add_photo_name, image_data)

def add_shop_certificates(shop_id, business_certificate=None, transport_certificate=None, other_certificate=None):
    dic = dict()
    if business_certificate:
        dic['business_certificate.jpg'] = business_certificate
    if transport_certificate:
        dic['transport_certificate.jpg'] = transport_certificate
    if other_certificate:
        dic['other_certificate.jpg'] = other_certificate

    StorageInterface.add_objects('shops', 'certificates/'+str(shop_id), dic)