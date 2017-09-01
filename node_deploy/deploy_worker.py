from threading import Thread
from time import sleep
import sys, os, logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] ='ads.settings'
from ads import settings
import django
django.setup()

from api.models import DeployHost, DeployRequest
from lib.rabbit_wrapper import RabbitWrapper
from node_deploy.node_mgr import HostNode
from lib.thread_pool import ThreadPool
import paramiko

class DeployWorker():

    def __init__(self):
        print("DeployWorker")
        self.deploy_id = -1
        self.deploy_form_id = -1
        self.deploy_type = None
        self.conn = -1
        self.driver_name = None

        self.pool = ThreadPool()
        self.msg_handler = RabbitWrapper()
        self.msg_handler.createWorkerConsumer(self.callbackWorker)
        self.error_msg_handler = RabbitWrapper()
        self.error_msg_handler.createErrorConsumer(self.callbackCancelTask)

    def getDeployRequest(self):
        return DeployRequest.objects.filter(id=self.deploy_id)[:1].get()

    def getDeployNodeList(self):
        return DeployHost.objects.filter(deploy_id=self.deploy_id)

    def getDeployParms(self):
        self.getDeployNodeList()
        test_parms = []
        deploy_request = self.getDeployRequest()
        # for item in detail:
        #     print("module %s" % item.module)
        #     module = item.module
        host_list = self.getDeployNodeList()
        for host in host_list:
            parm = {}
            parm["host_ip"] = host.host_ip
            parm["deploy_id"] = host.deploy_id.id
            parm["deploy_type"] = host.deploy_type
            parm["system"] = deploy_request.system
            parm["product"] = deploy_request.product
            parm["service_name"] = deploy_request.module
            test_parms.append(parm)
            print(test_parms)
        return test_parms

    def runDeploy(self, host_ip, deploy_id, deploy_type, service_name, product, system):
        print("runDeploy")
        print(host_ip, deploy_id, deploy_type, service_name, product, system)
        t = HostNode(host_ip, deploy_id, deploy_type, service_name, product, system)
        t.pre_check()

    def startDeploy(self, cmd_msg):
        self.deploy_id = cmd_msg['deploy_id']
        self.deploy_form_id = cmd_msg['deploy_form_id']
        self.deploy_type = cmd_msg['deploy_type']
        self.conn = cmd_msg['conn']
        self.product = cmd_msg['product']
        self.system = cmd_msg['system']

        task_parms = self.getDeployParms()
        print("task_parms %s" % task_parms)
        self.pool.setMaxWorkers(self.conn)
        self.pool.addTask(self.runDeploy)
        # print("run task")
        self.pool.runTaskPerParm(task_parms)

    def updateCancelToDB(self):
        print("updateCancelToDB")
        DeployHost.objects.filter(deploy_id=self.deploy_id, status=DeployHost.STATUS_NEW).\
            update(status=DeployHost.STATUS_CANCEL)
        # DeployHost.objects.filter(deploy_id=self.deploy_id).exclude(
        #     status=DeployHost.STATUS_FAIL).exclude(
        #     status=DeployHost.STATUS_SUCCESS).update(
        #     status=DeployHost.STATUS_CANCEL)

    def callbackWorker(self, ch, method, properties, body):
        print("callbackWorker")
        cmd_msg = self.msg_handler.parseMsg(body)
        print(cmd_msg)
        if cmd_msg == -1:
            print("error msg do nothing just return")
        else:
            print("start crtl thread")
            self.startDeploy(cmd_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # raise Exception("test callback exception")
        # obj = threading.Thread(target=deploy_ctl_thread, args=[parm])
        # obj.start()

    def callbackCancelTask(self, ch, method, properties, body):
        print("callbackCancelTask")
        parm = self.error_msg_handler.parseMsg(body)

        if parm == -1:
            print("error msg do nothing just return")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if parm['deploy_id'] == self.deploy_id:
            print("cancel task is in current process, proceed it")
            self.pool.cancelTask()
            self.updateCancelToDB()
            # ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print("ignore the cancel request")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listenWorkerQueue(self):
        self.msg_handler.recvMsg()

    def listenErrQueue(self):
        self.error_msg_handler.recvMsg()

if __name__ == '__main__':
    print("a")
    # def updateCancelToDB():
    #     print("updateCancelToDB")
    #     DeployHost.objects.filter(deploy_id=1).exclude(
    #         status=DeployHost.STATUS_FAIL).exclude(
    #         status=DeployHost.STATUS_SUCCESS).update(
    #         status=DeployHost.STATUS_CANCEL)
    #
    # updateCancelToDB()
    # test_parms = [{'product': 'iaas', 'service_name': 'jcloud-api-module', 'system': 'iaas',
    #                'host_ip': '172.27.53.31', 'deploy_id': 1, 'deploy_type': 'DEPLOY'}]
    #
    # def runDeploy(host_ip, deploy_id, deploy_type, service_name, product, system):
    #     print("runDeploy")
    #     print(host_ip, deploy_id, deploy_type, service_name, product, system)
    #     t = HostNode(host_ip,deploy_id,deploy_type,service_name,product,system)
    #     t.pre_check()
    #
    def load_url(index, str):
        # if str == "error":
        #     raise ThreadPoolError
        # print("--------------------")
        sleep(2)
        # print("this task is %s %s" % (index, str))

    pool = ThreadPool()
    pool.setMaxWorkers(20)
    pool.addTask(load_url, 1, "chenxi")
    # pool.runTaskPerNum(20000)
    obj = Thread(target=pool.runTaskPerNum, args=[200])
    obj.start()
    # sleep(2)
    print(len(pool.threads))
    sleep(1)
    print(len(pool.threads))
    pool.cancelTask()
    # pool.runTaskPerParm(test_parms)

    # t = HostNode(**test_parms)
    # t.pre_check()
    # worker = DeployWorker()
    # worker.listenWorkerQueue()
    # class Test():
    #     def __init__(self, index):
    #         print("test class sleep")
    #         sleep(8)
    #         print("class test %s" % index)
    #
    #
    # def load_url(deploy_type, service_name, host_ip, deploy_id):
    #     print("this task is %s %s %s %s" % (deploy_type, service_name, host_ip, deploy_id))
    #     t = HostNode(host_ip, deploy_id, deploy_type, service_name)
    #     t.pre_check()
    #
    # def runDeploy(host_ip, deploy_id, deploy_type, service_name):
    #     print("runDeploy")
    #     print host_ip
    #     print deploy_id
    #     print deploy_type
    #     print service_name
    #     t = HostNode(host_ip, deploy_id, deploy_type, service_name)
    #     t.pre_check()

    # test_parms = [{"deploy_type": 123, "service_name": "chenxi", "host_ip": "192.168.1.1", "deploy_id": 1}]
    # test_parms = [{"host_ip": "192.168.1.1", "deploy_id": 1, "deploy_type": "deploy",
                   # "service_name": "cc-router"}]
    # test_parms = []
    # module = ""
    # detail = DeployRequest.objects.filter(id=1)
    # for item in detail:
    #     print("module %s" % item.module)
    #     module = item.module
    # host_list = DeployHost.objects.filter(deploy_id=1)
    # for host in host_list:
    #     # self.runDeploy(host.host_ip, host.deploy_id, host.deploy_type, module)
    #     parm = {}
    #     parm["host_ip"] = host.host_ip
    #     parm["deploy_id"] = host.deploy_id_id
    #     parm["deploy_type"] = host.deploy_type
    #     parm["service_name"] = module
    #     test_parms.append(parm)
    #

    # # get_node_list("aa")
    # worker = DeployWorker()
    # # worker.listenWorkerQueue()
    # # worker.listenErrQueue()
    # t = Thread(target=worker.listenWorkerQueue)
    # t.start()
    #
    # t1 = Thread(target=worker.listenErrQueue)
    # t1.start()



