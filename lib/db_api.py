# -*- coding:utf-8 -*- 
from api.models import DeployHost
import logging
logger = logging.getLogger(__name__)


class DbWrapper(object):
    def __init__(self,host_ip,deploy_id):
        self.host_ip = host_ip
        self.deploy_id = deploy_id
        try:
            self.db_obj = DeployHost.objects.filter(host_ip=self.host_ip,deploy_id=self.deploy_id)
        except Exception as e:
            logger.info("filter db for host_ip error: %s" % e)
               
    def updateRetryNumber(self):
        try:
            current_number = self.db_obj[0].deploy_retry
            self.db_obj.update(deploy_retry = current_number + 1)
        except Exception as e:
            logger.info("update db for retry number error: %s" % e)
        
    def updateStatusInDb(self,current_status):
        try:
            self.db_obj.update(status=current_status)
        except Exception as e:
            logger.info("update db for status error: %s" % e)