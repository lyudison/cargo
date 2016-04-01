# coding=utf-8
import sys
sys.path.append("Interface/")
import DBInterface
import KVDBInterface

def get_location(customerId):
    '''get location of customer from KVDB.

    Args:
        customerId

    Returns:
        location: longitude,latitude (example: 113.3740005493164,23.091400146484375)
    '''
    location = KVDBInterface.get(customerId)
    return location

def set_location(customerId, location):
    KVDBInterface.set(customerId, location)
    return

def get_customer_all_info(customerId):
    '''get all information of customer.

    Args:
        customerId

    Returns:
        result[0]:customerId
        result[1]:customerName
        result[2]:gender
        result[3]:customerPhone
        result[4]:carModelId
        result[5]:plateNumber
    '''
    sql = "SELECT * FROM customer WHERE customerId=%s"
    # print 'get customer info sql:',sql%customerId
    result = DBInterface.query_for_one(sql, customerId)
    return result

def get_customerName(customerId):
    '''get customer name of customer.

    Args:
        customerId

    Returns:
        customerName
    '''
    sql = "SELECT customerName FROM customer WHERE customerId = %s"
    result = DBInterface.query_for_one_col(sql, customerId)
    return result

def get_gender(customerId):
    '''get customer gender of customer.

    Args:
        customerId

    Returns:
        gender: 0 is male, 1 is female
    '''
    sql = "SELECT gender FROM customer WHERE customerId = %s"
    result = DBInterface.query_for_one_col(sql, customerId)
    return result

def get_customerPhone(customerId):
    '''get customer phone of customer.

    Args:
        customerId

    Returns:
        phone: phone is a string
    '''
    sql = "SELECT customerPhone FROM customer WHERE customerId = %s"
    result = DBInterface.query_for_one_col(sql, customerId)
    return result

# has not used
def get_carModelId(customerId):
    '''get customer car model of customer. has not used!!!

    Args:
        customerId

    Returns:
        carModelId
    '''
    sql = "SELECT carModelId FROM customer WHERE customerId = %s"
    result = DBInterface.query_for_one_col(sql, customerId)
    return result

def get_plateNumber(customerId):
    '''get plate number of customer.

    Args:
        customerId

    Returns:
        plateNumber: is a string. (example:粤A66666)
    '''
    sql = "SELECT plateNumber FROM customer WHERE customerId = %s"
    result = DBInterface.query_for_one_col(sql, customerId)
    return result

def add_customer_info(open_id, customer_name, gender, customer_phone, car_type, plate_number):
    '''add customer information

    Args:
        open_id: customerId
        customer_name:
        gender:
        customer_phone:
        car_type:
        plate_number:
    '''
    sql = "INSERT INTO customer\
            (customerId, customerName, gender, customerPhone, carModelId, plateNumber)\
            VALUES (%s, %s, %s, %s, %s, %s)"
    param = (open_id, customer_name, gender, customer_phone, car_type, plate_number)
    # print 'add customer info sql:',sql%param
    DBInterface.execute_sql(sql, param)

def update_customer_info(open_id, customer_name, gender, customer_phone, car_type, plate_number):
    '''update customer information

    Args:
        open_id: customerId
        customer_name:
        gender:
        customer_phone:
        car_type:
        plate_number:
    '''
    sql = "UPDATE customer\
            SET customerName=%s, gender=%s, customerPhone=%s, carModelId=%s, plateNumber=%s\
            WHERE customerId=%s"
    param = (customer_name, gender, customer_phone, car_type, plate_number, open_id)
    DBInterface.execute_sql(sql, param)

def set_customer_info(open_id, customer_name, gender, customer_phone, car_type, plate_number):
    '''set person info
    if not existed, insert a new one
    else modify the saved one

    Args:
        open_id: same as customerId
        customer_name: customerName
        customer_phone: customerPhone
        plate_number: plateNumber
    '''
    result = get_customer_all_info(open_id)
    # print 'open_id:',open_id
    # print 'get customer info:',result
    # if not existed, then create
    if result==None or result=='None':
        # print 'customer not existed'
        add_customer_info(open_id, customer_name, gender, customer_phone, car_type, plate_number)
    # existed, then modify
    else:
        # print 'customer existed'
        update_customer_info(open_id, customer_name, gender, customer_phone, car_type, plate_number)
