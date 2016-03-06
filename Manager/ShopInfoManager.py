import sys
sys.path.append("Interface/")
import DBInterface

def get_shopAllInfo(shopId):
	sql = "SELECT * FROM shop WHERE shopId = %s"
	result = DBInterface.query_for_one(sql, shopId)
	return result

def get_shopName(shopId):
	sql = "SELECT shopName FROM shop WHERE shopId = %s"
	result = DBInterface.query_for_one(sql, shopId)
	return result
