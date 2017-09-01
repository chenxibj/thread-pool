# -*- coding:utf-8 -*- 
import time,os,sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] ='ads.settings'
from ads import settings
import django
django.setup()
from transitions import Machine, State
from lib.global_data import PRODUCT_DRIVER
# from django.db.models.signals import post_init
# from django.dispatch import receiver
# from transitions.extensions import GraphMachine
# from IPython.display import Image, display, display_png
from node_driver.deploy_driver_mgr import DeployDriverMgr
from node_check.main import runPostCheck, runPreCheck
from lib.db_api import DbWrapper
from api.models import DeployHost

logger = logging.getLogger(__name__)

class NodeMgr():
    @staticmethod
    def create_node(parm):
        checker = NodeChecker()
        logger = NodeLogger()
        deploy_tool = DeployTool()
        print("create_node")
        return HostNode(checker, logger, deploy_tool)

class HostNode(object):

    def __init__(self,host_ip,deploy_id,deploy_type,service_name,product,system,package_version=None):
        self.host_ip =host_ip
        self.deploy_id = deploy_id
        self.deploy_type = deploy_type
        self.service_name = service_name
        self.product = product
        self.package_version = package_version
        self.db_oper = DbWrapper(self.host_ip,self.deploy_id)
        self.node_status = False
        self.deploy_status = False
        self.config_status = False
        self.__on_new_deploy()
        self.__getDriver()
        states = [
            State(name='new'),
            State(name='deploy_ready',on_enter=["on_deploy_ready"]),
            State(name='deploy_done',on_enter=["on_deploy_done"]),
            State(name='pre_check_fail',on_enter=["on_pre_check_fail"]),
            State(name='deploy_fail',on_enter=["on_deploy_fail"]),
            
            State(name='post_check_fail',on_enter=["on_post_check_fail"]),
            
            State(name='success',on_enter=["on_success"]),
            State(name='fail',on_enter=["on_fail"])
        ]
        transitions = [
            {'trigger': 'pre_check', 'source': 'new', 'dest': 'deploy_ready', 'conditions': 'is_node_ok',
             'prepare': 'run_pre_check', 'after':'node_deploy'},
            {'trigger': 'pre_check', 'source': 'new', 'dest': 'pre_check_fail',
             'prepare': 'run_pre_check', 'unless':['is_node_ok'], 'after':'retry1'},
                       
            {'trigger': 'retry1', 'source': 'pre_check_fail', 'dest': 'deploy_ready', 'conditions': 'is_node_ok',
             'prepare': 'run_pre_check', 'after':'node_deploy'},
            {'trigger': 'retry1', 'source': 'pre_check_fail', 'dest': 'fail', 'unless': ['is_node_ok'],
             'prepare': 'run_pre_check'},
                       
            {'trigger': 'node_deploy', 'source': 'deploy_ready', 'dest': 'deploy_done', 'prepare': 'run_deploy_node',
             'conditions': 'is_deploy_ok', 'after':'post_check'},
            {'trigger': 'node_deploy', 'source': 'deploy_ready', 'dest': 'deploy_fail', 'prepare': 'run_deploy_node',
             'unless': ['is_deploy_ok'], 'after':'retry2'},
                       
            {'trigger': 'retry2', 'source': 'deploy_fail', 'dest': 'deploy_done', 'conditions': 'is_deploy_ok',
             'prepare': 'run_deploy_node'},
            {'trigger': 'retry2', 'source': 'deploy_fail', 'dest': 'fail', 'unless': ['is_deploy_ok'],
             'prepare': 'run_deploy_node', 'after':'run_fail_handler'},
                       
                       
            {'trigger': 'post_check', 'source': 'deploy_done', 'dest': 'success', 'prepare': 'run_post_check',
             'conditions': 'is_config_ok'},
            {'trigger': 'post_check', 'source': 'deploy_done', 'dest': 'post_check_fail', 'prepare': 'run_post_check',
              'unless': ['is_config_ok'], 'after':'retry3'},
            
            {'trigger': 'retry3', 'source': 'post_check_fail', 'dest': 'success', 'prepare': 'run_post_check',
             'conditions': 'is_config_ok'},
            {'trigger': 'retry3', 'source': 'post_check_fail', 'dest': 'fail', 'prepare': 'run_post_check', 
             'unless': ['is_config_ok']},
        ]

        # Initialize the state machine
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='new', queued=True)
    def __getDriver(self):
        self.func = DeployDriverMgr(self.host_ip,self.service_name,self.product)

    def __on_new_deploy(self):
        logger.info("###################Ready to deploy: update retrynumber in db######################")
        self.db_oper.updateRetryNumber()
        self.db_oper.updateStatusInDb(DeployHost.STATUS_NEW)
        
    def on_deploy_ready(self):
        logger.info("####################pre check is ok: update status in db######################")        
        self.db_oper.updateStatusInDb(DeployHost.STATUS_DEPLOY_READY)
    
    def on_deploy_done(self):
        logger.info("####################deploy is ok: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_DEPLOY_DONE)
        
    def on_pre_check_fail(self):
        logger.info("####################pre check is fail: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_PRE_CHECK_FAIL)
    
    def on_deploy_fail(self):
        logger.info("####################deploy is fail: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_DEPLOY_FAIL)
        
    def on_post_check_fail(self):
        logger.info("####################post check is fail: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_POST_CHECK_FAIL)

    def on_fail(self):
        print "on_enter_fail"
        logger.info("####################post check is fail: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_FAIL)
        
    def on_success(self):
        print("on_enter_success")
        logger.info("####################post check is success: update status in db######################")
        self.db_oper.updateStatusInDb(DeployHost.STATUS_SUCCESS)

    def raise_error(self): 
        raise ValueError("Oh no")

    def finalize(self):
        print("finalize")

        
    #conditions
    def is_node_ok(self):
        logger.info("###################is pre check ok######################")
        return self.node_status

    def is_deploy_ok(self):
        logger.info("###################is deploy ok######################")
        return self.deploy_status

    def is_config_ok(self):
        logger.info("###################is post check ok######################")
        return self.config_status

    def run_pre_check(self):
        logger.info("###################run pre check script######################")
        try:
            if self.func.preCheck()["status"]:       
                self.node_status = True
        except Exception as e:
            logger.info(type(e) + ":" + e)

    def run_deploy_node(self):
        logger.info("###################run chef-client######################")
        try:
            if self.func.deploy(self.deploy_type.lower())["status"]:
                self.deploy_status = True
        except Exception as e:
            logger.info(type(e) + ":" + e)
            
    def run_post_check(self):
        logger.info("###################run post check script######################")
        try:
            if self.func.postCheck()["status"]:
                self.config_status = True
        except Exception as e:
            logger.info(type(e) + ":" + e)

    def run_fail_handler(self):
        print("run_fail_handler")

    '''
    def timer_func(self):
        print self.machine.state
        self.machine.cancel()
    '''   
if __name__ == '__main__':
    batman = HostNode("172.27.53.31",1,"deploy","cc#cc-server","iaas","compute.vesion12.34")
    print(batman.state)
    batman.pre_check()
    print batman.state
    # batman.node_deploy()
    # print(batman.state)
    #timer(timer_func)

    # time.sleep(2)
    # print(batman.state)
    # time.sleep(2)