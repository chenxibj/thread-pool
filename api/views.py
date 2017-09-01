from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json, requests
from ads import settings
import os,logging
from api.validators import *
from api.models import *
from lib.rabbit_wrapper import RabbitWrapper,RabbitWrapperError
from node_logger.main import fetchLog
from singleton_decorator import singleton
from lib.global_data import RemoteLogPath

# Create your views here.

logger = logging.getLogger(__name__)

@singleton
class RabbitmqClient(object):
    def __init__(self):
        worker_rabbit = RabbitWrapper()
        worker_rabbit.createWorkerProducer()
        error_rabbit = RabbitWrapper()
        error_rabbit.createErrorProducer()
        self.worker_rabbit = worker_rabbit
        self.error_rabbit = error_rabbit
  
    def send_worker_msg(self,msg):
        logger.info("send rabbitmq message: {}".format(msg))
        return self.worker_rabbit.sendMsg(msg)

    def send_error_msg(self,msg):
        logger.info("send rabbitmq message: {}".format(msg))
        return self.error_rabbit.sendMsg(msg)


@api_view(['POST','DELETE'])
def deploy(request):
    """
    deploy with parameters posted in body
    cancel deploy with deploy id in URL
    """
    if request.method == "POST":
        return kickoff_deploy(request)
    elif request.method == "DELETE":
        return cancel_deploy(request)

def kickoff_deploy(request):
    deploy_request = request.data
    logger.info("got deploy request: {}".format(deploy_request))
    validator = DeployPostValidator()
    (is_valid,error_msg) = validator(deploy_request)
    if not is_valid:
        logger.error("validation error: {}".format(error_msg))
        return Response({"status":{"code":"FAIL", "msg":"validation error: {}".format(error_msg)}},status=status.HTTP_200_OK)

    #initialize database
    deploy_trans_data = {key:deploy_request[key] for key in ("deploy_form_id","product","system","app","module","group","version","pre_script","post_script","deploy_tag","conn")}
    deploy_trans = DeployRequest.objects.create(**deploy_trans_data)
    for host in deploy_request["host"]:
        DeployHost.objects.create(deploy_id=deploy_trans, host_ip=host, deploy_type=deploy_request["deploy_type"], status = DeployHost.STATUS_NEW)

    status_data = get_deploy_status(deploy_trans.id)
    try:
        #call message queue to add task
        #{"deploy_form_id": 3,  "deploy_id": 4, "deploy_type": 5, "conn": 1, "product": "iaas","system":"iaas"}
        rabbit_client = RabbitmqClient()
        rabbit_client.send_worker_msg({'deploy_form_id':deploy_trans_data['deploy_form_id'], "deploy_id":deploy_trans.id,"deploy_type":"DEPLOY","conn":deploy_trans_data['conn'],"product":deploy_trans_data["product"],"system":deploy_trans_data["system"]})
    except RabbitWrapperError as e:
        logger.error("rabbitmq exception: {}".format(str(e)))
        return Response({"status":{"code":"FAIL", "msg":str(e)},"data":status_data},status=status.HTTP_200_OK)
    return Response({"status":{"code":"SUCCESS", "msg":""},"data":status_data},status=status.HTTP_200_OK)

def cancel_deploy(request):
    deploy_id = request.GET['deploy_id']
    deploy_request = DeployRequest.objects.get(pk=deploy_id)

    status_data = get_deploy_status(deploy_id)
    try:
        rabbit_client = RabbitmqClient()
        rabbit_client.send_error_msg({"deploy_form_id":deploy_request.deploy_form_id,"deploy_id":deploy_id,"deploy_type":"CANCEL","conn":deploy_request.conn,"product":deploy_request.product,"system":deploy_request.system})
    except RabbitWrapperError as e:
        logger.error("rabbitmq exception: {}".format(str(e)))
        return Response({"status":{"code":"FAIL", "msg":str(e)},"data":status_data},status=status.HTTP_200_OK)
    return Response({"status":{"code":"SUCCESS", "msg":""},"data":status_data},status=status.HTTP_200_OK)

def get_deploy_status(deploy_id):
    trans = DeployRequest.objects.get(pk=deploy_id)
    host_status = list()
    for host in DeployHost.objects.filter(deploy_id=deploy_id):
        host_status.append({host.host_ip:host.status})
    return {"deploy_id": deploy_id, "app":trans.app, "group":trans.group, "host": host_status}

@api_view(['GET'])
def deploy_status(request):
    """
    get host deploy status for deploy id
    ---
    parameters:
      deploy_id: string
    """
    deploy_id = request.GET['deploy_id'] 
    status_data = get_deploy_status(deploy_id)
    return Response({"status":{"code":"SUCCESS", "msg":""},"data":status_data},status=status.HTTP_200_OK)


@api_view(['GET'])
def deploy_log(request):
    """
    show log content of host for deploy id
    ---
    parameters:
      - name: deploy_id
        decription: deploy id
        required: true
        type: string
        paramType: form
      - name: host
        description: host ip
        required: true
        type: string
        paramType: form
    """
    host_ip = request.GET['host']
    deploy_id = request.GET['deploy_id']
    host = DeployHost.objects.get(deploy_id=deploy_id, host_ip=host_ip)
    deploy_request = DeployRequest.objects.get(pk=deploy_id)
    #validate
    if host is None:
        err_msg = "no deploy availabe on deploy_id={} and host={}".format(deploy_id, host_ip)
        logger.error(err_msg)
        return Response({"status":{"code":"FAIL","msg":err_msg},"log":""},status=status.HTTP_200_OK)
    if deploy_request.product not in RemoteLogPath:
        err_msg = "no remote log path available configured for {}".format(deploy_request.product)
        logger.error(err_msg)
        Response({"status":{"code":"FAIL","msg":err_msg},"log":""},status=status.HTTP_200_OK)
    contents = fetchLog(host_ip,RemoteLogPath[deploy_request.product])
    return Response({"status":{"code":"SUCCESS","msg":""},"log":contents},status=status.HTTP_200_OK)

