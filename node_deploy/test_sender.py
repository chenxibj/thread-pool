# -*- coding:utf-8 -*- 
import pika
import pickle
import sys
sys.path.append("/home/chenxi/project/pga-ads")
from lib.rabbit_wrapper import RabbitWrpper

msg = {"deploy_form_id": 1,  "deploy_id": 2, "deploy_type": 3}
msg1 = {"deploy_form_id": 3,  "deploy_id": 4, "deploy_type": 5}
# data = pickle.dumps(d)
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='hello')
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=data)
#
# # print(" [x] Sent 'Hello World!'")
# connection.close()

rabbit = RabbitWrpper()
rabbit_error = RabbitWrpper()
rabbit.fastInitProcuder()
rabbit_error.fastInitErrorProcuder()
rabbit.sendMsg(msg)
rabbit_error.sendMsg(msg1)

