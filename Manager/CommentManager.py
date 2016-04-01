# coding=utf-8
import sys
sys.path.append("Interface/")
import DBInterface

def has_comment(recordId):
    """judge record has comment or not.

    Args:
        recordId:

    Returns:
        True: record has commented
        False: record has not commented
    """
    sql = "SELECT COUNT(*) FROM comment WHERE recordId=%s"
    result = DBInterface.query_for_one(sql, recordId)[0]
    if result > 0:
        return True
    else:
        return False

def get_shopcomment(shopId):
    '''get shop's comment by shopId.

    Args:
        shopId

    Returns:
        result[0][0]:recordId
        result[0][1]:starRating
        result[0][2]:contents
        result[0][3]:commentTime
        result[0][4]:customerName
        result[1][0]:...
    '''
    sql = "SELECT Com.recordId, Com.starRating, Com.contents, Com.commentTime, Cus.customerName\
        FROM record AS Rec, customer AS Cus, comment AS Com\
        WHERE Rec.customerId=Cus.customerId AND Rec.recordId=Com.recordId AND Rec.shopId=%s"
    result_tuple = DBInterface.query_for_all(sql, shopId)
    result = [list(item) for item in result_tuple]

    # sql = "SELECT * FROM comment WHERE recordId IN (SELECT recordId FROM record WHERE shopId = %s)"
    # result = DBInterface.query_for_all(sql, shopId)
    return result

def set_comment(recordId, starRating, contents, commentTime):
    """set record's comment.

    Args:
        recordId:
        starRating:
        contents：
        commentTime:

    """
    sql = "INSERT INTO comment VALUES (%s, %s, %s, %s)"
    param = (recordId, starRating, contents, commentTime)
    DBInterface.execute_sql(sql, param)

# redefined by lyudison
def get_shop_comment(shop_id):
    '''
    Rtn:
        comment = result[0]
        customer_name = comment[0]
        customer_phone = comment[1]
        plate_number = comment[2]
        content = comment[3]
        star_rating = comment[4]
    '''
    sql = "SELECT Cus.customerName, Cus.customerPhone, Cus.plateNumber, Com.contents, Com.starRating\
        FROM customer AS Cus, comment AS Com, record AS Rec\
        WHERE Rec.shopId=%s AND Rec.recordId=Com.recordId AND Cus.customerId=Rec.customerId"
    result_tuple = DBInterface.query_for_all(sql, shop_id)
    result = [list(item) for item in result_tuple]
    return result

def get_comment(record_id):
    '''
    Rtn:
        comment = result
        similar with get_shop_comment
    '''
    sql = "SELECT Cus.customerName, Cus.customerPhone, Cus.plateNumber, Com.contents\
        FROM customer AS Cus, comment AS Com, record AS Rec\
        WHERE Rec.recordId=%s AND Rec.recordId=Com.recordId"
    result_tuple = DBInterface.query_for_one(sql, record_id)
    result = list(result_tuple)
    return result

def get_comment_shopname(record_id):
    '''
    Rtn:
        comment = result
        comment[0] = shopName
        comment[1] = starRating
        comment[2] = contents
    '''
    sql = "SELECT Shp.shopName\
        FROM shop AS Shp, record AS Rec\
        WHERE Rec.recordId=%s AND Shp.shopId=Rec.shopId"
    result_tuple = DBInterface.query_for_one(sql, record_id)
    result = list(result_tuple)
    return result

def get_comment_content(record_id):
    '''
    Rtn:
        comment = result
        similar with get_shop_comment
    '''
    # sql = "SELECT Com.contents\
    #     FROM customer AS Cus, comment AS Com, record AS Rec\
    #     WHERE Rec.recordId=%s AND Rec.recordId=Com.recordId"
    sql = "SELECT contents FROM comment WHERE recordId=%s"
    result = DBInterface.query_for_one(sql, record_id)
    return result