from django.contrib import admin

# Register your models here.
from models import DeployHost,DeployRequest

class DeployHostAdmin(admin.ModelAdmin):
    list_display = ('deploy_id','host_ip','deploy_type','deploy_retry','status','created_at','updated_at',)
    search_fields = ('deploy_id','host_ip','deploy_type','deploy_retry','status','created_at',)
    list_filter = ('deploy_id','host_ip','deploy_type','deploy_retry','status','created_at','updated_at',)
    
class DeployRequestAdmin(admin.ModelAdmin):
    list_display = ('deploy_form_id','app','module','version','group','conn','pre_script','post_script','deploy_tag','created_at','updated_at',)
    search_fields = ('deploy_form_id','app','module','version','group','conn','pre_script','post_script','deploy_tag',)
    list_filter = ('deploy_form_id','app','module','version','group','conn','pre_script','post_script','deploy_tag','created_at','updated_at',)
    
admin.site.register(DeployHost, DeployHostAdmin)
admin.site.register(DeployRequest, DeployRequestAdmin)
