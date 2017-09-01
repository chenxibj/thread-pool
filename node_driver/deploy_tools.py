# -*- coding:utf-8 -*- 
from lib.ssh_wrapper import SshWrapper
import logging
logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}

def convertModelsToRunCommand(service_name,run_type):
    '''
    cc#cc-server---> cc::check-cc-server---> chef-client - o "recipe[cc::deploy-cc-server]"
    run_type = ["deploy","restart","pre-check","post-check"]
    '''
    res_tmp = service_name.strip().split("#")
    res_command = "chef-client - o 'recipe[" + res_tmp[0] + "::" + run_type + "-" + res_tmp[1] + "]' >>/tmp/chef-client.log"
    return res_command

class ChefCookBook(object):
    
    def __init__(self,host_ip,service_name):
        self.host_ip = host_ip
        self.service_name = service_name
    
    def runChef(self,run_type):
        ssh_conn = SshWrapper(self.host_ip)
        run_command = convertModelsToRunCommand(self.service_name,run_type)
        logger.info("runChef command: %s" % run_command)
        result  = ssh_conn.execCommand(run_command)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = "run chef fail"
        logger.info("runChef result: %s" % res)
        return res

class SaltStack(object):
    
    def __init__(self,host_ip,service_name):
        self.host_ip = host_ip
        self.service_name = service_name
        
    def runSalt(self,run_type=None):
        ssh_conn = SshWrapper(self.host_ip)
        if run_type:
            run_command = "salt -N %s state.highstate -t 10" % self.service_name
        else:
            run_command = "salt -N %s test.ping" % self.service_name
        logger.info("runSalt command: %s" % run_command)
        result  = ssh_conn.execCommand(run_command)
        if not result["status"]:
            res["status"] = 0
            res["msg"] = "run salt fail"
        logger.info("runSalt result: %s" % res)
        return res
        