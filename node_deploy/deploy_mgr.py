# -*- coding:utf-8 -*- 

import pika

# main rest entry entry
class DeployMgr():
    def __init__(self):
        print("init")

    def valid_parms(self, **kargv):
        print("")

    def start_deploy_process(self, **kargv):
        print("deploy_process")

        valid_parms(**kargv)
        deploy_id = generate_deploy_id()
        update_db()

        notify_backend(msg)

        # checker = NodeChecker()
        # logger = NodeLogger()
        # deploy_tool = DeployTool.get_tool("chef")
        # fork{
        # thread{
        #     goroutine channel
        # node = NodeMgr.create_node(checker, logger, deploy_tool)
        # node.pre_check()
        # node.node_deploy
        # }
        # }
        return deploy_id



    def generate_deploy_id(self):
        print("generate_deploy_id")

    def update_db(self):
        print("update_db")

    def get_deploy_status(self):
        print("deploy_status")

    def cancel_deploy(self):
        print("cancel")

    def init_mq(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello')

    def notify_backend(self, msg):
        self.channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=msg)
