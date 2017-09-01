# -*- coding:utf-8 -*- 
from lib.ssh_wrapper import SshWrapper
import logging
logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}

class PostCheck(object):
    
    def __init__(self,host_ip):
        self.host_ip = host_ip
    
    def checkPackageVersion(self,package_version):
        ssh_conn = SshWrapper(self.host_ip)
        ver_command = "/usr/bin/rpm -qa|grep %s || %s >> /tmp/chef-client.log 2>&1" % (package_version,package_version)
        logger.info("checkPackageVersion command: %s" % ver_command)
        result  = ssh_conn.execCommand(ver_command)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = "Package version check fail"
        logger.info("checkPackageVersion result: %s" % res)
        return res
    
    def checkServiceIsRestarted(self,service_name):
        """
                    服务的running时间，大于100s或非running，可认为失败
        """
        ssh_conn = SshWrapper(self.host_ip)
        sta_commands = """(((($(date +%s)-$(date -d "$(systemctl status """ + service_name + """|grep running|awk '{print$6" "$7}')" +%s)))>100)) &&  restart_fail >> /tmp/chef-client.log 2>&1""" 
        logger.info("checkServiceIsRestarted command: %s" % sta_commands)
        result  = ssh_conn.execCommand(sta_commands)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = " service restart check fail"
        logger.info("checkServiceIsRestarted result: %s" % res)
        return res

        