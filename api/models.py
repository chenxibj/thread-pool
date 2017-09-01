from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DeployHost(models.Model):
    DEPLOY_TYPE_DEPLOY= u'DEPLOY'
    DEPLOY_TYPE_RESTART = u'RESTART'
    DEPLOY_TYPE_DOWNGRADE = u'ROLLBACK'
    DEPLOY_TYPE_CANCEL = u'CANCEL'
    DEPLOY_TYPE_CHOICES = (
        (DEPLOY_TYPE_DEPLOY, u'deploy'),
        (DEPLOY_TYPE_RESTART, u'restart'),
        (DEPLOY_TYPE_DOWNGRADE, u'rollback'),
        (DEPLOY_TYPE_CANCEL, u'cancel')
    )

    STATUS_NEW = u'NEW'
    STATUS_DEPLOY_READY = u'DEPLOY_READY'
    STATUS_PRE_CHECK_FAIL = u'PRE_CHECK_FAIL'
    STATUS_DEPLOY_DONE = u'DEPLOY_DONE'
    STATUS_DEPLOY_FAIL = u'DEPLOY_FAIL'
    STATUS_POST_CHECK_FAIL = u'POST_CHECK_FAIL'
    STATUS_SUCCESS = u'SUCCESS'
    STATUS_FAIL = u'FAIL'
    STATUS_CANCEL = u'CANCEL'
    STATUS_CHOICES = (
        (STATUS_NEW, u'new'),
        (STATUS_DEPLOY_READY, u'deploy_ready'),
        (STATUS_PRE_CHECK_FAIL, u'pre_check_fail'),
        (STATUS_DEPLOY_DONE, u'deploy_done'),
        (STATUS_DEPLOY_FAIL, u'deploy_fail'),
        (STATUS_POST_CHECK_FAIL, u'post_check_fail'),
        (STATUS_SUCCESS, u'success'),
        (STATUS_FAIL, u'fail'),
        (STATUS_CANCEL, u'cancel')
    )      
    deploy_id = models.ForeignKey(u"DeployRequest")
    host_ip = models.CharField(max_length=50, null=False)
    deploy_type = models.CharField(max_length=20,choices=DEPLOY_TYPE_CHOICES,default=DEPLOY_TYPE_DEPLOY)
    deploy_retry = models.IntegerField(default=0)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = u'DeployHost'
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.host_ip

class DeployRequest(models.Model):
    deploy_form_id = models.CharField(max_length=50, unique=True,null=False)
    product = models.CharField(max_length=50, null=True)
    system = models.CharField(max_length=50, null=True)
    app = models.CharField(max_length=50, null=True)
    module = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    conn = models.IntegerField(null=False,default=1)
    pre_script = models.CharField(max_length=250, null=True)
    post_script = models.CharField(max_length=250, null=True)
    deploy_tag = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = u'DeployRequest'
        verbose_name_plural = verbose_name
