# -*- coding:utf-8 -*- 
from lib.sshwrapper import SshWrapper
res = {"status":1,"msg":"success"}

class PreCheck(object):
    
    def __init__(self,host_ip):
        self.host_ip = host_ip
    
    def checkDiskSpace(self):
        ssh_conn = SshWrapper(self.host_ip)
        space_command = """(($(df -h|grep export|awk '{print$5}'|tr -d "%")>95)) || space is not enough"""
        result  = ssh_conn.execCommand(space_command)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = "Package version check fail"
        return res
    
    def configIsCorrect(self):
        pass
