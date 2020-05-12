"""
Utils file used for the python compatiblity methods
"""

import sys

def string_compatibility(instance):
    if sys.version_info[0]==2:
        return instance
    else:
        return instance.encode('raw_unicode_escape')

def string_decode(instance):
    if sys.version_info[0]==2:
        return instance
    else:
        return instance.decode()

def string_required(instance):
    if sys.version_info[0] == 2:
        return str(instance)
    else:
        return instance

def string_or_bytes(instance):
    if sys.version_info[0] == 2:
        return str(instance)
    else:
        return bytes(instance)

def string_or_bytes_instance():
    if sys.version_info[0] == 2:
        return str
    else:
        return bytes

def buffer_or_memoryview():
    if sys.version_info[0] == 2:
        return buffer
    else:
        return memoryview

def memoryview_bytes_intances(instance):
    if sys.version_info[0] ==2:
        return instance
    else:
        return bytes(instance)