from collections import namedtuple

DeployData = namedtuple("DeployData", "host_ip deploy_id deploy_type service_name product system package_version")

#iaas default log path
REMOTE_PATH = "/tmp/chef-client.log"

RemoteLogPath = {"iaas":"/tmp/chef-client.log"}

#product mapping for driver
PRODUCT_DRIVER = {"iaas":"IaasDeployDriver","paas":"PaasDeployDriver"}
