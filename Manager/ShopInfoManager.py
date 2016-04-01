# coding=utf-8
import hashlib
import sys
sys.path.append("Interface/")
import DBInterface
import StorageInterface

def get_shopAllInfo(shopId):
    '''get all information of shop

    Args:
        shopId

    Returns:
        result: [shopId, shopName, ownerName, address, shopPhone,
                  longitude, latitude, starRating, description,
                  account, password]
    '''
    sql = "SELECT * FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one(sql, shopId)
    return result

def get_shopName(shopId):
    '''get shopName of shop

    Args:
        shopId

    Returns:
        result: shopName
    '''
    sql = "SELECT shopName FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_ownerName(shopId):
    '''get ownerName of shop

    Args:
        shopId

    Returns:
        result: ownerName
    '''
    sql = "SELECT ownerName FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_address(shopId):
    '''get address of shop

    Args:
        shopId

    Returns:
        result: address
    '''
    sql = "SELECT address FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_shopPhone(shopId):
    '''get shopPhone of shop

    Args:
        shopId

    Returns:
        result: shopPhone
    '''
    sql = "SELECT shopPhone FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_longitude(shopId):
    '''get longitude of shop

    Args:
        shopId

    Returns:
        result: longitude
    '''
    sql = "SELECT longitude FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_latitude(shopId):
    '''get latitude of shop

    Args:
        shopId

    Returns:
        result: latitude
    '''
    sql = "SELECT latitude FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_starRating(shopId):
    '''get starRating of shop

    Args:
        shopId

    Returns:
        result: starRating
    '''
    sql = "SELECT starRating FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)
    return result

def get_description(shopId):
    '''get description of shop

    Args:
        shopId

    Returns:
        result: description
    '''
    sql = "SELECT description FROM shop WHERE shopId = %s"
    result = DBInterface.query_for_one_col(sql, shopId)

def has_account(account):
    '''judge the accout is occupied or not

    Args:
        account:

    Returns:
        True: accout is occupied
        False: accout is not occupied
    '''
    sql = "SELECT shopId FROM shop WHERE account = %s"
    result = DBInterface.query_for_one_col(sql, account)
    if result:
        return True
    else:
        return False

def check_login(account, password):
    '''check account account and password is correct or not when login

    Args:
        account:
        password:

    Returns:
        True: can login
        False: can not login
    '''
    sql = "SELECT password FROM shop WHERE account = %s"
    result = DBInterface.query_for_one_col(sql, account)

    # m = hashlib.md5()
    # m.update(password)
    # password_md5 = m.digest()
    # print password_md5
    # print "!!!"
    # print result
    if (result and result == password):
        return True
    else:
        return False


def add_shop(shopName, ownerName, address, shopPhone, longitude,
        latitude, description, account, password):
    '''add shop when shop register

    Args:
        shopName:
        ownerName:
        address:
        shopPhone:
        longtitude:
        latitude:
        description:
        account:
        password:

    Returns:
        shopId:
    '''
    # m = hashlib.md5()
    # m.update(password)
    # password = m.digest()
    # print m.digest()
    sql = "INSERT INTO shop  (shopName, ownerName, address, shopPhone, longitude, latitude, description, account, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    param = (shopName, ownerName, address, shopPhone, longitude,
            latitude, description, account, password)
    DBInterface.execute_sql(sql, param)
    shopId = get_shopId_by_account(account)
    return shopId

def get_shopId_by_account(account):
    '''get shopId by account

    Args:
        account:

    Returns:
        shopId:
    '''
    sql = "SELECT shopId FROM shop WHERE account = %s"
    result = DBInterface.query_for_one_col(sql, account)
    return result

def get_shop_id_by_name(shop_name):
    '''get shopId by shopName

    Args:
        shop_name:

    Returns:
        shopId:
    '''
    shop_name = '%'+shop_name+'%'
    sql = "SELECT shopId FROM shop WHERE shopName LIKE %s"
    result = DBInterface.query_for_all(sql, shop_name)
    return result    

def set_shopPhone(shopId, shopPhone):
    '''set shop phone

    Args:
        shopPhone:
    '''
    sql = "UPDATE shop SET shopPhone=%s WHERE shopId=%s"
    param = (shopPhone, shopId)
    DBInterface.execute_sql(sql, param)

def set_description(shopId, description):
    """set shop description

    Args:
        shopId:
        description:
    """
    sql = "UPDATE shop SET description=%s WHERE shopId=%s"
    param = (description, shopId)
    DBInterface.execute_sql(sql, param)

def set_starRating(shopId, starRating):
    """set shop starRating

    Args:
        shopId:
        description:
    """
    sql = "UPDATE shop SET starRating=%s WHERE shopId=%s"
    param = (float(starRating), int(shopId))
    DBInterface.execute_sql(sql, param)

def set_password(shopId, password):
    """set shop password

    Args:
        shopId:
        password:
    """
    sql = "UPDATE shop SET password=%s WHERE shopId=%s"
    param = (password, shopId)
    DBInterface.execute_sql(sql, param)

#TODO:(HXM) 经纬度范围有待调整
def get_shop_nearby(longitude, latitude):
    '''get all shop nearby

    Args:
        longitude:
        latitude:

    Returns:
        result: [[shopId, shopName, ownerName, address, shopPhone, longitude,
                latitude, starRating, description, account, password],
                 [shopId, shopName, ownerName, address, shopPhone, longitude,
                latitude, starRating, description, account, password],
                  ...]
    '''
    search_range = 0.03
    sql = "SELECT * FROM shop WHERE longitude < %s AND longitude > %s AND latitude < %s AND latitude > %s"
    location = (float(longitude)+search_range, float(longitude)-search_range,
                float(latitude)+search_range, float(latitude)-search_range)
    result = DBInterface.query_for_all(sql, location)

    while len(result) < 5:
        search_range = float(search_range + 0.03)
        location = (float(longitude)+search_range, float(longitude)-search_range,
                    float(latitude)+search_range, float(latitude)-search_range)
        result = DBInterface.query_for_all(sql, location)
    return result

def update_comment_starRating(shopId):
    sql = "SELECT AVG(Com.starRating)\
        FROM record AS Rec, comment AS Com\
        WHERE Rec.shopId=%s AND Com.recordId=Rec.recordId"
    starRating = DBInterface.query_for_one(sql, shopId)[0]
    set_starRating(shopId, starRating)
    return