# -*- coding:utf-8 -*-
from deploy_tools import ChefCookBook,SaltStack

res = {"status":1,"msg":"success"}

class DeployDriver(object):
    
    def __init__(self,host_ip,service_name):
        self.host_ip = host_ip
        self.service_name = service_name
    
    def preCheck(self):
        pass
    
    def postCheck(self):
        pass

    def deploy(self, deploy_type):
        pass
    
class IaasDeployDriver(DeployDriver):
    
    def preCheck(self):
        cb = ChefCookBook(self.host_ip,self.service_name)
        result = cb.runChef("precheck")
        return result 
    
    def postCheck(self):
        cb = ChefCookBook(self.host_ip,self.service_name)
        result = cb.runChef("postcheck")
        return result 

    def deploy(self,deploy_type):
        cb = ChefCookBook(self.host_ip,self.service_name)
        result = cb.runChef(deploy_type)
        return result 
    

class PaasDeployDriver(DeployDriver):
    
    def preCheck(self):
        ss = SaltStack(self.host_ip,self.service_name)
        result = ss.runSalt()

    def deploy(self):
        return res
    
        
    def postCheck(self,deploy_type):
        ss = SaltStack(self.host_ip,self.service_name)
        result = ss.runSalt(deploy_type)

    
def DeployDriverMgr(host_ip,service_name,dvr_name):
    if dvr_name == "iaas":
        return IaasDeployDriver(host_ip,service_name)
    elif dvr_name == "paas":
        return PaasDeployDriver(host_ip,service_name)
    else:
        raise DriverNameIsNotExist("Driver name is not exist")
