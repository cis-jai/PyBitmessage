"""
Utils file used for the python compatiblity methods
"""
import sys

def string_compatibility(instance):
    if sys.version_info[0]==2:
        return instance
    else:
        return instance.encode()