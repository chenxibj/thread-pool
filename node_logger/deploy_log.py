# -*- coding:utf-8 -*- 
import os
import time
import logging
import commands
from lib.global_data import REMOTE_PATH
from lib.ssh_wrapper import SshWrapper
from _threading_local import local

logger = logging.getLogger(__name__)
res = {"status":1,"msg":"log download success"}

def LogOper(host_ip,log_path=REMOTE_PATH):
    fs = SshWrapper(host_ip)
    result = fs.execCommand(log_path,log_path)
    if result["status"]:
        log_content = result["msg"]
    else:
        log_content = "Get log fail....."
        logger.info("LogOper result: %s" % log_content)
    return log_content
