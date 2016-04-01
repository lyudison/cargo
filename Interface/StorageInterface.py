#coding=utf-8
from sae.storage import Bucket
from sae.ext.storage import monkey
monkey.patch_all()
import os

def get_urls(bucket_name, folder_path):
    """get resource urls from storage

    Args:
        bucket_name: the name of bucket
        folder_path: resources folder path

    Returns:
        list of resource urls
    """
    bucket = Bucket(bucket_name)

    folder_path+='/' # folder should be end with '/'

    # if no file
    files = [i for i in bucket.list(path=folder_path)]
    if len(files) == 0:
        return []

    # else has files
    filenames = []
    for item in [i['name'] for i in bucket.list(path=folder_path) if i['name'][-3:]=="jpg"]:
        filenames.append(item)
    return [bucket.generate_url(i) for i in filenames]

def add_objects(bucket_name, folder_path, objects):
    """add objects

    Args:
        bucket: name of bucket
        folder_path: folder path
        objects: dictionary of filename and its data, for example:

            objects['sample.txt']="hello world"
    """
    bucket = Bucket(bucket_name)
    folder_path = complete_folder(folder_path)

    for key in objects.keys():
        object_path = "%s%s" % (folder_path, key)
        virtual_object_path = "/s/%s/%s" % (bucket_name, object_path)
        if is_file_existed(virtual_object_path):
            print 'class StorageInterface add_objects() file existed! object_path: %s' % object_path
            continue
        bucket.put_object(object_path, objects[key])

def add_object(bucket_name, folder_path, object_name, object_data):
    """add object

    Args:
        bucket_name: name of bucket
        folder_path: folder path
        object_name: name of object
        object_data: object data

    Returns:
        True if add successfully
        False if object existed
    """
    bucket = Bucket(bucket_name)
    folder_path = complete_folder(folder_path)
    object_path = "%s%s" % (folder_path, object_name)

    virtual_object_path = "/s/%s/%s" % (bucket_name, object_path)
    print 'class StorageInterface add_object() virtual_object_path: %s' % virtual_object_path
    if is_file_existed(virtual_object_path):
        print 'class StorageInterface add_object() file existed! object_path: %s' % object_path
        return False
    
    print 'class StorageInterface add_object() start put_object() object_path: %s' % object_path
    # print 'class StorageInterface add_object() start put_object() object_data[0]: %s' % str(object_data)[0]
    bucket.put_object(object_path, object_data)
    print 'end'
    return True

def delete_object(bucket_name, folder_path, object_name):
    """delete object

    Args:
        bucket_name: name of bucket
        folder_path: folder path
        object_name: name of object

    Returns:
        True if delete successfully
        False if object unexisted
    """
    bucket = Bucket(bucket_name)
    folder_path = complete_folder(folder_path)
    object_path = "%s%s" % (folder_path, object_name)

    virtual_object_path = "/s/%s/%s" % (bucket_name, object_path)
    if not is_file_existed(virtual_object_path):
        print 'class StorageInterface delete_object() file unexisted! object_path: %s' % object_path
        return False

    bucket.delete_object(object_path)
    print 'class StorageInterface delete_object delete successfully!'
    return True
    
def set_object(bucket_name, folder_path, object_name, object_data):
    """update object
    
    Args:
        bucket_name: name of bucket
        folder_path: folder path
        object_name: name of object
        object_data: object raw data

        for example:
            object_name = 'sample.txt'
            object_data = "hello world"

    Returns:
        True if set successfully
        False if set failed
    """
    if not delete_object(bucket_name, folder_path, object_name):
        print 'class StorageInterface set_object() delete failed! object path: %s/%s/%s' % (bucket_name, folder_path, object_name)
        return False
    print 'class StorageInterface set_object() object path: %s/%s' % (folder_path, object_name)
    if not add_object(bucket_name, folder_path, object_name, object_data):
        print 'class StorageInterface set_object() add failed! object path: %s/%s/%s' % (bucket_name, folder_path, object_name)
        return False
    print 'class StorageInterface set_object() set successfully! object path: %s/%s/%s' % (bucket_name, folder_path, object_name)
    return True

def complete_folder(folder_path):
    """complete folder path

    Returns:
        folder path end with '/'
    """
    # folder should be end with '/'
    if folder_path[-1]!='/':
        folder_path += '/'
    return folder_path

def is_file_existed(object_path):
    """return whether file is existed

    Args:
        object_path: full path of object

    Returns:
        True if existed
        False if unexisted
    """
    if os.path.exists(object_path):
        return True
    else:
        return False

def get_max_file_index(bucket_name, folder_path):
    """get the max file index in specific folder

    Args:
        bucket_name: name of bucket
        folder_path: folder path

    Returns:
        -1 if no files
        an positive int (including zero) indicating the max file index
    """
    bucket = Bucket(bucket_name)
    folder_path = complete_folder(folder_path)

    # read files
    files = [i for i in bucket.list(path=folder_path)]

    # if the folder not exists or folder has no file
    if len(files)==0:
        return -1

    # if has files, return the max file index
    max_index = 0
    for i in files:
        num = int(i['name'].split(folder_path)[1].split('.')[0])
        if num>max_index:
            max_index = num

    return max_index