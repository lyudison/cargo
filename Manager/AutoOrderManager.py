import sys
sys.path.append("Interface/")
import KVDBInterface

def set_order_num(shopId, order_num):
    """set Order number of shop.

    Args:
        shopId:
        order_num: the auto order number

    Returns:
    """
    KVDBInterface.set(shopId, order_num)

def get_order_num(shopId):
    """get Order number of shop.

    Args:
        shopId:

    Returns:
        order_num: the auto order number
    """
    order_num = KVDBInterface.get(shopId)
    return order_num
