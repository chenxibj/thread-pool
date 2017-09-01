from django.core.validators import integer_validator,validate_ipv4_address,MinValueValidator,MaxValueValidator
from api.models import DeployHost
from django.core.exceptions import ValidationError 

class DeployPostValidator(object):
    def __init__(self):
        self.fields = ('deploy_form_id','app','module','group','version','host','pre_script','post_script','deploy_type','conn','deploy_tag')

    def __call__(self,dct):
        for field in self.fields:
            if field not in dct:
                return (False,"no value for field {}".format(field))
            method = getattr(self,"validate_{}".format(field),None)
            if callable(method):
                error_msg = "value '{}' for field '{}' is not valid".format(dct[field],field)
                try:
                    method(dct[field])
                except ValidationError as e:
                    return (False, error_msg)
        return (True,"OK")

    def validate_deploy_form_id(self,form_id):
        integer_validator(form_id)
 
    def __validate_string(self,value):
        if not isinstance(value,str) and not isinstance(value,unicode):
            raise ValidationError

    def validate_app(self,app):
        self.__validate_string(app)

    def validate_module(self,module):
        self.__validate_string(module)

    def validate_group(self,group):
        self.__validate_string(group)

    def validate_version(self,version):
        self.__validate_string(version)

    def validate_host(self,host_list):
        if not isinstance(host_list,list):
           raise ValidationError
        for ipv4 in host_list:
            validate_ipv4_address(ipv4)

    def validate_pre_script(self,script):
        self.__validate_string(script)

    def validate_post_script(self,script):
        self.__validate_string(script)

    def validate_deploy_type(self,deploy_type):
        self.__validate_string(deploy_type)
        deploy_type_list = [item[0] for item in DeployHost.DEPLOY_TYPE_CHOICES]
        if deploy_type not in deploy_type_list:
            raise ValidationError

    def validate_conn(self,conn):
        for validate in (integer_validator,MinValueValidator(1),MaxValueValidator(9999)):
            validate(conn)

    def validate_deploy_tag(self,tag):
        self.__validate_string(tag)
