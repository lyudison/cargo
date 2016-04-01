import sys
sys.path.append("Interface/")
import DBInterface

def get_customerId_list(shopId):
    sql = "SELECT customerId FROM favor WHERE shopId = %s"
    result = DBInterface.query_for_all(sql, shopId)
    return result

def get_shopId_list(customerId):
    """get shopId list which customer favor
    
    Args:
        customerId:

    Returns:
        result[0][0]:shopId0
        result[1][0]:shopId1
        result[2][0]:shopId2
        ...
    """
    sql = "SELECT shopId FROM favor WHERE customerId = %s"
    result = DBInterface.query_for_all(sql, customerId)
    return result

def add_favor(customerId, shopId):
    """add favor shop of customer

    Args:
        customerId:
        shopId:

    Returns:
    """
    sql = "INSERT INTO favor (customerId, shopId) VALUES (%s, %s)"
    param = (customerId, shopId)
    DBInterface.execute_sql(sql, param)
    return

def delete_favor(customerId, shopId):
    """add favor shop of customer

    Args:
        customerId:
        shopId:

    Returns:
    """
    sql = "DELETE FROM favor WHERE customerId=%s AND shopId=%s"
    param = (customerId, shopId)
    DBInterface.execute_sql(sql, param)
    return

def is_favored(customerId, shopId):
    """judge customer is favor shop or not

    Args:
        customerId:
        shopId:

    Returns:
        True/False
    """
    sql = "SELECT COUNT(*) FROM favor WHERE customerId=%s AND shopId=%s"
    param = (customerId, shopId)
    result = DBInterface.query_for_one(sql, param)
    num = result[0]
    if num > 0:
        return True
    else:
        return False