# -*- coding:utf-8 -*- 
import pika
import pickle
import sys
import os
sys.path.append("{}/..".format(os.path.dirname(os.path.abspath(os.path.realpath(__file__)))))
from lib.rabbit_wrapper import RabbitWrapper, RabbitWrapperError
from threading import Thread
from random import randint
from time import sleep
import logging
from lib.global_data import DeployData

os.environ['DJANGO_SETTINGS_MODULE']='ads.settings'

# data = DeployData(3, 1, 3, 5, 7, "iaas" "ebs", "1.1.1")
# print data

msg = {"deploy_form_id": 3,  "deploy_id": 1, "deploy_type": 5, "conn": 1, "driver_name": "iaas"}
template = {"deploy_form_id": 1,  "deploy_id": 1, "deploy_type": "UPGRADE", "conn": 5,
            "product": "iaas", "system":"jcloud"}

# class TestNode():
#     def __init__(self, deploy_data):
#         print deploy_data.deploy_id
#
# data = DeployData(3, 1, 3, 5, 7, "iaas" "ebs", "1.1.1")
# t =  TestNode(data)

# rabbit1 = RabbitWrapper()
# rabbit1.createWorkerProducer()
# # data = rabbit1.createMsg(1, 1, "upgrade", 1, "iaas")
# rabbit1.sendMsg(template)
try:
    rabbit = RabbitWrapper()
    rabbit.createErrorProducer()
    # rabbit.createWorkerProducer()

    while True:
        # data = rabbit.createMsg(1, 1, "upgrade", 1, "iaas")
        rabbit.sendMsg(template)
        sleep(2)

except RabbitWrapperError as e:
    print("hello world")
    print e

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
#
# channel.exchange_declare(exchange='logs',
#                          type='fanout')
#
# message = "info: Hello World!"
# channel.basic_publish(exchange='logs',
#                       routing_key='',
#                       body=message)
# print(" [x] Sent %r" % message)
# connection.close()
