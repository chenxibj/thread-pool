# -*- coding:utf-8 -*- 
from lib.ssh_wrapper import SshWrapper
import logging
logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}

class PreCheck(object):
    
    def __init__(self,host_ip):
        self.host_ip = host_ip
    
    def checkDiskSpace(self):
        ssh_conn = SshWrapper(self.host_ip)
        #space_command = """(($(df -h|grep export|awk '{print$5}'|tr -d "%")>95)) && space_is_not_enough > /tmp/chef-client.log 2>&1"""
        space_command = "uname -a"
        logger.info("checkDiskSpace command: %s" % space_command)
        result  = ssh_conn.execCommand(space_command)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = "Space is not enough"
        logger.info("checkDiskSpace result: %s" % res)
        return res
    
    def configIsCorrect(self):
        pass
