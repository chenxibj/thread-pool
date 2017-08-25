import pika
import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from time import sleep
from random import randint
import threading
# from test1.lib.node_mgr import NodeMgr
import sys
sys.path.append("/home/chenxi/project/pga-ads")
from lib.rabbit_wrapper import RabbitWrpper
import pickle

futures = []
pool = ThreadPoolExecutor(5)
queue_list = ['hello', 'world']

def callback(ch, method, properties, body):
    print("callback")
    parm = parse_msg(body)
    # obj = threading.Thread(target=deploy_ctl_thread, args=[parm])
    # obj.start()
    print("callback return")

def parse_msg(msg):
    d = pickle.loads(msg)
    print d
    return d

def deploy_ctl_thread(parm):
    node_list = []
    for item in parm:
        node_list.append(NodeMgr.create_node(item))
    while True:
        for x in range(5):
            futures.append(pool.submit(node_list[x].start_deploy_fsm))

def start_deploy_fsm(node):
    print("start_deploy_fsm")
    node.state
    node.pre_check()
    node.node_deploy()
    node.post_check()

def listen():
    rabbit = RabbitWrpper()
    rabbit.fastInitConsumer(callback)
    rabbit.recvMsg()

def listen_err():
    rabbit = RabbitWrpper()
    rabbit.fastInitErrorConsumer(callback)
    rabbit.recvMsg()

obj = threading.Thread(target=listen)
obj.start()

obj1 = threading.Thread(target=listen_err)
obj1.start()



