import datetime
import sys
sys.path.append("Interface/")
import DBInterface

def get_recordAllInfo(recordId):
    """get all information of record

    Args:
        recordId:

    Returns:
        result: [recordId, customerId, shopId, recordTime,
                customerBreach, shopBreach, finish, journeyTime]
    """
    sql = "SELECT * FROM record WHERE recordId = %s"
    result = DBInterface.query_for_one(sql, recordId)
    return result

def get_customerId(recordId):
    """get customerId of record

    Args:
        recordId:

    Returns:
        result: customerId
    """
    sql = "SELECT customerId FROM record WHERE recordId = %s"
    result = DBInterface.query_for_one_col(sql, recordId)
    return result

def get_shopId(recordId):
    """get shopId of record

    Args:
        recordId:

    Returns:
        result: shopId
    """
    sql = "SELECT shopId FROM record WHERE recordId = %s"
    result = DBInterface.query_for_one_col(sql, recordId)
    return result

def get_recordTime(recordId):
    """get recordTime of record

    Args:
        recordId:

    Returns:
        result: recordTime
    """
    sql = "SELECT recordTime FROM record WHERE recordId = %s"
    result = DBInterface.query_for_one_col(sql, recordId)
    return result

def add_record(customerId, shopId, recordTime, journeyTime):
    """add record

    Args:
        customerId:
        shopId:
        recordTime:
        journeyTime:
    """
    sql = "INSERT INTO record (customerId, shopId, recordTime, journeyTime) VALUES (%s, %s, %s, %s)"
    param = (customerId, shopId, recordTime, journeyTime)
    DBInterface.execute_sql(sql, param)
    return

def get_unfinished_record():
    """get all unfinished record

    Returns:
        result = [[recordId, customerId, shopId, recordTime,
                customerBreach, shopBreach, finish, journeyTime],
                [recordId, customerId, shopId, recordTime,
                customerBreach, shopBreach, finish, journeyTime],
                ...]

    """
    sql = "SELECT * FROM record WHERE finish=0"
    result = DBInterface.query_for_all(sql, None)
    return result

def get_unfinished_record_num(shopId):
    """get unfinished record number of one shop

    Args:
        shopId:

    Returns:
        num: unfinished record number of one shop
    """
    sql = "SELECT COUNT(*) FROM record WHERE finish=0 AND shopId=%s"
    result = DBInterface.query_for_one(sql, shopId)
    num = result[0]
    return num

# TODO: (HXM) test
def has_customer_unfinished_record(customerId):
    """get unfinished record number of one customer

    Args:
        customerId:

    Returns:
        num: unfinished record number of one customer
    """
    sql = "SELECT COUNT(*) FROM record WHERE finish=0 AND customerId=%s"
    result = DBInterface.query_for_one(sql, customerId)[0]
    if result > 0:
        return True
    else:
        return False

def record_breach(recordId):
    """set customer record breach when customer not arrived

    Args:
        recordId:
    """
    sql = "UPDATE record SET finish=1, customerBreach=1 WHERE recordId = %s"
    result = DBInterface.execute_sql(sql, recordId)
    return

