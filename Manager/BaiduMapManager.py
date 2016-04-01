#coding=utf-8
import tornado.wsgi
import urllib2
import json

AK_KEY = "wZNqARgljDouaTQYxPFEEm7k" # lyudison
# AK_KEY = "RRg5AgEQ6i8nb2FZQeXdNxv4" # hxm
TIME_OUT = 0.5

def get_duration_by_latlng(ori_lat, ori_lng, des_lat, des_lng):
    '''get duration by latitude and longitude

    Get the duration from one specified place to another one by driving with Baidu Map Web API

    Args:
        ori_lat: latitude of origin
        ori_lng: longitude of origin
        des_lat: latitude of destination
        des_lng: longitude of destination

    Returns:
        duration (seconds)
    '''
    # setting
    # TODO: get region by user input or intelligently request by Map API
    region = "广州"
    data_format = "json"

    # get navigation infomation by Baidu Map API
    url = "http://api.map.baidu.com/direction/v1?mode=driving&origin=%s,%s&destination=%s,%s&origin_region=%s&destination_region=%s&output=%s&ak=%s" % (ori_lat, ori_lng, des_lat, des_lng, urllib2.quote(region), urllib2.quote(region), data_format, AK_KEY)

    data = None
    try:
        urlfile = urllib2.urlopen(url, data=None, timeout=TIME_OUT)
        data =  urlfile.read()
    except Exception,e:
        # print 'class BaiduMapManager get_duration_by_latlng',str(e)
        return -1
    
    if data==None:
        # print 'class BaiduMapManager get_duration_by_latlng data==None'
        return -1
    if str(data)=='':
        # print 'class BaiduMapManager get_duration_by_latlng data[0]==\'\''
        return -1

    # print 'class BaiduMapManager get_duration_by_latlng data',data
    json_data = json.loads(data)

    # if find explicit route
    if json_data['type'] == 2 and json_data['result']['routes']:
        # print 'class BaiduMapManager get_duration_by_latlng get correct duration'
        return json_data['result']['routes'][0]['duration']
    # if implicit or not find return -1
    # print 'class BaiduMapManager get_duration_by_latlng cannot find explicit duration'
    return -1

def get_distance_by_latlng(ori_lat, ori_lng, des_lat, des_lng):
    '''get distance by latitude and longitude

    Get the distance from one specified place to another one by driving with Baidu Map Web API

    Args:
        ori_lat: latitude of origin
        ori_lng: longitude of origin
        des_lat: latitude of destination
        des_lng: longitude of destination

    Returns:
        distance (meters)
    '''
    # setting
    # TODO: get region by user input or intelligently request by Map API
    region = "广州"
    data_format = "json"

    # get navigation infomation by Baidu Map API
    url = "http://api.map.baidu.com/direction/v1?mode=driving&origin=%s,%s&destination=%s,%s&origin_region=%s&destination_region=%s&output=%s&ak=%s" % (ori_lat, ori_lng, des_lat, des_lng, urllib2.quote(region), urllib2.quote(region), data_format, AK_KEY)

    data = None
    try:
        urlfile = urllib2.urlopen(url, data=None, timeout=TIME_OUT)
        data =  urlfile.read()
    except Exception,e:
        # print 'class BaiduMapManager get_distance_by_latlng',str(e)
        return -1
    
    if data==None:
        # print 'class BaiduMapManager get_distance_by_latlng data==None'
        return -1
    if str(data)=='':
        # print 'class BaiduMapManager get_distance_by_latlng data[0]==\'\''
        return -1

    json_data = json.loads(data)

    # if find explicit route
    if json_data['type'] == 2 and json_data['result']['routes']:
        # print 'class BaiduMapManager get_distance_by_latlng get correct distance'
        return json_data['result']['routes'][0]['distance']
    # if implicit or not find return -1
    # print 'class BaiduMapManager get_distance_by_latlng cannot find explicit distance'
    return -1