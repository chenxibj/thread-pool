from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DeployHost(models.Model):
    deploy_form_id = models.CharField(max_length=50,  null=True)
    deploy_id = models.CharField(max_length=50,  null=True)
    host = models.CharField(max_length=1500, blank=True, null=True)
    log_file = models.CharField(max_length=150, blank=True, null=True)
    deploy_type = models.CharField(max_length=10, blank=True, null=True)
    deploy_retry = models.CharField(max_length=50,  null=True)
    status = models.CharField(max_length=150, blank=True, null=True)

class DeployTransaction(models.Model):
    deploy_form_id = models.CharField(max_length=50, null=True)
    deploy_id = models.CharField(max_length=50, null=True)
    app = models.CharField(max_length=50, null=True)
    module = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=150, blank=True, null=True)
    total_host = models.CharField(max_length=50, null=True)
    conn = models.CharField(max_length=50, null=True)
    pre_script = models.CharField(max_length=50, null=True)
    post_script = models.CharField(max_length=50, null=True)
    deploy_script = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
