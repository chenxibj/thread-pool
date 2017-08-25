# -*- coding:utf-8 -*- 
from post_check import PostCheck
from pre_check import PreCheck

res = {"status":1,"msg":"success"}

def runPostCheck(host_ip,package_version,service_name):
    pc = PostCheck(host_ip)
    if not pc.checkPackageVersion(package_version)["status"]:
        res["status"] = 0
        res["msg"] = "package version check fail"
    if not pc.checkServiceIsRestarted(service_name)["status"]:
        res["status"] = 0
        res["msg"] = "service restart check fail"
    return res


def runPreCheck(host_ip):
    prec = PreCheck(host_ip)
    if not prec.checkDiskSpace()["status"]:
        res["status"] = 0
        res["msg"] = "disk space is not enough"
    return res

if __name__ == "__main__":
    print runPostCheck("172.19.23.105","compute","openstack-compute")
    print runPreCheck("172.19.23.105")