def is_customer_breach(customerId):
    """judge customer breach or not in a recent day

    Args:
        customerId:
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    yesterday = str(yesterday).split('.')[0]
    sql = "SELECT COUNT(*) FROM record WHERE customerBreach=1 AND customerId=%s AND recordTime >= %s"
    param = (customerId, yesterday)
    result = DBInterface.query_for_one(sql, param)[0]
    if result > 0:
        return True
    else:
        return False

def get_unfinished_records_by_shopid(shop_id):
    """get all unfinished records by shop id

    Args:
        shop_id:

    Rtn:
        my_record = result[0]
        record_id = my_record[0]
        plate_number = my_record[1]
        customer_name = my_record[2]
        customer_phone = my_record[3]
        reserve_time = my_record[4]
    """
    sql = "SELECT R.recordId, C.plateNumber, C.customerName, C.customerPhone, R.recordTime, R.journeyTime\
        FROM record AS R, customer AS C\
        WHERE R.customerId=C.customerId AND R.shopId=%s AND R.finish=0"
    result_tuple = DBInterface.query_for_all(sql, shop_id)
    result = [list(item) for item in result_tuple]
    return result

def get_unfinished_records_after(shop_id, record_id):
    '''get all unfinished records with record id greater than record_id for shop with shop_id
    
    Rtn:
        similar with get_unfinished_records_by_shopid()
    '''
    sql = "SELECT R.recordId, C.plateNumber, C.customerName, C.customerPhone, R.recordTime, R.journeyTime\
        FROM record AS R, customer AS C\
        WHERE R.customerId=C.customerId AND R.shopId=%s AND R.finish=0 AND R.recordId>%s"
    param = (shop_id, record_id)
    result_tuple = DBInterface.query_for_all(sql, param)
    if(result_tuple==None):
        return []
    result = [list(item) for item in result_tuple]
    return result

def set_finish(record_id):
    """set record finish

    Args:
        record_id:

    Returns:
        result: the number of row which is set finished
    """
    sql = "UPDATE record SET finish=1 WHERE recordId=%s"
    result = DBInterface.execute_sql(sql, record_id)
    return

def get_records_interval(shop_id, start_date, end_date):
    '''get records which recordTime is between start_time and end_time

    Args: (for example)
        start_time: 2014-7-31
        end_time: 2014-8-5
        # time should be convert to datetime format (for example, 2014-7-31 15:30:31)

    Rtn:
        my_record = result[0]
        record_id = my_record[0]
        plate_number = my_record[1]
        customer_name = my_record[2]
        customer_phone = my_record[3]
        reserve_time = my_record[4]
    '''
    sql = "SELECT R.recordId, C.plateNumber, C.customerName, C.customerPhone, R.recordTime\
        FROM record AS R, customer AS C\
        WHERE R.shopId=%s AND R.finish=1\
          AND R.recordTime>=%s AND R.recordTime<=%s\
          AND R.customerId=C.customerId\
        ORDER BY R.recordId"
    # sql = "SELECT R.recordId, C.plateNumber, C.customerName, C.customerPhone, R.recordTime\
    #     FROM record AS R, customer AS C\
    #     WHERE R.shopId=%s AND R.finish=1 AND R.customerId=C.customerId\
    #     ORDER BY R.recordId"

    start_time = "00:00:00"
    end_time = "23:59:59"
    start_date+=' '+start_time
    end_date+=' '+end_time

    param = (shop_id, start_date, end_date)
    # param = shop_id
    result_tuple = DBInterface.query_for_all(sql, param)

    print 'result_tuple',result_tuple

    if result_tuple==None:
        return []
    result = [list(item) for item in result_tuple]
    return result

def get_records_interval_customer(customer_id, start_date, end_date):
    '''get records which recordTime is between start_time and end_time of customer

    Args: (for example)
        start_time: 2014-7-31
        end_time: 2014-8-5
        # time should be convert to datetime format (for example, 2014-7-31 15:30:31)

    Rtn:
        my_record = result[0]
        record_id = my_record[0]
        shop_id = my_record[1]
        recordTime = my_record[2]
        shopName = my_record[3]
    '''
    sql = "SELECT R.recordId, R.shopId, R.recordTime, S.shopName\
        FROM record AS R, shop AS S\
        WHERE R.customerId=%s AND R.finish=1\
          AND R.recordTime>=%s AND R.recordTime<=%s\
          AND R.shopId=S.shopId\
        ORDER BY R.recordTime DESC"
    # sql = "SELECT R.recordId, C.plateNumber, C.customerName, C.customerPhone, R.recordTime\
    #     FROM record AS R, customer AS C\
    #     WHERE R.shopId=%s AND R.finish=1 AND R.customerId=C.customerId\
    #     ORDER BY R.recordId"

    start_time = "00:00:00"
    end_time = "23:59:59"
    start_date+=' '+start_time
    end_date+=' '+end_time

    param = (customer_id, start_date, end_date)
    result_tuple = DBInterface.query_for_all(sql, param)

    # print 'result_tuple',result_tuple

    if result_tuple==None:
        return []
    result = [list(item) for item in result_tuple]
    return result