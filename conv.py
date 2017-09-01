#!/usr/bin/env python
import base64
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def ReadRsa(rsa_file):
    with open(rsa_file) as f:
          rsa_file_str = f.read()
    return base64.decodestring(rsa_file_str)

def WriteRsa(rsa_file_s):
    if not os.path.isdir("/home/admin/.ssh/"):
        os.makedirs("/home/admin/.ssh/")
    with open("/home/admin/.ssh/id_rsa","wb") as fo:
        fo.write(rsa_file_s)

rs = ReadRsa(os.path.join(BASE_DIR, "rsa.py"))
WriteRsa(rs)
