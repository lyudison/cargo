#coding=utf-8
import sae.const
import MySQLdb

def get_conn():
    '''get connection to sae MySQL
    '''
    conn = MySQLdb.connect(host=sae.const.MYSQL_HOST, port=int(sae.const.MYSQL_PORT),
		    user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS,
		    db=sae.const.MYSQL_DB, charset = 'utf8')
    return conn

#执行SQL查询，结果以list(dict...)的形式返回
def query_for_list(query, *param):
	try:
		conn = get_conn()
		try:
			cur = conn.cursor()
			cur.execute(query, param)
			result = cur.fetchall()
			return result
		finally:
			cur.close()
			conn.close()
	except MySQLdb.Error as e:
		print ("Mysql Error Occured! %s" % (e))
		return None

#执行SQL更新操作（如update, insert, delete等）
def execute_sql(query, *param):
	try:
		conn = get_conn()
		try:
			cur = conn.cursor()
			cnt = cur.execute(query, param)
			conn.commit()
			return cnt
		except Exception as e:
			conn.rollback()
			raise e
		finally:
			cur.close()
			conn.close()
	except MySQLdb.Error as e:
		print ("Mysql Error Occured! %s" % (e))
		return None

#获取单行型查询结果
def query_for_one(query, *param):
	try:
		conn = get_conn()
		try:
			cur = conn.cursor()
			cur.execute(query, param)
			result = cur.fetchone()
			return result
		finally:
			cur.close()
			conn.close()
	except MySQLdb.Error as e:
		print("Mysql Error Occured! %s" % (e))
		return None

def query_for_one_col(query, *param):
	try:
		conn = get_conn()
		try:
			cur = conn.cursor()
			cur.execute(query, param)
			result = cur.fetchone()
			return result[0]
		finally:
			cur.close()
			conn.close()
	except MySQLdb.Error as e:
		print("Mysql Error Occured! %s" % (e))
		return None

def add_customer(customername):
	sql = "INSERT INTO customer (customerId) VALUES (%s)"
	execute_sql(sql, customername)


    

