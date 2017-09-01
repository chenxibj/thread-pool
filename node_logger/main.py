# -*- coding:utf-8 -*- 
from  deploy_log import LogOper

def fetchLog(host_ip,log_path):
    lo = LogOper(host_ip,log_path)
    return lo

if __name__ == "__main__":
    print fetchLog("172.27.33.32","/tmp/chef-client.log")
