from django.contrib import admin
from .models import Members,Task
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display=['id','name','email','password']

class TaskAdmin(admin.ModelAdmin):
    list_display=['user','title','created_on','completed_status']

admin.site.register(Members,MemberAdmin)
admin.site.register(Task,TaskAdmin)