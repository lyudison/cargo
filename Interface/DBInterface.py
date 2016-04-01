#coding=utf-8
import sae.const
import MySQLdb

def get_conn():
    '''get connection to sae MySQL.
    '''
    conn = MySQLdb.connect(host=sae.const.MYSQL_HOST, port=int(sae.const.MYSQL_PORT),
                            user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS,
                            db=sae.const.MYSQL_DB, charset = 'utf8')
    return conn

# def query_for_list(query, param):
#     """not used now
#     """
#     try:
#         conn = get_conn()
#         try:
#             cur = conn.cursor()
#             cur.execute(query, param)
#             result = cur.fetchall()
#             return result
#         finally:
#             cur.close()
#             conn.close()
#     except MySQLdb.Error as e:
#         print ("Mysql Error Occured! %s" % (e))
#         return None

def execute_sql(query, param):
    """use for operator update, insert, delete...

    Args:
        query: the sql statement
        param: 

    Returns:
        cnt: the number of affected row
    """
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

def query_for_all(query, param):
    """select for multi-row.

    Args:
        query:
        param:

    Returns:
        result[0][0]: first row first column
        result[0][1]: first row second column
        ...
        result[1][0]: second row first column
        ...
    """
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
        print("Mysql Error Occured! %s" % (e))
        return None

def query_for_one(query, param):
    """select for one row.

    Args:
        query:
        param:

    Returns:
        result[0]: first element
        result[1]: second element
        ...
    """
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

def query_for_one_col(query, param):
    """select for one element.

    Args:
        query:
        param:

    Returns:
        element:
    """
    try:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(query, param)
            result = cur.fetchone()
            if result == None:
                return None
            else:
                element = result[0]
                return element
        finally:
            cur.close()
            conn.close()
    except MySQLdb.Error as e:
        print("Mysql Error Occured! %s" % (e))
        return None





