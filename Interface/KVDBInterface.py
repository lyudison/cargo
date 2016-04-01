#coding=utf-8
import sae.kvdb
import MySQLdb

def set(key, value):
    """set method in KVDB.

    Args:
        key:
        value:
    """
    kv = sae.kvdb.KVClient()
    key = str(key)
    kv.set(key, value)
    kv.disconnect_all()
    return

def add(key, value):
    """add method in KVDB.

    Args:
        key:
        value:
    """
    kv = sae.kvdb.KVClient()
    key = str(key)
    kv.add(key, value)
    kv.disconnect_all()
    return

def get(key):
    """get method in KVDB.

    Args:
        key:

    Returns:
        value:
    """
    kv = sae.kvdb.KVClient()
    key = str(key)
    value = kv.get(key)
    kv.disconnect_all()
    return value

def delete(key):
    """get method in KVDB.

    Args:
        key:
    """
    kv = sae.kvdb.KVClient()
    key = str(key)
    kv.delete(key)
    kv.disconnect_all()
    return

def replace(key, value):
    """replace method in KVDB.The same use with set, but only work in key exist.
    
    Args:
        key:
        value:
    """
    kv = sae.kvdb.KVClient()
    key = str(key)
    kv.replace(key, value)
    kv.disconnect_all()
    return